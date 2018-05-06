FROM jupyterhub/k8s-hub:v0.6
ARG NB_USER=tools.paws
ARG NB_UID=52771
ARG HOME=/home/paws
USER root
RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    --home ${HOME} \
    --force-badname \
    ${NB_USER}
COPY cull_idle_servers.py /usr/local/bin/cull_idle_servers.py

RUN pip3 install --upgrade --no-deps --force-reinstall https://github.com/chicocvenancio/jupyterhub/raw/dynamic_tables/dist/jupyterhub-0.8.1-py3-none-any.whl
RUN chown ${NB_USER}:${NB_USER} /srv/jupyterhub

USER ${NB_USER}

CMD ["jupyterhub","--debug", "--config", "/srv/jupyterhub_config.py"]
