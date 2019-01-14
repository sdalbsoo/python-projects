from contextlib import contextmanager
import time

import humanfriendly as hf


@contextmanager
def timeit_context(name):
    startTime = time.time()
    yield
    elapsedTime = time.time() - startTime
    print("[{}] finished in {}".format(
        name, hf.format_timespan(elapsedTime)))
