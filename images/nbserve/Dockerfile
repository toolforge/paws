FROM docker-registry.tools.wmflabs.org/toolforge-buster-sssd

RUN DEBIAN_FRONTEND=noninteractive apt-get update \
    && DEBIAN_FRONTEND=noninteractive \
    apt-get install --yes --no-install-recommends \
        build-essential \
        libnginx-mod-http-lua \
        luarocks \
        nginx-extras \
        python3 \
        unzip \
    && DEBIAN_FRONTEND=noninteractive apt-get autoremove --yes \
    && DEBIAN_FRONTEND=noninteractive apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN luarocks install lua-resty-http
RUN luarocks install lua-cjson

COPY nginx.py /srv/nginx.py

EXPOSE 8080

CMD ["/usr/bin/python3", "/srv/nginx.py"]
