FROM alpine:3.20.0

RUN apk add --no-cache procps python3 py3-pip py3-psutil nfs-utils util-linux kmod
RUN python3 -mpip install --break-system-packages --no-cache --upgrade pip
COPY requirements.txt /tmp/requirements.txt
RUN python3 -mpip install --break-system-packages --no-cache -r /tmp/requirements.txt

ENV PYTHONUNBUFFERED=1
