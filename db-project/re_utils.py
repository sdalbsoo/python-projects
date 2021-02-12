import time
from contextlib import contextmanager


@contextmanager
def timeit_context(name):
    startTime = time.time()
    yield
    running_time = time.time() - startTime
    print("[{}] finished in {}".format(
        name, running_time))
