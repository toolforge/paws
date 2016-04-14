#!/usr/bin/python
import os


CONFIG = """
# Let nginx automatically determine the number of worker processes
# to run. This defaults to number of cores on the host.
worker_processes auto;

# Do not daemonize - we'll either run this under a supervisor
# ourselves, or jupyterhub will manage the process, restarting
# it when it dies as necessary
daemon off;

# Set number of connections accepted per worker
events {
    worker_connections 768;
}

# This needs to be in 'main' since otherwise nginx
# will try to write to /var/log/nginx/error.log and failed
# because it does not have permissions
error_log stderr info;

# We do not really need / care about a pidfile
pid /dev/null;

http {
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    # server_tokens off;

    # These are varilous temp file paths, many that we do not use.
    # They are by default set to /var/lib/nginx/*, which causes
    # problems when running as non-root, as we are here. So we
    # shall set them all to /tmp. FIXME: Find proper paths for
    # these somewhere (perhaps on current-dir?)
    client_body_temp_path /tmp;
    proxy_temp_path /tmp;
    fastcgi_temp_path /tmp;
    uwsgi_temp_path /tmp;
    scgi_temp_path /tmp;

    # access_log does not support 'stderr' directive directly
    # FIXME: This does not work in docker < 1.9 https://github.com/docker/docker/issues/6880
    access_log /dev/stderr;

    # nginx needs an async way to resolve hostnames to IPs, and
    # the default `gethostbyname` setup does not allow for this.
    # While ideally nginx should parse /etc/resolv.conf itself,
    # it does not do so at this time, and needs us to set the DNS
    # server explicitly. This can be specified by the user, but
    # defaults to a value we parse out of /etc/resolv.conf.
    # NOTE: This causes issues when resolving localhost and
    # other hostnames traditionally set in /etc/hosts, since
    # DNS servers respond erratically to queries for them.
    resolver %s ipv6=off;

    # This is used to support websocket proxying. We need to set
    # the 'Upgrade' HTTP header to either 'upgrade' (for websockets)
    # or 'close' (for everything else).
    # See https://www.nginx.com/resources/admin-guide/reverse-proxy/
    # for more details.
    map $http_upgrade $connection_upgrade {
            default upgrade;
            ''      close;
    }

    # Shared memory area for caching username to id mappings
    lua_shared_dict usernamemapping 16m;

    lua_ssl_trusted_certificate /etc/ssl/certs/ca-certificates.crt;
    lua_ssl_verify_depth 10;

    # This is the 'regular' server, that sees all public
    # traffic and proxies them to the appropriate backend server.
    server {
        listen 0.0.0.0:8000;

        location ~ \/\. {
            deny all;
        }

        # Only after the User: redirect! Otherwise our backend can't find the file.
        location ~ /\d+/.*\.ipynb$ {
            include /etc/nginx/uwsgi_params;
            uwsgi_pass uwsgi://%s:8000;
        }

        location /paws-public {
            rewrite_by_lua '
                local m = ngx.re.match(ngx.var.uri, "/paws-public/User:([^/]+)(.*)");
                if m then
                    local userid = ngx.shared.usernamemapping:get(m[1]);
                    if userid == nil then
                        local http = require "resty.http";
                        local httpc = http.new();
                        local apiurl = "https://meta.wikimedia.org/w/api.php?" ..
                                       "action=query&format=json&formatversion=2" ..
                                       "&prop=&list=users&meta=&usprop=centralids" ..
                                       "&ususers=" .. m[1];

                        local res, err = httpc:request_uri(apiurl);
                        local cjson = require "cjson";
                        local resp_data = cjson.decode(res.body);

                        ngx.log(ngx.ERR, res.body);
                        if resp_data["query"]["users"][1]["missing"] then
                            ngx.exit(404);
                        end
                        userid = resp_data["query"]["users"][1]["centralids"]["CentralAuth"]

                        ngx.shared.usernamemapping:set(m[1], userid);
                    end
                    return ngx.exec("/paws-public/" .. userid  .. m[2]);
                end
            ';

            index index.html index.ipynb Index.ipynb;
            fancyindex on;

            alias /data/project/paws/userhomes;

            proxy_http_version 1.1;

            # This is required for websockets to be proxied correctly
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection $connection_upgrade;

            # This is required for the target servers to know what
            # exactly the original protocol / URI / Host was.
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_set_header X-Original-URI $request_uri;
            proxy_set_header Host $host:$server_port;
        }
    }
}
"""

def get_nameservers(ipv4only=True):
    """
    Return a list of nameservers from parsing /etc/resolv.conf.

    If ipv4only is set, filter out ipv6 nameservers. This is because nginx
    freaks out in some formats of ipv6 that otherwise seem ok.
    """
    nameservers = []
    with open('/etc/resolv.conf') as f:
        for line in f:
            if line.strip().startswith('nameserver'):
                nameservers += line.strip().split(' ')[1:]
    if ipv4only:
        nameservers = [n for n in nameservers if ':' not in n]
    return nameservers

with open('/tmp/nginx.conf', 'w') as f:
    # Not using the nicer .format since it gets confused by the { } in the
    # nginx config itself :(
    params = (
        ' '.join(get_nameservers()),
        os.environ['RENDERER_PORT_8000_TCP_ADDR']
    )
    f.write(CONFIG % params)

os.execl('/usr/sbin/nginx', '/usr/sbin/nginx', '-c', '/tmp/nginx.conf')
