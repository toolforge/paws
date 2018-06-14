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
ADD https://raw.githubusercontent.com/jupyterhub/jupyterhub/0.9.0rc1/examples/cull-idle/cull_idle_servers.py /usr/local/bin/cull_idle_servers.py
RUN chmod +rx /usr/local/bin/cull_idle_servers.py
RUN pip3 install --upgrade --no-cache-dir --force-reinstall jupyterhub==0.9.0rc1

ADD https://raw.githubusercontent.com/chicocvenancio/jupyterhub/31e6a15a8560a8481f009edd72d9195827df0259/jupyterhub/proxy.py /usr/local/lib/python3.6/dist-packages/jupyterhub/proxy.py
RUN chmod 644 /usr/local/lib/python3.6/dist-packages/jupyterhub/proxy.py
RUN chown ${NB_USER}:${NB_USER} /srv/jupyterhub
USER ${NB_USER}

CMD ["jupyterhub","--debug", "--config", "/srv/jupyterhub_config.py"]
