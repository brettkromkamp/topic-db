# See URL: https://hakibenita.com/fast-load-data-python-postgresql

import time
from functools import wraps

from memory_profiler import memory_usage  # type: ignore


def profile(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        fn_kwargs_str = ", ".join(f"{k}={v}" for k, v in kwargs.items())
        print(f"\n{fn.__name__}({fn_kwargs_str})")

        # Measure time
        t = time.perf_counter()
        return_value = fn(*args, **kwargs)
        elapsed = time.perf_counter() - t
        print(f"Time spent: {elapsed:0.4}")

        # Measure memory
        mem, return_value = memory_usage(
            (fn, args, kwargs), retval=True, timeout=200, interval=1e-7
        )

        print(f"Memory used: {max(mem) - min(mem)}")
        return return_value

    return inner
