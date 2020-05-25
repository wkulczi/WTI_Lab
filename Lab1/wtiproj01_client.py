import redis

# cnxn = RedisQueue('test', 'localhost', 6381, 0)


class RedisQueue:
    def __init__(self, _name='default', _host='localhost', _port=6381, _db=0):
        """
        Initialize redis queue class
        Args:
            _name: Name of queue in redis, default value: 'default'
            _host: Host adress, default value: 'localhost'
            _port: Connection port, default value: 6381
            _db: i don't remember, sorry
        """
        self.cnxn = redis.Redis(host=_host, port=_port, db=_db)
        self.key = '%s:%s' % ("queue", _name)

    def qsize(self):
        """
        Returns: size of list
        """
        return self.cnxn.llen(self.key)

    def empty(self)->bool:
        """
        Returns: if redis queue is empty
        """
        return self.qsize() == 0

    def put(self, item):
        """
        Pushes using redis rpush
        Args:
            item: Item to push
        """
        self.cnxn.rpush(self.key, item)

    def get(self, block=True, timeout=None):
        """
        Pops using redis lpop
        Args:
            block: If block connection, default: True
            timeout: Sets timeout value, default: None

        Returns: Item at the leftmost.

        """
        if block:
            item = self.cnxn.blpop(self.key, timeout=timeout)
        else:
            item = self.cnxn.lpop(self.key)

        if item:
            return item
        else:
            return '(nil)'

    def clear(self):
        """
        Clears redis queue.
        """
        self.cnxn.delete(self.key)

    def get_nowait(self):
        """

        Returns: ¯\_(ツ)_/¯

        """
        return self.get(False)