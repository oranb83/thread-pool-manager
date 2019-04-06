import logging

from time import sleep

from pool import Pool

logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s'
)


class Orchestrator(object):
    """
    Thread pools manager

    Note:
        this class only implement the api requirements, nothing more,
        but can easily be extended.
    """
    def __init__(self):
        # Pool of threads, one for each type
        self.pools = dict()

    def __del__(self):
        self.terminate()

    def get_or_create_pool(self, _type, max_workers=10):
        """
        Get or create pool by type

        @type _type: str
        @param _type: pool type
        @type max_workers: int
        @param max_workers: amount of pool workers

        @rtype: Pool
        @return: Pool
        """
        if _type in self.pools:
            logging.debug('pool "%s" already exist', _type)
            return self.pools[_type]

        pool = Pool(max_workers)
        logging.debug('creating a new pool "%s"', _type)
        self.pools[_type] = pool
        return pool

    def add_task(self, pool, task, *args):
        """
        Add task by exposing the pool interface

        @type pool: Pool
        @param pool: thread pool
        @type task: func
        @param task: send task to the queue for processing
        """
        pool.add_task(task, *args)

    def get_results(self, pool, wait=3):
        """
        Run the thread pool and get results

        @type pool: Pool
        @param pool: thread pool
        @rtype: list
        @return: pool results after workers are completed
        """
        # TODO: workers should be triggered upon new tasks to enable faster response, but it
        #       was not done due to Python implementation of threads which adds additional complexity.
        pool.start_workers(True)
        sleep(wait)
        while not pool.done() or not pool.idle():
            return self._print_results(pool)

        return self._print_results(pool)

    def _print_results(self, pool):
        return [result for result in pool.results()]

    def terminate(self):
        for pool in self.pools.keys():
            self.pools[pool].done()
