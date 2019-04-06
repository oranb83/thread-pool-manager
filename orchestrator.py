from pool import Pool


class Orchestrator(object):
    def __init__(self):
        self.pools = set()

    @property
    def get_or_create_pool(self, _type):
        if _type in self.pools:
            return self.pools['type']

        pool = Pool(_type)
        self.pools.add(pool)
        return pool

    def run(self, _type, task):
        self.get_or_create_pool(_type).add_task(task)
