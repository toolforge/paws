FROM docker-registry.tools.wmflabs.org/jessie-toollabs

RUN echo lol
RUN echo 'deb http://ftp.debian.org/debian jessie-backports main' >> /etc/apt/sources.list

RUN apt-get update
RUN apt-get install --yes --no-install-recommends -t jessie-backports \
            nginx-extras \
            luarocks \
            unzip \
            build-essential

RUN luarocks install lua-resty-http
RUN luarocks install lua-cjson

COPY nginx.py /srv/nginx.py

EXPOSE 8080

CMD /usr/bin/python /srv/nginx.py
