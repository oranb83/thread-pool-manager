import os


class Pool(object):

    def __init__(self, min_workers=0, max_workers=10):
        self.resize_lock = RLock()
        self.debug_print_lock = RLock()
        self.job_semaphore = Semaphore(0)
        self.queue = deque()
        self.min_workers = min_workers
        self.available_workers = 0
        self.start_workers(max_workers)

    def __del__(self):
        self.terminate()

    def _debug(self, message):
        """Note: this can easily be changed to a logger, but a print is good enough for now"""
        if not os.getenv('DEBUG', True):
            return

        with self.debug_print_lock:
            print('Pool: {}'.format(message))

    def start_workers(self, max_workers):
        """Init all workers"""
            for i in range(max_workers):
                worker = Worker(self)
                worker.start()
                self.available_workers += 1

    def stop_workers(self, max_workers):
        """Stop workers"""
        self._debug('Stopping {} threads'.format(max_workers))
        with self.resize_lock:
            self.min_workers -= 1
            self.add_task(None)

    def terminate(self):
        """Stop all active workers"""
        self._debug('Terminating')
        with self.resize_lock:
            while self.min_workers > 0:
                self.stop_workers(self.available_workers)

    def add_task(self, func):
        """Add a job"""
        self._debug('Adding job {}'.format(str(func)))
        self.queue.append(func)
        self.job_semaphore.release()

    def get_task(self):
        """
        Called by worker threads to get a job from the queue.

        Note: each worker should call this method from it's own pull.
        """
        self.job_semaphore.acquire()

        if self.min_workers < self.available_workers:
            with self.resize_lock:
                # Defensive approach for double lock, in case another thread
                # already slipped in and acquired a lock on the last thread.
                if self.min_workers < self.available_workers:
                    # Return None to tell the worker thread to exit
                    return None

        return self.queue.popleft()
