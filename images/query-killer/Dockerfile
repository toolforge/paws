FROM ubuntu:17.10

RUN apt-get update && \
    apt-get install --yes --no-install-recommends \
    percona-toolkit ca-certificates

CMD pt-kill \
    --busy-time "${MAX_QUERY_TIME}" \
    --interval 60 \
    --user "${MYSQL_USERNAME}" \
    --password "${MYSQL_PASSWORD}" \
    --host "${MYSQL_HOST}" \
    --kill \
    --print
