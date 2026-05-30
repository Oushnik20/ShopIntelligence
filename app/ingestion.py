from pydantic import BaseModel
from typing import Optional
from typing import Dict


class EventSchema(BaseModel):
    event_id: str
    store_id: str
    camera_id: str
    visitor_id: str
    event_type: str
    timestamp: str
    zone_id: Optional[str] = None
    dwell_ms: int
    is_staff: bool
    confidence: float
    metadata: Dict