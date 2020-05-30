import redis


# cnxn = RedisQueue('test', 'localhost', 6381, 0)


class RedisQueue:
    _name = ""



    def __init__(self, name='default', host='localhost', port=6381):
        """
        Initialize redis queue class
        Args:
            _name: Name of queue in redis, default value: 'default'
            host: Host adress, default value: 'localhost'
            port: Connection port, default value: 6381
            db: i don't remember, sorry
        """
        self._name = name
        self.cnxn = redis.Redis(host=host, port=port)
        self.key = '%s:%s' % ("queue", name)

    def qsize(self):
        """
        Returns: size of list
        """
        return self.cnxn.llen(self.key)

    def empty(self) -> bool:
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

    def lrange(self, start, end):
        """

        Args:
            start: start index for lrange
            end: end index for lrange

        Returns: all objects inside the range

        """
        return self.cnxn.lrange(self.key, start, end)

    def get(self, block=True, timeout=None):
        """
        Pops using redis lpop
        Args:
            block: If block connection, default: True
            timeout: Sets timeout value, default: None

        Returns: Item at the leftmost in bytes.

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

    def ltrim(self, start, end):
        """

        Args:
            start: start idx of ltrim value
            end: end idx of ltrim value
        """
        self.cnxn.ltrim(self.key, start, end)

    def flushdb(self):
        """
        flushes using flushdb
        """
        self.cnxn.flushdb()

    def get_nowait(self):
        """
        Returns: ¯\_(ツ)_/¯
        """
        return self.get(False)
