FROM docker-registry.tools.wmflabs.org/toolforge-python37-sssd-web

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install \
    python3-pip \
    python3-setuptools \
    python3-wheel\
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install git+https://github.com/jupyter/nbconvert.git ipython werkzeug
RUN pip install git+https://github.com/Python-Markdown/markdown.git
RUN pip install docutils

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
