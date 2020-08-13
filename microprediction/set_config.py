import os
from sys import platform
from getjson import getjson


# Retrieve credentials for database where state is stored

try:
    from microprediction.set_env_private import NOTHING_MUCH
except ImportError:
    # Environment variables need to be set some other way, for example by retrieving github secrets
    pass

micro_config_url = os.getenv('MICRO_TEST_CONFIG_URL')
if micro_config_url is None:
    raise Exception('Cannot get environment variable MICRO_TEST_CONFIG_URL')

micro_config_failover_url = os.getenv('MICRO_TEST_CONFIG_FAILOVER_URL')
if micro_config_failover_url is None:
    raise Exception('Cannot get environment variable MICRO_TEST_CONFIG_FAILOVER_URL')

MICRO_TEST_CONFIG = getjson(url=micro_config_url, failover_url=micro_config_failover_url)
