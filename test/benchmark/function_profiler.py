"""
This is a custom (and hacky) code profiler that provides a mechanism for
"zero-cost" profiling of very specific library functions.

This allows lightweight function timing wrappers to be injected into the library
at runtime, without polluting the actual source code with profiling/benchmarking
junk.

An alternative to this is to use Python's native cProfile, however this makes
realistic benchmark comparisons impossible for mixed-implementation libraries
where C extension modules exist.
"""

import time
import importlib
from collections import OrderedDict


class Timer:
    def __init__(self, func):
        self.func = func
        self.recurse_counter = 0
        self.start_time = None

        self.total_time = 0.0
        self.n_primary_calls = 0
        self.n_total_calls = 0

    def __enter__(self):
        # Start timer at the first call. Ignore additional starts caused by recursion
        self.n_total_calls += 1
        if self.recurse_counter == 0:
            self.start_time = time.time()
            self.n_primary_calls += 1

        # keep track of recursive calls
        self.recurse_counter += 1

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.recurse_counter -= 1
        if self.recurse_counter == 0:
            # Exited top-most call. Capture total time
            self.total_time += time.time() - self.start_time

class Profiler:
    def __init__(self):
        self.timers: OrderedDict[Timer] = OrderedDict()

    def _wrap_function_in_timer(self, func, label: str):
        timer = Timer(func)
        self.timers[label] = timer

        def wrapper(*args, **kwargs):
            with timer:
                result = func(*args, **kwargs)
            return result
        return wrapper

    def bind_timer(self, module_path: str, function_path: str, label: str) -> None:
        """
        Bind a profiling timer to an internal library function
        """
        # Lookup the module
        module = importlib.import_module(module_path)

        # Lookup the function object from the path
        obj = module
        segments = function_path.split(".")
        for segment in segments:
            parent = obj
            obj = getattr(parent, segment)

        # Wrap the function, and monkey-patch it back in-place
        obj = self._wrap_function_in_timer(obj, label)
        setattr(parent, segments[-1], obj)

    def print_result(self):
        total_time = list(self.timers.values())[0].total_time
        for label, timer in self.timers.items():
            call_str = f"{timer.n_primary_calls}/{timer.n_total_calls}"
            percent = 100* timer.total_time / total_time
            print(f"{label:>15s}: {call_str:10s} {timer.total_time:.5f} ({percent:.1f}%)")
