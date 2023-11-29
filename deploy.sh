#!/bin/bash

set -e

if [ "${1}" = 'eqiad1' ]
then
  datacenter=${1}
elif [ "${1}" = 'codfw1dev' ]
then
  datacenter=${1}
else
  echo "Please enter datacenter."
  echo "Usage:"
  echo "${0} <eqiad1|codfw1dev>"
  exit
fi


if ! command -v kubectl ; then
  echo "please install kubectl"
  exit 1
fi

if ! command -v helm ; then
  echo "please install helm"
  exit 1
fi

if ! command -v tofu ; then
  echo "please install tofu"
  exit 1
fi

source secrets-${datacenter}.sh

python3 -m venv .venv/deploy
source .venv/deploy/bin/activate
pip install ansible==8.1.0 kubernetes==26.1.0


cd tofu
tofu init -backend-config access_key="${ACCESS_KEY}" -backend-config secret_key="${SECRET_KEY}"
tofu apply -var datacenter=${datacenter} # -auto-approve
export KUBECONFIG=$(pwd)/kube.config

cd ../ansible
ansible-playbook paws.yaml --extra-vars "datacenter=${datacenter}"
