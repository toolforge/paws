FROM ubuntu:22.04

ENV PYWIKIBOT_VERSION=7.4.0
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

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    --home ${HOME} \
    --force-badname \
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

ENV PATH=/srv/paws/pwb:/srv/paws/bin:/srv/paws:/srv/julia/bin:$PATH

USER ${NB_USER}
RUN python3 -m venv /srv/paws
RUN pip --no-cache-dir install -U pip setuptools wheel

# Install base notebook packages
RUN pip install --prefix=/srv/paws --no-cache-dir \
    jupyterhub==2.3.0 \
    jupyterlab==3.3.4

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
        openjdk-11-jdk \
        nodejs

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
        mariadb-client

# pyaudio
RUN apt-get install --yes \
        portaudio19-dev

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen

# Setup nodesource, because node on Ubuntu is far too old to be useful
ADD node/nodesource.gpg.key /etc/apt/trusted.gpg.d/nodesource.gpg.key
ADD node/nodesource.list /etc/apt/sources.list.d/nodesource.list
RUN apt-key add /etc/apt/trusted.gpg.d/nodesource.gpg.key

## Install R ##
# Use newer version of R
# Binary packages from packagemanager.rstudio.com work against this.
# Base R from Focal is only 3.6.
COPY E298A3A825C0D65DFD57CBB651716619E084DAB9.asc /tmp/
RUN apt-key add /tmp/E298A3A825C0D65DFD57CBB651716619E084DAB9.asc && rm /tmp/E298A3A825C0D65DFD57CBB651716619E084DAB9.asc
RUN echo "deb https://cloud.r-project.org/bin/linux/ubuntu jammy-cran40/" > /etc/apt/sources.list.d/cran.list

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

# Install RStudio
# give access to libssl1.1 for rstudio-server
RUN echo "deb http://archive.ubuntu.com/ubuntu/ focal main restricted" > /etc/apt/sources.list.d/focal.list
RUN apt-get update

ENV RSTUDIO_SERVER_URL https://download2.rstudio.org/server/bionic/amd64/rstudio-server-2022.02.3-492-amd64.deb
RUN curl --silent --location --fail ${RSTUDIO_SERVER_URL} > /tmp/rstudio-server.deb
RUN gdebi -n /tmp/rstudio-server.deb && rm /tmp/rstudio-server.deb
# remove focal repo
RUN rm /etc/apt/sources.list.d/focal.list && apt-get update


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
    git+https://github.com/toolforge/jupyter-rsession-proxy.git@57d89b4

# Set CRAN mirror to rspm before we install anything
COPY Rprofile.site /usr/lib/R/etc/Rprofile.site
# RStudio needs its own config
COPY rsession.conf /etc/rstudio/rsession.conf

# Install the R Kernel
RUN r -e "install.packages('IRkernel', version='1.1.1')" && \
    r -e "IRkernel::installspec(prefix='${VENV_DIR}')" && \
    rm -rf /tmp/downloaded_packages

## Done installing R


USER root
# Setup OpenRefine
ENV OPENREFINE_DIR /srv/openrefine
RUN mkdir -p ${OPENREFINE_DIR} && cd ${OPENREFINE_DIR} && \
    curl -L https://github.com/OpenRefine/OpenRefine/releases/download/3.5.2/openrefine-linux-3.5.2.tar.gz | tar xzf - --strip=1
COPY proxies/openrefine-logo.svg ${OPENREFINE_DIR}/openrefine-logo.svg

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


# Install Julia directories and depot path
ENV JULIA_DEPOT_PATH /srv/julia-depot/
RUN install -d -o ${NB_USER} -g ${NB_USER} /srv/julia
RUN install -d -o ${NB_USER} -g ${NB_USER} ${JULIA_DEPOT_PATH}

USER ${NB_USER}
RUN pip install --no-cache-dir \
    retrolab \
    jupyterlab-link-share>=0.2.4 \
    nbgitpuller==0.9.0 \
    voila \
    bash_kernel

# Install the bash kernel
RUN python -m bash_kernel.install --sys-prefix



# Install mass amount of python libraries!
COPY --chown=tools.paws:tools.paws requirements.txt /tmp/requirements.txt

RUN pip --no-cache-dir install -r /tmp/requirements.txt

# Install pywikibot
RUN git clone --branch $PYWIKIBOT_VERSION --recursive https://gerrit.wikimedia.org/r/pywikibot/core.git /srv/paws/pwb
COPY --chown=tools.paws:tools.paws user-config.py /srv/paws/
COPY --chown=tools.paws:tools.paws user-fixes.py /srv/paws/

COPY install-pwb /usr/local/bin/
RUN /usr/local/bin/install-pwb

COPY install-extensions /usr/local/bin/
RUN /usr/local/bin/install-extensions

COPY banner /etc/bash.bashrc

# use custom css to hide clusters tab
COPY --chown=tools.paws:tools.paws hide_clusters_tab.css /home/paws/.jupyter/custom/custom.css

# Setup custom config as needed
COPY jupyter_notebook_config.py /srv/paws/etc/jupyter/jupyter_notebook_config.py

# install julia and julia kernel
COPY install-julia /tmp/install-julia
RUN /tmp/install-julia

# SPARQL
USER root
RUN apt-get update && \
    apt-get install --yes \
    # For sparql kernel
    graphviz

USER ${NB_USER}
RUN pip install --no-cache-dir sparqlkernel
RUN python3 -m jupyter sparqlkernel install --sys-prefix

EXPOSE 8888
