FROM ubuntu:24.04

ENV PYWIKIBOT_VERSION=9.4.1
ENV EDITOR=/bin/nano
ENV PYWIKIBOT_DIR=/srv/paws
ENV DEBIAN_FRONTEND=noninteractive

## Begin minimal setup ##
# Use bash as default shell, rather than sh
ENV SHELL /bin/bash

# Set up user
ENV NB_USER tools.paws
ENV NB_UID 52771
ENV HOME /home/paws

RUN useradd \
    --uid ${NB_UID} \
    --home-dir ${HOME} \
    ${NB_USER}
WORKDIR ${HOME}

RUN apt-get update && \
    apt-get install --yes \
        python3-venv \
        pip \
        python3

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

# Create venv directory, and let users install into it
ENV VENV_DIR /srv/paws
RUN install -d -o ${NB_USER} -g ${NB_USER} ${VENV_DIR}

ENV PATH=/srv/paws/pwb:/srv/paws/bin:/srv/paws:$PATH

USER ${NB_USER}
RUN python3 -m venv /srv/paws
RUN pip --no-cache-dir install -U pip setuptools wheel

# Install base notebook packages
RUN pip install --prefix=/srv/paws --no-cache-dir \
    jupyterhub==4.1.1 \
    jupyterlab==4.2.5

## End minimal setup ##

USER root

# Base building utilities that'll always be required, probably
RUN apt-get update && \
    apt-get install --yes \
        git \
        locales \
        pkg-config \
        build-essential \
        gcc \
        apt-transport-https

RUN apt-get update --yes && \
    apt-get install --yes \
        python3-dev \
        openjdk-11-jdk

# Utilities
RUN apt-get install --yes \
        curl \
        wget \
        less \
        dnsutils \
        emacs \
        links \
        nano \
        vim \
        lsof \
        mariadb-client \
        unrar

RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
RUN apt-get install -y nodejs

# pyaudio
RUN apt-get install --yes \
        portaudio19-dev

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen

## Install R ##
# Use newer version of R
# Binary packages from packagemanager.rstudio.com work against this.
# Base R from Focal is only 3.6.
ADD r/cran.gpg /etc/apt/trusted.gpg.d/cran.gpg
ADD r/cran.list /etc/apt/sources.list.d/cran.list

# Install languages needed and their core dev packages
RUN apt-get update --yes && \
    apt-get install --yes \
        r-recommended \
        r-base-dev \
        r-cran-littler \
        git \
        curl \
        gdebi \
        # For R's mysql
        libmariadb-dev \
        # For R's curl
        libcurl4-openssl-dev \
        # for ipython kernels
        libzmq3-dev \
        # For R's devtools
        libssl-dev

# Install rstudio-server
ENV RSTUDIO_SERVER_URL https://download2.rstudio.org/server/jammy/amd64/rstudio-server-2023.12.1-402-amd64.deb
RUN curl --silent --location --fail ${RSTUDIO_SERVER_URL} > /tmp/rstudio-server.deb
RUN gdebi -n /tmp/rstudio-server.deb && rm /tmp/rstudio-server.deb


# Create user owned R libs dir
# This lets users temporarily install packages
ENV R_LIBS_USER /srv/r
RUN install -d -o ${NB_USER} -g ${NB_USER} ${R_LIBS_USER}

# R_LIBS_USER is set by default in /etc/R/Renviron, which RStudio loads.
# We uncomment the default, and set what we wanna - so it picks up
# the packages we install. Without this, RStudio doesn't see the packages
# that R does.
# Stolen from https://github.com/jupyterhub/repo2docker/blob/6a07a48b2df48168685bb0f993d2a12bd86e23bf/repo2docker/buildpacks/r.py
RUN sed -i -e '/^R_LIBS_USER=/s/^/#/' /etc/R/Renviron && \
    echo "R_LIBS_USER=${R_LIBS_USER}" >> /etc/R/Renviron

