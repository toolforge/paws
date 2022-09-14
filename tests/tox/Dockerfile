FROM ubuntu:22.04

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    tox

COPY . /paws
WORKDIR /paws


ENTRYPOINT ["tox"]
