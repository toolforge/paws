FROM ubuntu:22.04

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    curl \
    ca-certificates

COPY . /paws
WORKDIR /paws

RUN curl -Lf https://github.com/instrumenta/kubeval/releases/download/0.15.0/kubeval-linux-amd64.tar.gz | tar xzf -
RUN chmod +x kubeval
ENV KUBERNETES_VERSION=1.16.0

ENTRYPOINT ["sh", "-c", "./kubeval -v $KUBERNETES_VERSION --strict manifests/*"]
