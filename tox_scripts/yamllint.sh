#!/bin/bash

# yamllint doesn't handle helm templates well, in particular {{- bits, so we
# exclude them with some sed. In order to keep from making a mess of the working
# directory of anyone running this test we copy them to a tmp directory. Then we
# switch to that directory to do the test as it looks more like we are actually
# running in the base dir, rather than displaying things like
# /tmp/tmpdir/paws/values.yaml will show ./paws/values.yaml in output.

export TEMP_DIR=$(mktemp -d -p "/tmp/")
cp -r . ${TEMP_DIR} 
cd ${TEMP_DIR}
find . -not -path "./.tox/*" -type f -regex ".*\.ya?ml" -exec sed -i "s/{{/# /" {} \;
yamllint -c .yamllint.conf .
