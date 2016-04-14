FROM docker-registry.tools.wmflabs.org/jessie-wikimedia

RUN apt-get update
RUN apt-get install --yes --no-install-recommends nginx-extras luarocks

RUN luarocks install lua-resty-http
RUN luarocks install lua-cjson

COPY nginx.conf /srv/nginx.conf

EXPOSE 8080

CMD /usr/sbin/nginx -c /srv/nginx.conf
