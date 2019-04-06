from queue import Queue
from threading import Thread


class Worker(Thread):
    """Worker extends theimplementation of threads"""
    def __init__(self, name, queue, results, abort, idle, exception_handler):
        Thread.__init__(self)
        self.name = name
        self.queue = queue
        self.results = results
        self.abort = abort
        self.idle = idle
        self.exception_handler = exception_handler
        self.daemon = True
        self.start()

    def run(self):
        """Run Forever, unless the abort signal is triggered"""
        while not self.abort.is_set():
            try:
                func, args, kwargs = self.queue.get(False)
                self.idle.clear()
            except:
                self.idle.set()
                continue

            try:
                result = func(*args, **kwargs)
                if result is not None:
                    self.results.put(result)
            except Exception as e:
                self.exception_handler(self.name, e, args, kwargs)
            finally:
                self.queue.task_done()
