import logging
import random
import time

from microprediction.config_private import COVID_API, COVID_UUID, BUZZ_UUIDS

from ravenpackapi import RPApi, ApiConnectionError

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# initialize the API (here we use the RP_API_KEY in os.environ)
api = RPApi(api_key=COVID_API)

# query the realtime feed
ds = api.get_dataset(dataset_id=BUZZ_UUIDS["cop.json"])


def wait_between_attempts():
    """ Incremental backoff between connection attempts """
    wait_time = 0.3  # time is in seconds
    while True:
        yield wait_time
        wait_time = min(wait_time * 1.5, 30)
        wait_time *= (100 + random.randint(0, 50)) / 100


wait_time = wait_between_attempts()
while True:
    try:
        for record in ds.request_realtime():
            print(record)
            print(record.timestamp_utc, record.entity_name,
                  record['event_relevance'])
    except (KeyboardInterrupt, SystemExit):
        break
    except ApiConnectionError as e:
        logger.error("Connection error %s: reconnecting..." % e)
        time.sleep(next(wait_time))