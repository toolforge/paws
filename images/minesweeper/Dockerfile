FROM alpine:3.15

RUN apk add --no-cache procps python3 py3-pip py3-psutil
RUN python3 -mpip install --no-cache --upgrade pip
COPY requirements.txt /tmp/requirements.txt
RUN python3 -mpip install --no-cache -r /tmp/requirements.txt

# always!
ENV PYTHONUNBUFFERED=1
