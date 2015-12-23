FROM debian:jessie

RUN apt-get update
RUN apt-get install -y python3 virtualenv ca-certificates nodejs nodejs-legacy npm git locales

RUN npm -g install configurable-http-proxy

# Setup the C.UTF-8 Locale, since otherwise it defaults to an ASCII one
RUN locale-gen C.UTF-8
ENV LC_ALL C.UTF-8

# HACK! HACK! HACK!
COPY passwd /etc/passwd

RUN virtualenv -p python3 /srv/jupyterhub
WORKDIR /srv/jupyterhub

COPY requirements.txt /srv/jupyterhub
RUN /srv/jupyterhub/bin/pip install -r  /srv/jupyterhub/requirements.txt

# Needed for kubespawner
ENV PYTHONPATH=.:$PYTHONPATH

COPY kubespawner/kubespawner /srv/jupyterhub/kubespawner
COPY jupyterhub_config.py /srv/jupyterhub/

# Fuck you too, Docker? https://github.com/docker/docker/issues/6119
RUN chown -R 52771:52771 /srv/jupyterhub
USER 52771

EXPOSE 8000

CMD /srv/jupyterhub/bin/jupyterhub --config /srv/jupyterhub/jupyterhub_config.py
