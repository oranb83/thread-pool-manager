import logging
from time import sleep

from pool import Pool
from orchestrator import Orchestrator

logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s'
)

def wait_for_results(pool):
    while not pool.done() or not pool.idle():
        for result in pool.results():
            logging.debug('got result %s', str(result))

    for result in pool.results():
        logging.debug('got result %s', str(result))


def test(x):
    sleep(2)
    logging.debug('%s finished', str(x))
    return x


def test_pool():
    pool = Pool(5)
    logging.debug('queueing work')
    for i in range(10):
        pool.add_task(test, i)
    logging.debug('starting work')
    pool.start_workers(True)
    logging.debug('waiting')
    sleep(5)
    for result in pool.results():
        logging.debug('got result %s', str(result))
    logging.debug('cancel unstarted workers')
    pool.abort()
    logging.debug('waiting and restarting')
    pool.start_workers(True)
    logging.debug('restarted waiting for results')
    wait_for_results(pool)
    logging.debug('adding additional workers')
    for i in range(10, 15):
        pool.add_task(test, i)
    wait_for_results(pool)

    pool.done()

    """
    Test Results:
        (MainThread) queueing work
        (MainThread) starting work
        (MainThread) waiting
        (thread-0  ) 0 finished
        (thread-4  ) 4 finished
        (thread-3  ) 3 finished
        (thread-1  ) 1 finished
        (thread-2  ) 2 finished
        (thread-4  ) 6 finished
        (thread-1  ) 8 finished
        (thread-0  ) 5 finished
        (thread-3  ) 7 finished
        (thread-2  ) 9 finished
        (MainThread) got result 0
        (MainThread) got result 4
        (MainThread) got result 3
        (MainThread) got result 1
        (MainThread) got result 2
        (MainThread) got result 6
        (MainThread) got result 8
        (MainThread) got result 5
        (MainThread) got result 7
        (MainThread) got result 9
        (MainThread) cancel unstarted workers
        (MainThread) waiting and restarting
        (MainThread) restarted waiting for results
        (MainThread) adding additional workers
        (thread-4  ) 12 finished
        (thread-2  ) 11 finished
        (thread-3  ) 13 finished
        (thread-1  ) 14 finished
        (thread-0  ) 10 finished
        (MainThread) got result 12
        (MainThread) got result 11
        (MainThread) got result 13
        (MainThread) got result 14
        (MainThread) got result 10
    """

def test_orchestrator():

    try:
        orchest = Orchestrator()

        # Empty pool prints empty list
        pool = orchest.get_or_create_pool('empty')
        logging.debug('start working and wait for results')
        logging.debug('results: %s', str(orchest.get_results(pool)))

        # New int pool prints 0 to 9
        pool = orchest.get_or_create_pool('int')
        logging.debug('queueing work')
        for i in range(10):
            orchest.add_task(pool, test, i)
        logging.debug('start working and wait for results')
        logging.debug('results: %s', str(orchest.get_results(pool)))

        # New str pool prints a to e
        pool = orchest.get_or_create_pool('str')
        logging.debug('queueing work')
        for i in ['a', 'b', 'c', 'd', 'e']:
            orchest.add_task(pool, test, i)
        logging.debug('start working and wait for results')
        logging.debug('results: %s', str(orchest.get_results(pool)))

        # Existing int pool prints 10 to 19
        pool = orchest.get_or_create_pool('int')
    finally:
        orchest.terminate()
    """
    Test Results:
        (MainThread) creating a new pool "empty"
        (MainThread) start working and wait for results
        (MainThread) results: []
        (MainThread) creating a new pool "int"
        (MainThread) queueing work
        (MainThread) start working and wait for results
        (thread-2  ) 2 finished
        (thread-9  ) 9 finished
        (thread-3  ) 3 finished
        (thread-5  ) 5 finished
        (thread-1  ) 1 finished
        (thread-7  ) 7 finished
        (thread-4  ) 4 finished
        (thread-6  ) 6 finished
        (thread-0  ) 0 finished
        (thread-8  ) 8 finished
        (MainThread) results: [2, 9, 3, 5, 1, 7, 4, 6, 0, 8]
        (MainThread) creating a new pool "str"
        (MainThread) queueing work
        (MainThread) start working and wait for results
        (thread-0  ) a finished
        (thread-1  ) b finished
        (thread-2  ) c finished
        (thread-3  ) d finished
        (thread-4  ) e finished
        (MainThread) results: ['a', 'b', 'c', 'd', 'e']
        (MainThread) pool "int" already exist
    """

if __name__ == '__main__':
    # test_pool()
    test_orchestrator()