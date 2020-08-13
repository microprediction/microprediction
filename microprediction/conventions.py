from microconventions import MicroConventions, KeyConventions, api_url, failover_api_url, new_key, create_key, maybe_create_key

PY_REDIS_ARGS = (
    'host', 'port', 'db', 'username', 'password', 'socket_timeout', 'socket_keepalive', 'socket_keepalive_options',
    'connection_pool', 'unix_socket_path', 'encoding', 'encoding_errors', 'charset', 'errors',
    'decode_responses', 'retry_on_timeout', 'ssl', 'ssl_keyfile', 'ssl_certfile', 'ssl_cert_reqs', 'ssl_ca_certs',
    'ssl_check_hostname', 'max_connections', 'single_connection_client', 'health_check_interval', 'client_name')
FAKE_REDIS_ARGS = ('decode_responses',)