USER ${NB_USER}
RUN pip install --no-cache-dir \
    jupyter-server-proxy \
    jupyter-rsession-proxy

# Set CRAN mirror to rspm before we install anything
COPY r/Rprofile.site /usr/lib/R/etc/Rprofile.site
# RStudio needs its own config
COPY r/rsession.conf /etc/rstudio/rsession.conf

USER root
# Install the R Kernel
RUN r -e "install.packages('IRkernel', version='1.3.2')" && \
    r -e "IRkernel::installspec(prefix='${VENV_DIR}')" && \
    rm -rf /tmp/downloaded_packages

## Done installing R

USER root

## Setup OpenRefine
ENV OPENREFINE_DIR /srv/openrefine
ENV PATH=$PATH:$OPENREFINE_DIR
RUN mkdir -p ${OPENREFINE_DIR} && cd ${OPENREFINE_DIR} && \
    curl -L 'https://github.com/OpenRefine/OpenRefine/releases/download/3.8.2/openrefine-linux-3.8.2.tar.gz' | tar xzf - --strip=1

USER root
RUN apt-get install --yes unzip

USER ${NB_USER}
ENV REFINE_DIR /home/paws
RUN pip install --no-cache-dir nb_serverproxy_openrefine

USER root
RUN wget https://github.com/OpenRefine/CommonsExtension/releases/download/v0.1.2/openrefine-commons.zip -O /tmp/openrefine-commonsextension.zip
RUN unzip /tmp/openrefine-commonsextension.zip -d ${OPENREFINE_DIR}/webapp/extensions/

## Done setting up OpenRefine

## install quarto

USER root
RUN wget https://github.com/quarto-dev/quarto-cli/releases/download/v1.4.554/quarto-1.4.554-linux-amd64.deb -O /tmp/quarto.deb
RUN dpkg -i /tmp/quarto.deb

## done install quarto

USER root

RUN npm install -g wikibase-cli

# Machine-learning type stuff
RUN apt-get update && \
    apt-get install --yes \
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
    # For PDFs and stuff
    pandoc \
    texlive-xetex


## Install Julia
# Install Julia directories and depot path

ENV PATH=$PATH:/srv/julia/bin
ENV JULIA_DEPOT_PATH /srv/julia-depot/
RUN install -d -o ${NB_USER} -g ${NB_USER} /srv/julia
RUN install -d -o ${NB_USER} -g ${NB_USER} ${JULIA_DEPOT_PATH}

USER ${NB_USER}

# install julia and julia kernel
COPY install-julia /tmp/install-julia
RUN /tmp/install-julia

## Done Installing Julia

# install sql access tool
COPY install-sql-tool /tmp/install-sql-tool
RUN /tmp/install-sql-tool

## Done installing sql access tool

# Install the bash kernel
RUN pip install bash_kernel
RUN python -m bash_kernel.install --sys-prefix

# Install mass amount of python libraries!
COPY --chown=tools.paws:tools.paws requirements.txt /tmp/requirements.txt

RUN pip --no-cache-dir install -r /tmp/requirements.txt

# Install pywikibot
RUN git clone \
    --branch $PYWIKIBOT_VERSION \
    --depth 1 \
    --recurse-submodules \
    --shallow-submodules \
    https://gerrit.wikimedia.org/r/pywikibot/core.git \
    /srv/paws/pwb
RUN pip install --no-cache-dir \
    /srv/paws/pwb[eventstreams,graphviz,google,isbn,memento,mysql,mwoauth,html]
COPY --chown=tools.paws:tools.paws user-config.py /srv/paws/
COPY --chown=tools.paws:tools.paws user-fixes.py /srv/paws/


COPY install-extensions /usr/local/bin/
RUN /usr/local/bin/install-extensions

COPY banner /etc/bash.bashrc

# use custom css to hide clusters tab
COPY --chown=tools.paws:tools.paws hide_clusters_tab.css /home/paws/.jupyter/custom/custom.css

EXPOSE 8888
