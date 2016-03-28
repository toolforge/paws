import os
import hmac
import hashlib


c.Application.log_level = 'DEBUG'

c.JupyterHub.authenticator_class = 'oauthenticator.mediawiki.MWOAuthenticator'
c.JupyterHub.hub_ip = '127.0.0.1'
c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.db_url = os.environ['JPY_DB_URL']
c.JupyterHub.db_kwargs = {
    'pool_recycle': 60  # Do not keep connections for more than one minute
}

c.MWOAuthenticator.client_id = '0a73e346a40b07262b6e36bdba01cba4'
c.MWOAuthenticator.client_secret = '99b284730a79dd30e2c35988be42708ef7e57122'
c.MWOAuthenticator.pass_secrets = True

c.JupyterHub.spawner_class = 'kubespawner.KubeSpawner'
c.KubeSpawner.kube_namespace = 'paws'

c.Authenticator.admin_users = {'YuviPanda'}
c.Authenticator.admin_access = True

def generate_mysql_password(spawner):
    h = hmac.new(
        os.environ['MYSQL_HMAC_KEY'].encode('utf-8'),
        spawner.user.name.encode('utf-8'),
        hashlib.sha256
    )
    return h.hexdigest()


def generate_mysql_username(spawner):
    return spawner.user.name


c.KubeSpawner.extra_env = {
    'MYSQL_HOST': os.environ['MYSQL_SERVICE_HOST'],
    'MYSQL_USERNAME': generate_mysql_username,
    'MYSQL_PASSWORD': generate_mysql_password
}

c.KubeSpawner.kube_api_endpoint = 'https://%s' % os.environ['KUBERNETES_PORT_443_TCP_ADDR']
c.KubeSpawner.hub_ip_connect = '%s:8000' % os.environ['PAWS_PORT_8000_TCP_ADDR']
c.KubeSpawner.kube_ca_path = False
c.KubeSpawner.kube_token = os.environ['INSECURE_KUBE_TOKEN']
c.KubeSpawner.singleuser_image_spec = 'tools-docker-registry.wmflabs.org/pawsuser'
c.KubeSpawner.volumes = [
    {
        'name': 'home',
        'hostPath': {
            'path': '/data/project/paws/userhomes/{userid}'
        }
    },
    {
        'name': 'dumps',
        'hostPath': {
            'path': '/public/dumps',
        }
    }
]
c.KubeSpawner.volume_mounts = [
    {
        'mountPath': '/home/paws',
        'name': 'home'
    },
    {
        'mountPath': '/public/dumps',
        'name': 'dumps',
    }
]
c.KubeSpawner.start_timeout = 60 * 5  # First pulls can be really slow


c.JupyterHub.base_url = '/paws/'
