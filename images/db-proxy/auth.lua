-- Simple mysql-proxy plugin script to perform simple authentication
-- It relies on a shared secret (passed in as env variable PASSWORD_SALT)
-- to authenticate users. This allows us to use one mysql user shared across
-- multiple different downstream users in a controlled way. Downstream users
-- will have to generate a SHA256 based HMAC with the secret as the key
-- and their username as data, and pass that HMAC as the password. This allows
-- us to control who gets passwords (since we control the shared secret)
-- without having to maintain too much state.
--
-- It requires the three following env variables to be set to work
--  - HMAC_KEY- the shared secret used to key the HMAC
--  - MYSQL_USERNAME - the username to use to connect to mysql backend
--  - MYSQL_PASSWORD - the password to use to connect to mysql backend
--
-- It also rewrites queries to have a JSON blob with some metadata as a
-- comment in the beginning, currently containing just the username. This
-- allows us sysadmins to isolate and swat individual users when they do
-- crazy things, as they do.
local os = require('os')
local password = require("mysql.password")
local proto = require("mysql.proto")

package.cpath = package.cpath .. ';/usr/local/lib/lua/5.1/?.so'
local crypto = require('crypto')
local cjson = require('cjson')
local socket = require('socket.core')

local HMAC_KEY = os.getenv('HMAC_KEY')
local MYSQL_USERNAME = os.getenv('MYSQL_USERNAME')
local MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
local MYSQL_DOMAIN = os.getenv('MYSQL_DOMAIN') 

function connect_server()
	local client = proxy.connection.client
	local database = client.default_db
	local dns = socket.dns

	if (database == 'enwiki_p') then
		proxy.connection.backend_ndx = 1
	elseif (database == 'wikidatawiki_p') then
		proxy.connection.backend_ndx = 8
	elseif (database == 'commonswiki_p' or database == 'testcommonswiki_p') then
		proxy.connection.backend_ndx = 4
	elseif (database == 'meta_p') then
		proxy.connection.backend_ndx = 7
	else
		-- If this isn't a well-known db, ask DNS!
		local source_db = string.gsub(database, "_p", "")
		local db_host = source_db .. '.' .. MYSQL_DOMAIN
		local db_address, address_info = dns.toip(db_host)
		-- backend_address should be the canonical name (eg. s4.analytics...)
		local backend_address = address_info.name
		proxy.connection.backend_ndx = tonumber(backend_address:sub(2,2))
	end
end

function read_auth()
	local client = proxy.connection.client
	local server = proxy.connection.server

	local required_pw = crypto.hmac.digest(
		'sha256',
		client.username,
		HMAC_KEY
	)
	if password.check(
		server.scramble_buffer,
		client.scrambled_password,
		password.hash(password.hash(required_pw))
	) then
		proxy.queries:append(1,
			proto.to_response_packet({
				username = MYSQL_USERNAME,
				response = password.scramble(
					server.scramble_buffer,
					password.hash(MYSQL_PASSWORD)
				),
				charset  = 8, -- default charset
				database = client.default_db,
				max_packet_size = 1 * 1024 * 1024
			})
		)

		return proxy.PROXY_SEND_QUERY
	else
		return proxy.PROXY_IGNORE_RESULT
	end
end

function read_query( packet )
	if string.byte(packet) == proxy.COM_QUERY then
		local client = proxy.connection.client
		local query = string.sub(packet, 2)

		local metadata = {
			username = client.username
		}

		proxy.queries:append(
			1,
			string.char(proxy.COM_QUERY) .. "/*" .. cjson.encode(metadata) .. "*/" .. query
		)
		return proxy.PROXY_SEND_QUERY
	end
end
