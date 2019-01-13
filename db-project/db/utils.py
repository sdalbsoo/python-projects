from contextlib import contextmanager
import time

import humanfriendly as hf
from loguru import logger


@contextmanager
def timeit_context(name):
    startTime = time.time()
    yield
    elapsedTime = time.time() - startTime
    logger.info("[{}] finished in {}".format(
        name, hf.format_timespan(elapsedTime)))
