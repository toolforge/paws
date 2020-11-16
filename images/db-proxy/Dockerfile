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
RUN luarocks install luasocket

ADD auth.lua /srv/auth.lua

CMD mysql-proxy \
    --plugins=proxy \
    --proxy-lua-script=/srv/auth.lua \
    --proxy-backend-addresses="${SEC1_HOST}":3306 \
    --proxy-backend-addresses="${SEC2_HOST}":3306 \
    --proxy-backend-addresses="${SEC3_HOST}":3306 \
    --proxy-backend-addresses="${SEC4_HOST}":3306 \
    --proxy-backend-addresses="${SEC5_HOST}":3306 \
    --proxy-backend-addresses="${SEC6_HOST}":3306 \
    --proxy-backend-addresses="${SEC7_HOST}":3306 \
    --proxy-backend-addresses="${SEC8_HOST}":3306 \
    --proxy-address=0.0.0.0:3306 \
    --proxy-skip-profiling
