FROM jupyterhub/k8s-hub:1.1.3
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

COPY PAWS.svg /srv/jupyterhub

RUN chown -R ${NB_USER}:${NB_USER} /srv/jupyterhub
USER ${NB_USER}

CMD ["jupyterhub", "--config", "/srv/jupyterhub_config.py"]
