# A jupyterhub config for a local PAWS install
import socket

c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
c.JupyterHub.hub_ip = '0.0.0.0' 

c.DockerSpawner.hub_ip_connect = socket.gethostbyname(socket.getfqdn())
c.DockerSpawner.container_image = 'yuvipanda/pawsuser'

c.JupyterHub.ip = '0.0.0.0'
