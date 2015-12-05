# A jupyterhub config for a local PAWS install
import socket

c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
c.JupyterHub.hub_ip = '0.0.0.0' 

c.DockerSpawner.hub_ip_connect = socket.gethostbyname(socket.getfqdn())
c.DockerSpawner.container_image = 'yuvipanda/pawsuser'

# Setup MW OAuth Login
# These credentials are set up to be useful only for localhost and
# have no privilages, so are ok to be public I think.
c.JupyterHub.authenticator_class = 'oauthenticator.mediawiki.MWOAuthenticator'
c.MWOAuthenticator.client_id = 'e9f54a40f11e930c5b8e9c422e2cb470'
c.MWOAuthenticator.client_secret = '4efddbcac568a99dcc164fa72560cca05841ffd5'

c.JupyterHub.ip = '0.0.0.0'
