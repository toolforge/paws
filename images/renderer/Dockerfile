FROM docker-registry.tools.wmflabs.org/jessie-toollabs

RUN apt-get install --yes --no-install-recommends \
        python3 \
        python3-pip \
        uwsgi-plugin-python3 \
        git

RUN pip3 install git+https://github.com/jupyter/nbconvert.git ipython werkzeug

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
