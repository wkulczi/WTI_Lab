import redis


    class RedisQueue:
        def __init__(self, _name, _host, _port, _db):
            self.cnxn = redis.Redis(host=_host, port=_port, db=_db)
            self.key = '%s:%s' % ("queue", _name)

        def qsize(self):
            return self.cnxn.llen(self.key)

        def empty(self):
            return self.qsize() == 0

        def put(self, item):
            self.cnxn.rpush(self.key, item)

        def get(self, block=True, timeout=None):
            if block:
                item = self.cnxn.blpop(self.key, timeout=timeout)
            else:
                item = self.cnxn.lpop(self.key)

            if item:
                return item
            else:
                return '(nil)'

        def clear(self):
            self.cnxn.delete(self.key)

        def get_nowait(self):
            return self.get(False)


q = RedisQueue('test', 'localhost', 6381, 0)
q.put('hello')
q.put('world')
x = q.get(block=False)
print(x)
x = q.get(block=False)
print(x)
q.put('hello')
q.put('world')
q.clear()
print(q.empty())

