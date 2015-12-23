FROM debian:jessie
RUN echo 'lol'
RUN apt-get update
RUN apt-get install --yes --no-install-recommends ca-certificates nodejs nodejs-legacy npm locales

RUN npm -g install configurable-http-proxy

# Setup the C.UTF-8 Locale, since otherwise it defaults to an ASCII one
RUN locale-gen C.UTF-8
ENV LC_ALL C.UTF-8

# HACK! HACK! HACK!
COPY passwd /etc/passwd

USER 52771

EXPOSE 8000
