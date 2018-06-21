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

RUN chmod +rx /usr/local/bin/cull_idle_servers.py
RUN pip3 install --upgrade --no-cache-dir --force-reinstall jupyterhub==0.9.0
COPY PAWS.svg /srv/jupyterhub

RUN chown -R ${NB_USER}:${NB_USER} /srv/jupyterhub
USER ${NB_USER}

CMD ["jupyterhub", "--config", "/srv/jupyterhub_config.py"]
