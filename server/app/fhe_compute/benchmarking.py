from contextlib import contextmanager
from time import perf_counter
from typing import Iterator


@contextmanager
def measure_operation() -> Iterator[dict[str, float]]:
    result = {"elapsed_seconds": 0.0}
    start = perf_counter()
    try:
        yield result
    finally:
        result["elapsed_seconds"] = perf_counter() - start
