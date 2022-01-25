
import os
import yaml
import json
import requests as r
from subprocess import Popen
from requests.auth import HTTPBasicAuth


class KafKaProxy:

    def __init__(self):
        print('Initializing project from config file')
        # Read config file
        with open('/config/config.yml', 'r') as fp:
            self.env = yaml.safe_load(fp)
            self.env['service_key']['kafka'] = json.loads(self.env['service_key']['kafka'])
            self.env['cf']['otp'] = os.getenv('CF_OTP')

        self.parse_kafka_service()
        self.setup_vlan()
        self.cf_login()
        self.setup_tunnels()

    def parse_kafka_service(self):
        print('Parsing vCap file')

        # Extract broker info from kafka service key
        kafka = self.env['service_key']['kafka']
        tmp = kafka['cluster']['brokers'].split(',')

        brokers = []
        for itr, broker in enumerate(tmp):
            tmp2 = broker.split(':')
            brokers.append(
                {
                    "host": tmp2[0],
                    "port": tmp2[1],
                    "host_port": broker
                }
            )

        # Get auth token
        k_user = kafka['username']
        k_pass = kafka['password']
        k_token_url =  kafka['urls']['token']

        response = r.post(
            k_token_url,
            auth=HTTPBasicAuth(k_user, k_pass),
            data="grant_type=client_credentials",
            headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            })
        k_auth_token = response.json()['access_token']

        self.env['kafka'] = {
            'brokers': brokers,
            'user': k_user,
            'pass': k_auth_token
        }

    def setup_vlan(self):
        print('Creating vLan interfaces')

        for id, broker in enumerate(self.env['kafka']['brokers']):
            cmd = f'ip link add link eth0 name eth0.{id} type vlan id {id}'
            Popen(cmd, shell=True).wait()

            cmd = f'ip link set dev eth0.{id} up'
            Popen(cmd, shell=True).wait()

            cmd = f'ip addr add {broker["host"]}/24 dev eth0.{id}'
            Popen(cmd, shell=True).wait()

    def cf_login(self):
        print('Logging in into CF')
        cmd = f'cf login -a {self.env["cf"]["api"]} -o {self.env["cf"]["org"]} -s {self.env["cf"]["space"]} -u {self.env["cf"]["user"]} -p {self.env["cf"]["pass"]}{self.env["cf"]["otp"]}'
        Popen(cmd, shell=True).wait()

    def setup_tunnels(self):
        print('Starting tunnel')
        for broker in self.env['kafka']['brokers']:
            cmd = f'cf ssh {self.env["cf"]["app"]} -L {broker["host_port"]}:{broker["host_port"]} -T -N &'
            Popen(cmd, shell=True).wait()

    def start(self):
        print('Starting proxy server')

        server_mapping = ''
        for id, broker in enumerate(self.env['kafka']['brokers']):
            server_mapping += f' --bootstrap-server-mapping "{broker["host_port"]},0.0.0.0:{30000+id},localhost:{30000+id}" '

        cmd = f'kafka-proxy server {server_mapping}' \
              f' --sasl-username "{self.env["kafka"]["user"]}" ' \
              f' --sasl-password "{self.env["kafka"]["pass"]}" ' \
              f' --sasl-method "PLAIN" ' \
              f' --sasl-enable ' \
              f' --tls-enable ' \
              f' --tls-insecure-skip-verify ' \
              f' --debug-enable '
        Popen(cmd, shell=True).wait()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    KafKaProxy().start()
