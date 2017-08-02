#!/bin/bash
# Just build and push all images
set -e
PREFIX="${1:-quay.io/wikimedia-paws/}"

function build (){
    WHAT="${1}"
    TAG=$(git log -n 1 --pretty=format:%H -- ${WHAT})
    NAME="${PREFIX}${WHAT}"
    docker build -t ${NAME}:${TAG} ${WHAT}
    docker push ${NAME}:${TAG}
}

TO_BUILD="singleuser db-proxy query-killer"

for IMAGE in ${TO_BUILD}; do
    build ${IMAGE}
done
