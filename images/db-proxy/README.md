Mysql-proxy plugin Lua script to perform simple authentication to the [Wiki Replicas](https://wikitech.wikimedia.org/wiki/Wiki_Replicas). This allows user to use Wiki Replica connections in their notebooks.

It makes a database connection to the Wiki Replicas using its own tool auth and a shared key with the Jupyterhub application.

It relies on a shared secret (passed in as an env variable `PASSWORD_SALT`) to authenticate users. This allows us to use one mysql user shared accross multiple different downstream users in a controlled way. Downstream users will have to generate a SHA256 based HMAC with the secret as the key and their username as data, and pass that HMAC as the password. This allows us to control who gets passwords (since we control the shared secret), without having to maintain too much state.

It requires the three following env variables to be set to work
- `HMAC_KEY`- the shared secret used to key the HMAC
- `MYSQL_USERNAME` - the username to use to connect to mysql backend
- `MYSQL_PASSWORD` - the password to use to connect to mysql backend


Refs:
- [Wiki Replicas](https://wikitech.wikimedia.org/wiki/Wiki_Replicas)
- [mysql-proxy docs](https://downloads.mysql.com/docs/mysql-proxy-en.pdf)
- [T253134](https://phabricator.wikimedia.org/T253134)