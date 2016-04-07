FROM docker-registry.tools.wmflabs.org/jessie-wikimedia

RUN apt-get update

# npm is needed because we're installing jupyter from git, which requires it
# We can toss it once we go back to using pip
RUN apt-get install --yes --no-install-recommends \
    python3 \
    ca-certificates \
    git \
    locales \
    nodejs-legacy \
    npm \
    python3-pip

# Setup the C.UTF-8 Locale, since otherwise it defaults to an ASCII one
RUN locale-gen C.UTF-8
ENV LC_ALL C.UTF-8

RUN npm install -g git+https://github.com/jupyter/configurable-http-proxy.git#master

# HACK! HACK! HACK!
RUN echo 'tools.paws:x:52771:52771:tools.paws:/home/paws:/bin/bash' >> /etc/passwd

COPY requirements.txt /srv/jupyterhub/requirements.txt
RUN pip3 install -r  /srv/jupyterhub/requirements.txt

# Needed for kubespawner
COPY jupyterhub_config.py /srv/jupyterhub/

# Fuck you too, Docker? https://github.com/docker/docker/issues/6119
RUN chown -R 52771:52771 /srv/jupyterhub

USER 52771

EXPOSE 8000

CMD /usr/local/bin/jupyterhub --config /srv/jupyterhub/jupyterhub_config.py --no-ssl
