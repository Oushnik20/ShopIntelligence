from pydantic import BaseModel
from typing import Optional
from typing import Dict


# Mapping of external event types to internal event types
EVENT_TYPE_MAPPING = {
    # New event types
    "entry": "ENTRY",
    "exit": "EXIT",
    "zone_entered": "ZONE_ENTER",
    "zone_exited": "ZONE_EXIT",
    "queue_completed": "BILLING_QUEUE_COMPLETED",
    "queue_abandoned": "BILLING_QUEUE_ABANDON",
    
    # Old internal types (backward compatibility)
    "ENTRY": "ENTRY",
    "EXIT": "EXIT",
    "ZONE_ENTER": "ZONE_ENTER",
    "ZONE_EXIT": "ZONE_EXIT",
    "ZONE_DWELL": "ZONE_DWELL",
    "BILLING_QUEUE_JOIN": "BILLING_QUEUE_JOIN",
    "BILLING_QUEUE_ABANDON": "BILLING_QUEUE_ABANDON",
    "BILLING_QUEUE_COMPLETED": "BILLING_QUEUE_COMPLETED",
}


def normalize_event_type(
    incoming_type: str
) -> str:
    """
    Convert incoming event type to internal format.
    Maintains backward compatibility for old internal types.
    
    Args:
        incoming_type: The event type from the incoming payload
        
    Returns:
        The normalized internal event type
    """
    normalized = incoming_type.lower().strip()
    
    if normalized in EVENT_TYPE_MAPPING:
        return EVENT_TYPE_MAPPING[normalized]
    
    # If not found, return uppercase as fallback
    # (backward compatibility for any unmapped types)
    return incoming_type.upper()


class EventSchema(BaseModel):
    event_id: str
    store_id: str
    camera_id: str
    visitor_id: str
    event_type: str
    timestamp: str
    
    # Zone information
    zone_id: Optional[str] = None
    zone_name: Optional[str] = None
    zone_type: Optional[str] = None
    is_revenue_zone: Optional[bool] = None
    
    # Dwell and engagement
    dwell_ms: int
    
    # Visitor attributes
    is_staff: bool
    gender: Optional[str] = None
    age: Optional[int] = None
    age_bucket: Optional[str] = None
    
    # Group information
    group_id: Optional[str] = None
    group_size: Optional[int] = None
    
    confidence: float
    metadata: Dict