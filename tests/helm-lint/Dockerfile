FROM ubuntu:22.04

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    curl \
    ca-certificates

COPY . /paws
WORKDIR /paws

RUN curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
RUN helm repo add jupyterhub https://jupyterhub.github.io/helm-chart/
RUN helm repo add bitnami https://charts.bitnami.com/bitnami
RUN helm dependency update paws/


ENTRYPOINT ["helm", "lint", "paws/"]
