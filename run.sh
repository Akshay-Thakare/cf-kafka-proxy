
# if CF is protected with 2FA (SSO login not supported by script)
export CF_OTP=445644

# Kill old processes
pkill -f cf
pkill -f kafka

# start proxy server
poetry install
poetry run python main.py &

# start kafka management ui
export KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS=localhost:30000
java -jar kafka-ui-api-0.3.1.jar
