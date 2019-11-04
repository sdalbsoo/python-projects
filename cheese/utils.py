from contextlib import contextmanager
import time

import humanfriendly as hf


@contextmanager
def time_manager(name):
    start_time = time.time()
    yield
    elapsed_time = time.time() - start_time
    print(f"[{name}] finished in {hf.format_timespan(elapsed_time)}")
