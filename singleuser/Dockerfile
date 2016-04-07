FROM tools-docker-registry.wmflabs.org/jessie-wikimedia

MAINTAINER Yuvi Panda <yuvipanda@riseup,net>

# Add the R debian repo
RUN apt-key adv --keyserver keys.gnupg.net --recv-key 381BA480
RUN echo 'deb http://cran.us.r-project.org/bin/linux/debian jessie-cran3/' >> /etc/apt/sources.list

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
        libreadline-dev \
        libxml2-dev \
        libxslt1-dev

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

# Machine-learning type stuff
RUN apt-get install --yes \
    libblas3 \
    libblas-dev \
    liblapack3 \
    liblapack-dev \
    libquadmath0 \
    gfortran

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

COPY requirements.txt /tmp/requirements.txt
RUN /srv/paws/bin/pip --no-cache-dir install -r /tmp/requirements.txt

RUN /srv/paws/bin/pip --no-cache-dir install /srv/paws/

# Install the bash kernel
RUN /srv/paws/bin/python -m bash_kernel.install

RUN mkdir -p /home/paws
RUN chown 52771:52771 /home/paws


# Setup R packages
RUN apt-get install --yes --no-install-recommends \
    r-recommended \
    r-base-dev

COPY install-r /usr/local/bin/install-r
RUN /usr/local/bin/install-r

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
