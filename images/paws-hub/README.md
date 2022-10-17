This is the jupyterhub image with a few branding changes for PAWS.

The image is built for production by a github action. It can be built locally with:
docker build .
from this directory.

The image itself would be deployed into PAWS through helm. Defined in the values.yaml file under the jupyterhub.hub definition. 
