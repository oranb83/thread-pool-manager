from queue import Queue
from threading import Thread, Event
from sys import stdout, stderr
from time import sleep
from worker import Worker


#default exception handler. if you want to take some action on failed tasks
#maybe add the task back into the queue, then make your own handler and pass it in
def default_handler(name, exception, *args, **kwargs):
    print('%s raised %s with args %s and kwargs %s', name, str(exception), repr(args), repr(kwargs))

#class for thread pool
class Pool(object):
    """Pool of threads consuming tasks from a queue"""
    def __init__(self, max_workers, batch_mode=False, exception_handler=default_handler):
        """Workers constructor"""
        # block when adding tasks if no threads available to process
        self.queue = Queue(thread_count if batch_mode else 0)

        self.result_queue = Queue(0)
        self.thread_count = max_workers
        self.exception_handler = exception_handler
        self.aborts = []
        self.idles = []
        self.workers = []


    def __del__(self):
        """Workers destructor"""
        self.abort()

    def start_workers(self, block=False):
        # Wait for threads to finish
        if block:
            while self.alive():
                sleep(1)
        elif self.alive():
            return False

        # Start threads
        self.aborts = []
        self.idles = []
        self.workers = []
        for n in range(self.thread_count):
            abort = Event()
            idle = Event()
            self.aborts.append(abort)
            self.idles.append(idle)
            self.workers.append(Worker('thread-%d' % n, self.queue, self.result_queue, abort, idle, self.exception_handler))

        return True

    def add_task(self, func, *args, **kargs):
        """Add a task to the queue"""
        self.queue.put((func, args, kargs))

    def abort(self, block=False):
        """
        Terminat all workers

        @type block: bool
        @param block: block while thread is still running
        """

        # Tell the threads to stop after they are done with what they are currently doing
        for a in self.aborts:
            a.set()
        # Wait for them to finish if requested
        while block and self.alive():
            sleep(1)

    def alive(self):
        """
        Check if workers are running

        @rtype: bool
        @return: True if all workers are running
        """
        return True in [t.is_alive() for t in self.workers]

    def idle(self):
        """
        Check if workers are idle

        @rtype: bool
        @return: True if all workers are idle
        """
        return False not in [i.is_set() for i in self.idles]

    def done(self):
        """
        Check if all tasks have been completed

        @rtype: bool
        @return: True if queue is empty (has no tasks)
        """
        return self.queue.empty()

    def results(self, wait=0):
        """
        Get the set of results that have been processed

        @type wait: int
        @param wait: seconds to wait before operation is triggered
        @rtype: bool
        @return: True if queue is empty (has no tasks)
        """
        sleep(wait)
        results = []
        try:
            while True:
                results.append(self.result_queue.get(False))
                self.result_queue.task_done()
                sleep(0.1)
        except:
            pass

        return results
