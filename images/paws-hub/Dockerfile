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
ADD https://raw.githubusercontent.com/jupyterhub/jupyterhub/0.9.0b3/examples/cull-idle/cull_idle_servers.py /usr/local/bin/cull_idle_servers.py
RUN chmod +rx /usr/local/bin/cull_idle_servers.py
RUN pip3 install --upgrade --no-cache-dir --force-reinstall jupyterhub==0.9.0b3

ADD https://raw.githubusercontent.com/minrk/jupyterhub/505a6eb4e33216e3694d5ddd806150e4212012ec/jupyterhub/user.py /usr/local/lib/python3.6/dist-packages/jupyterhub/user.py
RUN chown ${NB_USER}:${NB_USER} /srv/jupyterhub
USER ${NB_USER}

CMD ["jupyterhub","--debug", "--config", "/srv/jupyterhub_config.py"]
