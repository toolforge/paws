# PAWS

PAWS: A Web Shell (PAWS) is a Jupyter notebooks deployment that has been customized to make interacting with Wikimedia wikis easier. It allows users to create and share documents that contain live code, visualizations such as graphs, rich text, etc. The user created notebooks are a powerful tool that enables data analysis and scientific research, and also transforms the way in which programmers write code - by enabling an exploratory environment with a quick feedback loop, and a low barrier for entry through it's easy to use graphical interface. 

## Contributing

Bugs, issues and feature requests are found on [Wikimedia Foundation's Phabricator](https://phabricator.wikimedia.org/).
There is a [workboard](https://phabricator.wikimedia.org/project/view/1648/) and a project tag of `#paws` to use for related work. You can reference code and commits from this repo at the Phabricator mirror of the code [here](https://phabricator.wikimedia.org/diffusion/PAWS/browse/master/), but please do not clone or try to use that mirror directly.

To contribute to this project's code, please fork the repo on [GitHub](https://github.com/toolforge/paws/) and submit a pull request.

If you have push access to the project, we ask that new changes be reviewed by one other
project member by using either a feature branch on the  https://github.com/toolforge/paws repo
to trigger a pull request or using a fork to set up a pull request.

### Settings up a development environment

It is possible to run a fully-functioning PAWS system inside [minikube](https://minikube.sigs.k8s.io/docs/)! You don't need
access to the secrets.yaml file to do it either, since the defaults mostly support it. At this time, you need to
set it up with a cluster version before 1.22, most likely.

Once minikube is working, you need to run `minikube addons enable ingress` to have ingress controller support.

You will need to install minikube and [helm](https://helm.sh) on your system. When you are confident those are working,
install the dependencies for the PAWS dev environment with these steps:
 - `helm repo add jupyterhub https://jupyterhub.github.io/helm-chart/`
 - `helm repo add bitnami https://charts.bitnami.com/bitnami`
 - `helm dep up paws/`

Then, you need to create a new namespace for paws (`kubectl create namespace paws-dev` for instance) and then install into it
with helm (from the top level of this repo):
`helm -n paws-dev install dev paws/`

The rest of the setup instructions will display on screen as long as the install is successful.
Please refer to the helm documentation from there.

NOTE: By default the mariadb chart keeps a PersistentVolumeClaim around for its storage even after
uninstall. If you intend on rebuilding your dev environment later, you will need to use all the same
values for DB and DB passwords if you don't delete that claim and volume (and the data from your
last wiki will be in there--which means you keep your oauth grant!). The PVC for mediawiki gets cleaned up on uninstall.

If minikube is acting weird, it might be worth it to upgrade minikube or even to
 increase the default memory:
`minikube config set memory 4096`

#### Working with images
There are 8 images that are part of PAWS, in particular in the images/ directory. If you start a dev environment, it will pull those images from quay.io by default, just like in Wikimedia Cloud Services. If you are making changes to the images and testing those locally, you'll need to build them and tag them for your local environment, possibly setting them in your local values file with the tags you set.

If you are using minikube, you need to make sure you are using minikube's docker, not your system's docker with `eval $(minikube docker-env)`. Now your docker commands will operate on the minikube environment.

For example, let's say you wanted to update the singleuser image (which is the actual notebook server image):
- `cd images/singleuser`
- `docker build -t tag-you-are-going-to-use:whatever .`

And then you should have the image with a tag of `tag-you-are-going-to-use:whatever` that you could edit into your values.yaml file for local helm work. If you were aiming to aggressively push a tag for deployment, dodging around the CI system to do so, you'd tag with `quay.io/wikimedia-paws-prod/singleuser:latest`, which will cause a later `docker push quay.io/wikimedia-paws-prod/singleuser:latest` to actually push that tag directly to the repo for deployment in Cloud Services. Don't do that unless you really know what you are doing.
## Useful libraries
### Accessing Database Replicas With Pandas and Sqlalchemy

Pandas is a lovely high level library for in-memory data manipulations. In order to get the result of a SQL query as a pandas dataframe use:
```
from sqlalchemy import create_engine
import sys, os
import pandas as pd

constr = 'mysql+pymysql://{user}:{pwd}@{host}'.format(user=os.environ['MYSQL_USERNAME'],
                                                      pwd=os.environ['MYSQL_PASSWORD'],
                                                      host=os.environ['MYSQL_HOST'])
con = create_engine(constr)

df = pd.read_sql('select * from plwiki_p.logging limit 10', con)
```

### Storage space
Publishing space

A notebook can be turned into a public notebook by publishing a link to it. This works as the notebook is made available in a read only mode. An example might be …revisions-sql.ipynb?kernel_name=python3. It could be wise to add the kernel name to the link, even if it isn't necessary in some cases.

If you want to run the copy yourself, or do interactive changes, you must download the notebook and reupload on your own account. Downloading the raw format of the previous example can be done by adding format=raw to the previous example …revisions-sql.ipynb?format=raw. This download-reupload-process is somewhat awkward.

Note that a notebook will always be published, as the link can be guessed, so don't add any private information. 

### To know more about paws have a look at:
https://wikitech.wikimedia.org/wiki/PAWS
