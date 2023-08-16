import os
import json

DEBUG = True
REDIS_URL = 'redis://localhost:6380/0'
REDIS_ENABLED = True

REDIS_CONFIG = dict(host='localhost', port=6380, password='')


if os.environ.get('VCAP_APPLICATION'):
    DEBUG = False
    services = json.loads(os.getenv('VCAP_SERVICES'))
    if 'aws-elasticache-redis' in services:
        redis_credentials = services['aws-elasticache-redis'][0]['credentials']
        REDIS_CONFIG['host'] = redis_credentials['host']
        REDIS_CONFIG['port'] = int(redis_credentials['port'])
        REDIS_CONFIG['password'] = redis_credentials['password']
        # REDIS_CONFIG['ssl'] = True
        # REDIS_CONFIG['ssl_cert_reqs'] = None
        REDIS_URL = redis_credentials['uri'].replace("redis", "rediss")
        REDIS_ENABLED = True
    else:
        REDIS_URL = None
        REDIS_ENABLED = False
