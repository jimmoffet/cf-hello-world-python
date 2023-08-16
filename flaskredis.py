import os
import traceback
import logging
import time
from flask import Flask, current_app, jsonify
from flask_redis import FlaskRedis
from redis import RedisError, Redis

app = Flask(__name__)
app.config.from_object('config')


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@app.route('/')
def hello():
    logger.info('serving hello at default route /')
    return 'Coming Soon!'


@app.route('/flaskredis', methods=['GET'])
def flaskredis():
    logger.info('serving flaskredis at /flaskredis')
    try:
        api_status = {"error": "unexpected error"}
        logger.info(f"app.config: {app.config}")
        redis_uri = app.config['REDIS_URL']
        logger.info(f"config['REDIS_URL']: {redis_uri}")
        redis_enabled = app.config['REDIS_ENABLED']
        logger.info(f"config['REDIS_ENABLED']: {redis_enabled}")
        if redis_enabled:
            logger.info("config['REDIS_ENABLED'] evaluates as True")
        redis_config = app.config['REDIS_CONFIG']
        logger.info(f"config['REDIS_CONFIG']: {redis_config}")

        try:
            now = str(int(time.time()))
            check_redis = FlaskRedis()
            check_redis.init_app(app, **redis_config)
            check_redis.set('mytestkey', now)
            val = check_redis.get('mytestkey')
            logger.info(f"mytestkey is: {val}")
        except RedisError as err:
            logger.exception(f"Redis service failed to respond with {err}")

        api_status = {"200": "ok", "mytestkey": str(val)}

        return jsonify(
            status="ok",
            api=api_status), 200
    except Exception as err:
        current_app.logger.exception(
            F"Unhandled exception: {err} - {traceback.format_exc()}")
        return jsonify(
            status=f"error: {err}",
            api=api_status), 500


@app.route('/redis', methods=['GET'])
def redis():
    logger.info('serving redis at /redis')
    try:
        api_status = {"error": "unexpected error"}
        logger.info(f"app.config: {app.config}")
        redis_uri = app.config['REDIS_URL']
        logger.info(f"config['REDIS_URL']: {redis_uri}")
        redis_enabled = app.config['REDIS_ENABLED']
        logger.info(f"config['REDIS_ENABLED']: {redis_enabled}")
        if redis_enabled:
            logger.info("config['REDIS_ENABLED'] evaluates as True")
        redis_config = app.config['REDIS_CONFIG']
        logger.info(f"config['REDIS_CONFIG']: {redis_config}")

        try:
            now = str(int(time.time()))
            check_redis = Redis(ssl=True, ssl_cert_reqs=None, **redis_config)
            check_redis.set('mytestkey', now)
            val = check_redis.get('mytestkey')
            logger.info(
                f"Retrieved value from redis for mytestkey is: {val}")
        except RedisError as err:
            logger.exception(f"Redis service failed to respond with {err}")

        api_status = {"200": "ok", "mytestkey": str(val)}

        return jsonify(
            status="ok",
            api=api_status), 200
    except Exception as err:
        current_app.logger.exception(
            F"Unhandled exception: {err} - {traceback.format_exc()}")
        return jsonify(
            status=f"error: {err}",
            api=api_status), 500


port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))
