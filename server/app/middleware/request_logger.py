import logging
import time

from fastapi import Request

logger = logging.getLogger(__name__)


async def request_logging_middleware(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start
    logger.info("%s %s %.3f", request.method, request.url.path, duration)
    return response
