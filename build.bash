#!/bin/bash
# Just build and push all images
set -e
PREFIX="${1:-quay.io/wikimedia-paws/}"

function build (){
    DIR="$1"
    WHAT=$(basename ${1})
    TAG=$(git log -n 1 --pretty=format:%H -- ${WHAT})
    NAME="${PREFIX}${WHAT}"
    cd ${1}
    docker build -t ${NAME}:${TAG} .
    docker push ${NAME}:${TAG}
}

TO_BUILD=$(ls -d images/*/)


for IMAGE in ${TO_BUILD}; do
    build ${IMAGE}
done
