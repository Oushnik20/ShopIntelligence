import time

from starlette.middleware.base import BaseHTTPMiddleware

from .logger import make_log


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(
        self,
        request,
        call_next
    ):

        start = time.time()

        response = await call_next(request)

        latency = (time.time() - start) * 1000

        make_log(
            endpoint=request.url.path,
            status_code=response.status_code,
            latency_ms=latency
        )

        return response