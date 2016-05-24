FROM docker-registry.tools.wmflabs.org/jessie-toollabs

RUN apt-get install --yes --no-install-recommends \
    ca-certificates \
    locales \
    nodejs-legacy \
    npm \
    git

# Setup the C.UTF-8 Locale, since otherwise it defaults to an ASCII one
RUN locale-gen C.UTF-8
ENV LC_ALL C.UTF-8

#RUN npm install -g configurable-http-proxy
RUN npm install -g git+https://github.com/jupyter/configurable-http-proxy.git#master

EXPOSE 8000

RUN apt-get install --yes curl
CMD /usr/local/bin/configurable-http-proxy --ip 0.0.0.0 --port 8000 --api-ip 0.0.0.0 --api-port 8001 --error-target http://${HUB_SERVICE_HOST}:${HUB_SERVICE_PORT}/paws/error --default-target http://${HUB_SERVICE_HOST}:${HUB_SERVICE_PORT}  --log-level debug
