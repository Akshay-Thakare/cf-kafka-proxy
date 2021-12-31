# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.209.6/containers/ubuntu/.devcontainer/base.Dockerfile

# [Choice] Ubuntu version (use hirsuite or bionic on local arm64/Apple Silicon): hirsute, focal, bionic
ARG VARIANT="hirsute"
FROM mcr.microsoft.com/vscode/devcontainers/base:0-${VARIANT}

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>

RUN apt-get update -y \
    && apt install python3.8-venv -y \
    && curl -sSL https://install.python-poetry.org | python3 -

COPY binaries/cf8-cli_8/cf /usr/bin/cf
COPY binaries/cf8-cli_8/cf8 /usr/bin/cf8
COPY binaries/kafka-proxy-v3/kafka-proxy /usr/bin/kafka-proxy

RUN chmod +x /usr/bin/cf
RUN chmod +x /usr/bin/cf8
RUN chmod +x /usr/bin/kafka-proxy

RUN apt-get install openjdk-17-jdk -y
