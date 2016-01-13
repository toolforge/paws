FROM debian:jessie

MAINTAINER Yuvi Panda <yuvipanda@riseup,net>

RUN apt-get update --yes

# Matplotlib needs freetype, png and pkg-config
RUN apt-get install --yes --no-install-recommends \
        python3.4 \
        git \
        python3.4-dev \
        virtualenv \
        locales \
        pkg-config \
        build-essential \
        gcc \
        libfreetype6-dev \
        libpng-dev \
        libzmq3-dev \
        libreadline-dev

# Utilities
RUN apt-get install --yes --no-install-recommends \
        curl \
        dnsutils \
        emacs \
        links \
        nano \
        vim

# Setup the C.UTF-8 Locale, since otherwise it defaults to an ASCII one
RUN locale-gen C.UTF-8
ENV LC_ALL C.UTF-8

RUN  mkdir -p /srv/paws && chown 52771:52771 /srv/paws

# HACK! HACK! HACK!
COPY passwd /etc/passwd

RUN mkdir -p /srv/paws


RUN git clone --recursive https://gerrit.wikimedia.org/r/pywikibot/core.git /srv/paws
COPY user-config.py /srv/paws/
COPY user-fixes.py /srv/paws/

COPY install-pwb /usr/local/bin/

RUN /usr/local/bin/install-pwb

# MW related libraries
RUN /srv/paws/bin/pip install \
    mwapi \
    mwdb \
    mwxml \
    mwreverts \
    mwsessions \
    mwdiffs \
    mwoauth \
    mwtypes \
    mwpersistence

# Visualization libraries
RUN /srv/paws/bin/pip install \
    bokeh \
    ipywidgets \
    matplotlib

RUN /srv/paws/bin/pip install jupyterhub ipython[notebook] bash_kernel
RUN /srv/paws/bin/pip install /srv/paws/
RUN /srv/paws/bin/pip install git+https://github.com/yuvipanda/python-wdqs.git

# Install the bash kernel
RUN /srv/paws/bin/python -m bash_kernel.install

RUN mkdir -p /home/paws
RUN chown 52771:52771 /home/paws

ENV HOME=/home/paws
ENV USER=tools.paws
ENV PATH=/srv/paws/bin:/srv/paws:$PATH
ENV SHELL=/bin/bash
ENV PYWIKIBOT2_DIR=/srv/paws

# Setup R packages
RUN apt-get install --yes --no-install-recommends \
    r-recommended \
    r-base-dev

COPY install-r /usr/local/bin/install-r
RUN /usr/local/bin/install-r

RUN /srv/paws/bin/pip install rpy2

WORKDIR /home/paws

COPY banner /etc/bash.bashrc

RUN chown -R 52771:52771 /srv/paws
USER 52771

EXPOSE 8888

CMD jupyterhub-singleuser \
  --port=8888 \
  --ip=0.0.0.0 \
  --user="$JPY_USER" \
  --cookie-name=$JPY_COOKIE_NAME \
  --base-url=$JPY_BASE_URL \
  --hub-prefix=$JPY_HUB_PREFIX \
  --hub-api-url=$JPY_HUB_API_URL
