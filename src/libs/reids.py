import redis as redis

redis_config_online = {
    "host": "slots-redis-stream.8domnh.0001.use1.cache.amazonaws.com",
    "port": 5379,
    "db": 1
}

redis_config_test = {
    "host": "172.16.10.249",
    "port": 6379,
    "db": 1
}
redis_config = redis_config_test
redis_pool = redis.ConnectionPool(**redis_config)


class Redis():
    def __init__(self):
        self.r = redis.StrictRedis(connection_pool=redis_pool)

    def xadd_stream(self, fields, stream_name="slots:server_event", id="*"):
        result = self.r.xadd(stream_name, fields, id=id)

    def xadd_world_event(self, data):
        pass


m_redis = Redis()
