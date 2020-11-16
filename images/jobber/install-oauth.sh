#!/bin/ash

extension_url=$(curl 'https://www.mediawiki.org/w/api.php?action=query&list=extdistbranches&edbexts=OAuth&formatversion=2&format=json' | jq -r .query.extdistbranches.extensions.OAuth.REL1_34)
/usr/bin/curl -o OAuth.tar.gz "$extension_url"

# Wait until the mediawiki pod creates the extensions dir in the PVC
while ! test -d "/opt/mediawiki/extensions"; do
    sleep 1
done
tar -xzf OAuth.tar.gz -C /opt/mediawiki/extensions
chown -R 1001:0 /opt/mediawiki/extensions/OAuth
