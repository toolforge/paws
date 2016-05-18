FROM docker-registry.tools.wmflabs.org/jessie-toollabs

RUN apt-get install --yes --no-install-recommends \
    percona-toolkit

CMD pt-kill \
    --busy-time 1800 \
    --interval 60 \
    --user "${MYSQL_USERNAME}" \
    --password "${MYSQL_PASSWORD}" \
    --host "${MYSQL_HOST}" \
    --kill \
    --print
