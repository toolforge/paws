FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    libgd-dev \
    libpcre3-dev \
    libssl-dev \
    luarocks \
    make \
    perl \
    unzip \
    ca-certificates \
    git \
    libxml2-dev \
    libxslt1-dev \
    python3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ARG RESTY_VERSION="1.17.8.2"
ARG RESTY_J="1"
# ARG RESTY_OPENSSL_VERSION="1.1.1d"
ARG RESTY_CONFIG_OPTIONS="\
    --with-compat \
    --with-file-aio \
    --with-http_addition_module \
    --with-http_auth_request_module \
    --with-http_dav_module \
    --with-http_flv_module \
    --with-http_gunzip_module \
    --with-http_gzip_static_module \
    --with-http_image_filter_module=dynamic \
    --with-http_mp4_module \
    --with-http_random_index_module \
    --with-http_realip_module \
    --with-http_secure_link_module \
    --with-http_slice_module \
    --with-http_ssl_module \
    --with-http_stub_status_module \
    --with-http_sub_module \
    --with-http_v2_module \
    --with-http_xslt_module=dynamic \
    --with-ipv6 \
    --with-mail \
    --with-mail_ssl_module \
    --with-md5-asm \
    --with-pcre-jit \
    --with-sha1-asm \
    --with-stream \
    --with-stream_ssl_module \
    --with-threads \
    --add-module=./ngx-fancyindex \
    "

RUN cd /tmp \
    && curl -fSL https://openresty.org/download/openresty-${RESTY_VERSION}.tar.gz -o openresty-${RESTY_VERSION}.tar.gz \
    && tar xzf openresty-${RESTY_VERSION}.tar.gz \
    && cd /tmp/openresty-${RESTY_VERSION} \
    && git clone https://github.com/aperezdc/ngx-fancyindex \
    && eval ./configure -j${RESTY_J} ${RESTY_CONFIG_OPTIONS} \
    && make -j${RESTY_J} \
    && make -j${RESTY_J} install \
    && cd /tmp \
    && rm -rf \
    openresty-${RESTY_VERSION}.tar.gz openresty-${RESTY_VERSION} \
    && mkdir -p /var/run/openresty

RUN ln -sf /dev/stdout /usr/local/openresty/nginx/logs/access.log
RUN ln -sf /dev/stderr /usr/local/openresty/nginx/logs/error.log

# Add additional binaries into PATH for convenience
ENV PATH=$PATH:/usr/local/openresty/luajit/bin:/usr/local/openresty/nginx/sbin:/usr/local/openresty/bin

RUN luarocks install lua-resty-http
RUN luarocks install lua-cjson

RUN apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY nginx.py /srv/nginx.py

EXPOSE 8000

CMD ["/usr/bin/python3", "/srv/nginx.py"]

# Use SIGQUIT instead of default SIGTERM to cleanly drain requests
# See https://github.com/openresty/docker-openresty/blob/master/README.md#tips--pitfalls
STOPSIGNAL SIGQUIT
