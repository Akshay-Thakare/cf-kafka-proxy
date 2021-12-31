
## CF (SAP BTP) Kafka Proxy

### Quickstart
1. Clone project
2. Add details to `config/config.yml`
3. Run `docker-compose up`

Docker image can be found [here](https://hub.docker.com/r/register9091/cf-kafka-proxy)

### For future project contributors

The CF Kafka Proxy project is an extension of (kafka-proxy)[https://github.com/grepplabs/kafka-proxy] which enables users to proxy CF kafka service requests to their local machines.
Additionally, a (kafka-ui)[https://github.com/provectus/kafka-ui] to easily manage and test the service.

The entire project is contained in `main.py` file and the run script is in `run.sh` file. \
The `config.yml` file which contains all the parameters needed to run the project, users are expected to populate this file with appropriate credentials.

### How does this project work?

- Based on the number of brokers to be proxies VLAN's are created
- The CF CLI is then used to tunnel remote CF app to VLAN's
- The kafka-proxy server is then used to proxy the VLAN connections to localhost

NOTE: Authentication is configured in the proxy server i.e. clients need not authenticate.

# Getting started

## Pre-requisites

1. Docker
2. vsCode IDE with Remote containers setup

## To run project

1. Open folder in remote container (in vsCode)
2. Modify config.yml file with appropriate details
3. (optional) Add OTP to `run.sh` file OR set it as an env variable
4. Execute `run.sh` script

Kafka ports will be available on localhost at ports 30000 up to 30005 (based on number of brokers in cluster). 
If you cluster has more ports to be exposed you need to add the same to `.devcontainer/devcontainer.json` > `forwardPorts` section.

## Based on

1. http://luckyabhishek.blogspot.com/2019/03/connecting-to-cloud-foundry-kafka.html
2. https://github.com/grepplabs/kafka-proxy
3. https://github.com/provectus/kafka-ui
