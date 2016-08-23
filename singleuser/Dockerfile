FROM docker-registry.tools.wmflabs.org/toollabs-base

MAINTAINER Yuvi Panda <yuvipanda@riseup,net>

ENV HOME=/home/paws
ENV USER=tools.paws
ENV SHELL=/bin/bash
ENV EDITOR=/bin/nano
ENV PYWIKIBOT2_DIR=/srv/paws


# Create and setup temporary home. This will be overmounted on for PAWS,
# but is useful for things that write stuff to $HOME when building
RUN mkdir -p /home/paws
RUN chown 52771:52771 /home/paws
WORKDIR /home/paws

# Add the R debian repo
RUN apt-key adv --keyserver keys.gnupg.net --recv-key 381BA480
RUN echo 'deb http://cran.us.r-project.org/bin/linux/debian jessie-cran3/' >> /etc/apt/sources.list

RUN apt-get update --yes

# Base building utilities that'll always be required, probably
RUN apt-get install --yes --no-install-recommends \
        git \
        locales \
        pkg-config \
        build-essential \
        gcc

# Setup the C.UTF-8 Locale, since otherwise it defaults to an ASCII one
RUN locale-gen C.UTF-8
ENV LC_ALL C.UTF-8

# Install languages needed and their core dev packages
RUN apt-get install --yes --no-install-recommends \
        python3.4 \
        python3.4-dev \
        virtualenv \
        r-recommended \
        r-base-dev

# Utilities
RUN apt-get install --yes --no-install-recommends \
        curl \
        wget \
        less \
        dnsutils \
        emacs \
        links \
        nano \
        vim \
        mariadb-client

# Machine-learning type stuff
RUN apt-get install --yes \
    # For scipy & friends
    libblas-dev \
    liblapack-dev \
    libquadmath0 \
    gfortran \
    # for lxml
    libxml2-dev \
    libxslt1-dev \
    # for matplotlib
    libfreetype6-dev \
    libpng-dev \
    # for ipython kernels
    libzmq3-dev \
    libreadline-dev \
    # For R's mysql
    libmariadb-client-lgpl-dev \
    # For R's curl
    libcurl4-openssl-dev

RUN mkdir -p /srv/paws && chown 52771:52771 /srv/paws
ENV PATH=/srv/paws/pwb:/srv/paws/bin:/srv/paws:$PATH

RUN virtualenv -p python3 /srv/paws

# Upgrade pip to latest, unconditionally.
RUN /srv/paws/bin/pip install -U pip

# Install mass amount of python libraries!
COPY requirements.txt /tmp/requirements.txt
RUN /srv/paws/bin/pip --no-cache-dir install -r /tmp/requirements.txt

# Install the bash kernel
RUN /srv/paws/bin/python -m bash_kernel.install

# Install the R Kernel and libraries
COPY install-r /usr/local/bin/install-r
RUN /usr/local/bin/install-r

# Install pywikibot
RUN git clone --recursive https://gerrit.wikimedia.org/r/pywikibot/core.git /srv/paws/pwb
COPY user-config.py /srv/paws/
COPY user-fixes.py /srv/paws/
COPY install-pwb /usr/local/bin/
RUN /usr/local/bin/install-pwb

COPY install-extensions /usr/local/bin/
RUN /usr/local/bin/install-extensions

RUN chown -R 52771:52771 /srv/paws
# Allow people to install their own R libraries
RUN chown -R 52771:52771 /usr/local/lib/R/site-library

COPY banner /etc/bash.bashrc

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
