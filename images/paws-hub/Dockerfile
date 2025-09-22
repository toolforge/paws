FROM jupyterhub/k8s-hub:3.3.8
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

COPY PAWS.svg /usr/local/share/jupyterhub/static/PAWS.svg
COPY paws-favicon.ico /usr/local/share/jupyterhub/static/favicon.ico

RUN chown -R ${NB_USER}:${NB_USER} /srv/jupyterhub
USER ${NB_USER}

CMD ["jupyterhub", "--config", "/srv/jupyterhub_config.py"]
