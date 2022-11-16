#!/bin/bash

k8s_version='v1.21.8'

# check that we have dependencies
for command in kubectl helm minikube ; do
    if ! command -v ${command} > /dev/null ; then
        echo "${command} was not found"
        echo "please install ${command} before proceeding"
        exit 1
    fi
done

# Rather than mess with people's minikube setup let them know about it and ask them to fix it
if ! kubectl get nodes | tail -1 | awk '{print $NF}' | grep "${k8s_version}" > /dev/null ; then
    if minikube status > /dev/null ; then
        echo "minikube is running but not on k8s version ${k8s_version}."
    else
        echo "minikube is not running."
    fi
    echo "Please create and start a cluster running ${k8s_version}. Perhaps by running:"
    echo "minikube start --kubernetes-version=${k8s_version}"
    echo "Then rerun this script."
    exit 1
fi

# these steps are fast, just run them
minikube addons enable ingress
helm repo add jupyterhub https://jupyterhub.github.io/helm-chart/
helm dep up paws/
kubectl create namespace paws-dev --dry-run=client -o yaml | kubectl apply -f -
kubectl config set-context --current --namespace=paws-dev

if helm status -n paws-dev dev 2>&1 > /dev/null ; then
    helm -n paws-dev upgrade dev paws/ --timeout=50m
else
    helm -n paws-dev install dev paws/ --timeout=50m
fi
