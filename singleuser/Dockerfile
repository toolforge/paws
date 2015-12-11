FROM debian:jessie

MAINTAINER Yuvi Panda <yuvipanda@riseup,net>

RUN apt-get update
RUN apt-get install --yes \
        python3.4 \
        git \
        python3.4-dev \
        virtualenv \
        locales \
        build-essential \
        gcc

# Utilities
RUN apt-get install --yes \
        curl \
        dnsutils \
        emacs \
        nano \
        vim

# Setup the C.UTF-8 Locale, since otherwise it defaults to an ASCII one
RUN locale-gen C.UTF-8
ENV LC_ALL C.UTF-8

RUN  mkdir -p /srv/pwb && chown 52771:52771 /srv/pwb

# HACK! HACK! HACK!
COPY passwd /etc/passwd

RUN mkdir -p /srv/pwb


RUN git clone --recursive https://gerrit.wikimedia.org/r/pywikibot/core.git /srv/pwb
ADD user-config.py /srv/pwb/
ADD install-pwb /usr/local/bin

RUN /usr/local/bin/install-pwb

# MW related libraries
RUN /srv/pwb/bin/pip install \
    python-mwapi \
    mwdb \
    mwxml

RUN /srv/pwb/bin/pip install jupyterhub ipython[notebook] bash_kernel
RUN /srv/pwb/bin/pip install /srv/pwb/

# Install the bash kernel
RUN /srv/pwb/bin/python -m bash_kernel.install

RUN mkdir -p /home/paws
RUN chown 52771:52771 /home/paws

ENV HOME=/home/paws
ENV USER=tools.paws
ENV PATH=/srv/pwb/bin:/srv/pwb:$PATH
ENV SHELL=/bin/bash
ENV PYWIKIBOT2_DIR=/srv/pwb

WORKDIR /home/paws

ADD banner /etc/bash.bashrc

RUN chown 52771:52771 /srv/pwb
USER 52771

EXPOSE 8888

CMD jupyterhub-singleuser \
  --port=8888 \
  --ip=0.0.0.0 \
  --user=$JPY_USER \
  --cookie-name=$JPY_COOKIE_NAME \
  --base-url=$JPY_BASE_URL \
  --hub-prefix=$JPY_HUB_PREFIX \
  --hub-api-url=$JPY_HUB_API_URL
