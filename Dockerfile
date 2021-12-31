FROM grepplabs/kafka-proxy:v0.3.0
LABEL author=akshay.thakare.india@gmail.com

# Add vlan packages
RUN apk update \
    && apk add --no-cache vlan \
    && apk add --no-cache curl \
    && apk add --no-cache python3 \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -

ENV PATH="${PATH}:/root/.poetry/bin"

# Add CF ClI v8 binaries
# https://packages.cloudfoundry.org/stable?release=linux64-binary&version=8.0.0&source=github-rel
COPY .devcontainer/binaries/cf8-cli_8/cf /usr/bin/cf
COPY .devcontainer/binaries/cf8-cli_8/cf8 /usr/bin/cf8
RUN chmod +x /usr/bin/cf
RUN chmod +x /usr/bin/cf8

# Add kafka proxy binaries
# https://github.com/grepplabs/kafka-proxy/releases/download/v0.3.0/kafka-proxy-v0.3.0-linux-amd64.tar.gz
RUN cp /opt/kafka-proxy/bin/kafka-proxy /usr/bin/kafka-proxy

# Copy python project file
COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml

# install python project dependencies
RUN poetry install

# Copying python code later for faster builds
RUN mkdir /config
COPY main.py main.py

# poetry run python main.py
# To be changed to python script
#ENTRYPOINT ["tail", "-f", "/dev/null"]
ENTRYPOINT ["poetry", "run", "python", "main.py"]
