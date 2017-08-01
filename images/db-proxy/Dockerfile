# Stuck at Jessie for now, mysql-proxy is dead software :(
FROM debian:jessie

RUN apt-get update 
RUN apt-get install --yes --no-install-recommends \
    mysql-proxy \
    luarocks \
    libssl-dev \
    gcc \
    unzip

RUN luarocks install luacrypto
RUN luarocks install lua-cjson

ADD auth.lua /srv/auth.lua

CMD mysql-proxy \
    --plugins=proxy \
    --proxy-lua-script=/srv/auth.lua \
    --proxy-backend-addresses="${MYSQL_HOST}":3306 \
    --proxy-address=0.0.0.0:3306 \
    --proxy-skip-profiling
