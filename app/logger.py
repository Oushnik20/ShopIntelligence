import logging
import time
import uuid

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s"
)

logger = logging.getLogger("store-intelligence")


def make_log(
    endpoint,
    status_code,
    latency_ms,
    store_id=None,
    event_count=None
):
    logger.info({
        "trace_id": str(uuid.uuid4()),
        "endpoint": endpoint,
        "store_id": store_id,
        "event_count": event_count,
        "latency_ms": round(latency_ms, 2),
        "status_code": status_code
    })