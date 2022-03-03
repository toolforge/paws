# PAWS

PAWS: A Web Shell (PAWS) is a Jupyter notebooks deployment that has been customized to make interacting with Wikimedia wikis easier. It allows users to create and share documents that contain live code, visualizations such as graphs, rich text, etc. The user created notebooks are a powerful tool that enables data analysis and scientific research, and also transforms the way in which programmers write code - by enabling an exploratory environment with a quick feedback loop, and a low barrier for entry through it's easy to use graphical interface.

## Contributing

Bugs, issues and feature requests are found on [Wikimedia Foundation's Phabricator](https://phabricator.wikimedia.org/).
There is a [workboard](https://phabricator.wikimedia.org/project/view/1648/) and a project tag of `#paws` to use for related work. You can reference code and commits from this repo at the Phabricator mirror of the code [here](https://phabricator.wikimedia.org/diffusion/PAWS/browse/master/), but please do not clone or try to use that mirror directly.

To contribute to this project's code, please fork the repo on [GitHub](https://github.com/toolforge/paws/) and submit a pull request.

If you have push access to the project, we ask that new changes be reviewed by one other
project member by using either a feature branch on the https://github.com/toolforge/paws repo
to trigger a pull request or using a fork to set up a pull request.

### Pull Requests and CI

When a pull request is opened a few things are run automatically. Any container that was modified in /images will be built and pushed to quay.io. Your branch will be updated with an additional commit, updating the values.yaml file to point to the new image tags. And a linter will be run. These workflows, and their status, will be visible in the github pull request page. At this point you, or anyone else, will be able to pull down the branch in the PR and run it locally in minikube as described below.

If your PR originates from a fork, please be sure "Allow edits and access to secrets by maintainers" is enabled such that the CI can function. Alternatively please manually edit the values.yaml to match the PR number for any containers that your code updates.

### Settings up a development environment

It is possible to run a fully-functioning PAWS system inside [minikube](https://minikube.sigs.k8s.io/docs/)! You don't need
access to the secrets.yaml file to do it either, since the defaults mostly support it. At this time, you need to
set it up with a cluster version before 1.22, most likely.

You will need to install minikube (tested on minikube 1.23) and [helm](https://helm.sh) and kubectl on your system. When you are confident those are working, start minikube with:
 - `minikube start --kubernetes-version=v1.20.11`
 - `minikube addons enable ingress`
(from the top level of this repo):
install the dependencies for the PAWS dev environment with these steps:
 - `helm repo add jupyterhub https://jupyterhub.github.io/helm-chart/`
 - `helm dep up paws/`
 - `kubectl create namespace paws-dev`
 - `helm -n paws-dev install dev paws/ --timeout=50m`

The rest of the setup instructions will display on screen as long as the install is successful.
Please refer to the helm documentation from there.

If you are experiencing issues with the installation, you can try changing the driver configuration in minikube: https://minikube.sigs.k8s.io/docs/drivers/

- First delete the current cluster:

    `minikube delete`

- Start a new cluster with the driver you want to use (e.g. docker, virtualbox, hyperkit, etc.):

    `minikube start --driver=docker --kubernetes-version=v1.20.11`

Another possible solution if minikube is acting weird might be to upgrade minikube, or even to
increase the default memory:

`minikube config set memory 4096`

#### Working with images
Keep in mind that opening a PR will, attempt, to build any image that has changed in the PR branch. This method is fine to build and test the resulting container. Though it is often easier to build, and rebuild, a container locally for testing. The following describes how to build and use a container locally.

There are 8 images that are part of PAWS, in particular in the images/ directory. If you start a dev environment, it will pull those images from quay.io by default, just like in Wikimedia Cloud Services. If you are making changes to the images and testing those locally, you'll need to build them and tag them for your local environment, possibly setting them in your local values file with the tags you set.

If you are using minikube, you need to make sure you are using minikube's docker, not your system's docker with `eval $(minikube docker-env)`. Now your docker commands will operate on the minikube environment.

For example, let's say you wanted to update the singleuser image (which is the actual notebook server image):
- `cd images/singleuser`
- `docker build -t tag-you-are-going-to-use:whatever .`

And then you should have the image with a tag of `tag-you-are-going-to-use:whatever` that you could edit into your values.yaml file for local helm work.
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
