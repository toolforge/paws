#!/bin/bash
set -e
# Used by travis to trigger deployment

curl \
    -d crypt-key="${GIT_CRYPT_KEY}" \
    -d release=prod \
    -d commit=${TRAVIS_COMMIT} \
    -d repo=https://github.com/yuvipanda/paws \
    -H 'Authorization: Bearer ${DEPLOY_HOOK_KEY}' \
    https://paws-deploy-hook.tools.wmflabs.org/deploy
