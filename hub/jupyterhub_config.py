import os
c.Application.log_level = 'DEBUG'

c.JupyterHub.authenticator_class = 'oauthenticator.mediawiki.MWOAuthenticator'

c.MWOAuthenticator.client_id = '8303709369544a0b519dbb0df52fc804'
c.MWOAuthenticator.client_secret = '5eb1c8a7d97edd72db241f8cd8ea2c6f7fd9ab39'
c.MWOAuthenticator.pass_secrets = True

c.JupyterHub.spawner_class = 'kubespawner.KubeSpawner'
c.KubeSpawner.kube_namespace = 'paws'
c.KubeSpawner.kube_api_endpoint = 'https://%s' % os.environ['KUBERNETES_PORT_443_TCP_ADDR']
c.KubeSpawner.hub_ip_connect = '%s:30000' % os.environ['PAWS_PORT_30000_TCP_ADDR']
c.KubeSpawner.kube_ca_path = False
c.KubeSpawner.kube_token = os.environ['INSECURE_KUBE_TOKEN']
c.KubeSpawner.singleuser_image_spec = 'yuvipanda/pawsuser:latest'
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

c.JupyterHub.base_url = '/paws/'
