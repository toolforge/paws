FROM jupyterhub/k8s-hub:v0.6
ARG NB_USER=tools.paws
ARG NB_UID=52771
ARG HOME=/home/paws
RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    --home ${HOME} \
    --force-badname \
    ${NB_USER}

RUN chown ${NB_USER}:${NB_USER} /srv/jupyterhub

USER ${NB_USER}
CMD ["jupyterhub", "--config", "/srv/jupyterhub_config.py"]
