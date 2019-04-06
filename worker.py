import os

from threading import Thread


class Worker(Thread):

    def __init__(self, pool):
        """
        This is the start method as part of the constructor
        """
        self.pool = pool
        Thread.__init__(self)
        self.id = self.name

    @property
    def status(self):
        return str(self).split(', ')[-1][:-2]

    def _debug(self, message):
        # Note: this can easily be changed to a logger, but a print is good enough for now
        if not os.getenv('DEBUG', True):
            return

        with self.pool.debug_print_lock:
            print('id: {}, status: {}, message: {}'.format(self.id, self.status, message))

    def terminate_worker(self):
        """
        This method should not be called, since it's force killing the thread.
        A better implementation can be found in the pool "__del__" method to soft kill a thread.
        """
        self._stop()

    def run(self):
        """
        This method executes the the worker
        """
        self._debug('Starting up')
        while True:
            self._debug('Waiting for a job')
            job_func = self.pool.get_task()

            if job_func is None:
                self._debug('Pool has asked me to terminate. Bye!')
                return

            self._debug('Running job: {}'.format(str(job_func)))
            print(job_func())
            self._debug('Finished running job {}'.format(str(job_func)))
