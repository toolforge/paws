FROM alpine:3.12

RUN apk --no-cache add curl jq

COPY install-oauth.sh /opt/install-oauth.sh
COPY hack-localsettings.sh /opt/hack-localsettings.sh

RUN chmod a+x /opt/install-oauth.sh
RUN chmod a+x /opt/hack-localsettings.sh

WORKDIR /opt/mediawiki
