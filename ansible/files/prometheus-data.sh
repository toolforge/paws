#!/bin/bash

export KUBECONFIG=/tmp/kube.config.previous
PREVIOUS_POD=$(kubectl get pods -n metrics --selector=app.kubernetes.io/component=server --no-headers -o custom-columns=":metadata.name")
kubectl -n metrics exec -it pod/${PREVIOUS_POD} -c prometheus-server -- tar cfz backup.tar.gz /data
kubectl cp metrics/${PREVIOUS_POD}:backup.tar.gz /tmp/prometheus.tar.gz -c prometheus-server

sleep 150 # make a little gap of time to keep data from overlapping

export KUBECONFIG=/tmp/kube.config.current
CURRENT_POD=$(kubectl get pods -n metrics --selector=app.kubernetes.io/component=server --no-headers -o custom-columns=":metadata.name")
kubectl -n metrics wait --for=condition=ready pod -l app.kubernetes.io/component=server --timeout=600s
kubectl cp /tmp/prometheus.tar.gz metrics/${CURRENT_POD}:backup.tar.gz -c prometheus-server
kubectl -n metrics exec -it pod/${CURRENT_POD} -c prometheus-server -- sh -c 'rm -rf /data/* ; tar xfz backup.tar.gz -C /'
kubectl -n metrics rollout restart deployment.apps/prometheus-server
