FROM docker-registry.tools.wmflabs.org/jessie-wikimedia

RUN apt-get update

RUN apt-get install --yes --no-install-recommends \
        python3 \
        python3-pip \
        uwsgi-plugin-python3

RUN pip3 install nbconvert ipython

ADD renderer.py /srv/renderer.py

CMD /usr/bin/uwsgi \
    --plugins python3 \
    --socket 0.0.0.0:8000 \
    --wsgi-file /srv/renderer.py \
    --master \
    --processes 4 \
    --die-on-term
