FROM debian:jessie

RUN apt-get update
RUN apt-get install --yes --no-install-recommends lighttpd

COPY lighttpd.conf /srv/lighttpd.conf

EXPOSE 8000

CMD /usr/sbin/lighttpd -f /srv/lighttpd.conf -D
