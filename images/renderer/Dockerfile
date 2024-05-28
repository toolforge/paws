FROM ubuntu:24.04

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    uwsgi \
    uwsgi-plugin-python3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt

# We don't care about breaking system packages since this is a container
RUN pip3 --no-cache-dir install --break-system-packages -r /tmp/requirements.txt

# something about the --no-cache-dir keeps pyrsistent from visibly installing
RUN pip3 install --break-system-packages pyrsistent

COPY renderer.py /srv/renderer.py
COPY basic.tpl /srv/basic.tpl
COPY full.tpl /srv/full.tpl

WORKDIR /srv

CMD /usr/bin/uwsgi \
    --plugins python3 \
    --socket 0.0.0.0:8000 \
    --wsgi-file /srv/renderer.py \
    --master \
    --processes 4 \
    --die-on-term
