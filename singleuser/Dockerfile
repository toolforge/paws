FROM tools-docker-registry.wmflabs.org/jessie-wikimedia

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
        wget \
        dnsutils \
        emacs \
        links \
        nano \
        vim \
        mariadb-client

# Setup the C.UTF-8 Locale, since otherwise it defaults to an ASCII one
RUN locale-gen C.UTF-8
ENV LC_ALL C.UTF-8

RUN  mkdir -p /srv/paws && chown 52771:52771 /srv/paws
ENV PATH=/srv/paws/bin:/srv/paws:$PATH

# HACK! HACK! HACK!
RUN echo 'tools.paws:x:52771:52771:tools.paws:/home/paws:/bin/bash' >> /etc/passwd


RUN git clone --recursive https://gerrit.wikimedia.org/r/pywikibot/core.git /srv/paws
COPY user-config.py /srv/paws/
COPY user-fixes.py /srv/paws/

COPY install-pwb /usr/local/bin/

RUN /usr/local/bin/install-pwb

# MW related libraries
RUN /srv/paws/bin/pip --no-cache-dir install \
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
RUN /srv/paws/bin/pip3 --no-cache-dir install \
    bokeh \
    ipywidgets \
    matplotlib \
    pandas

# DB access
RUN /srv/paws/bin/pip3 --no-cache-dir install \
    mycli

# Machine-learning type stuff
RUN apt-get install --yes \
    libblas3 \
    libblas-dev \
    liblapack3 \
    liblapack-dev \
    libquadmath0 \
    gfortran

RUN /srv/paws/bin/pip --no-cache-dir install \
    revscoring \
    editquality \
    wikiclass \
    scikit-neuralnetwork

RUN /srv/paws/bin/pip --no-cache-dir install jupyterhub ipython[notebook] bash_kernel
RUN /srv/paws/bin/pip --no-cache-dir install /srv/paws/
RUN /srv/paws/bin/pip --no-cache-dir install git+https://github.com/yuvipanda/python-wdqs.git

# Install the bash kernel
RUN /srv/paws/bin/python -m bash_kernel.install

RUN mkdir -p /home/paws
RUN chown 52771:52771 /home/paws


# Setup R packages
RUN apt-get install --yes --no-install-recommends \
    r-recommended \
    r-base-dev \
    r-cran-ggplot2 \
    r-cran-rmysql

COPY install-r /usr/local/bin/install-r
RUN /usr/local/bin/install-r

RUN /srv/paws/bin/pip --no-cache-dir install rpy2

WORKDIR /home/paws

COPY banner /etc/bash.bashrc

ENV HOME=/home/paws
ENV USER=tools.paws
ENV SHELL=/bin/bash
ENV PYWIKIBOT2_DIR=/srv/paws

RUN chown -R 52771:52771 /srv/paws
RUN chown -R 52771:52771 /usr/local/lib/R/site-library

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
