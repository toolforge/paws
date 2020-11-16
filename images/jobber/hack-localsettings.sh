#!/bin/ash

if ! test -f /opt/mediawiki/LocalSettings.php; then
    echo "The settings file LocalSettings.php is missing!"
    exit 1
fi

/bin/cat <<"EOF" >> /opt/mediawiki/LocalSettings.php
wfLoadExtension( 'OAuth' );
$wgMWOAuthSecureTokenTransfer = false;
$wgEmailAuthentication = false;
$wgOAuthSecretKey = '0469807d667f4d6cdbf3ae772ea874d95518fbe41c59f73eb59169f7ed02b7d3';
$wgGroupPermissions['user']['mwoauthmanageconsumer'] = true;
$wgGroupPermissions['user']['mwoauthproposeconsumer'] = true;
$wgGroupPermissions['user']['mwoauthupdateownconsumer'] = true;
$wgOAuthGroupsToNotify = [ 'sysop' ];
EOF
