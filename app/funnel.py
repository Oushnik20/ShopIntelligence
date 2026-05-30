from sqlalchemy.orm import Session
from .models import Event


def get_funnel(
    db: Session,
    store_id: str
):

    events = db.query(Event).filter(
        Event.store_id == store_id,
        Event.is_staff == False
    ).all()

    sessions = {}

    for e in events:

        vid = e.visitor_id

        if vid not in sessions:
            sessions[vid] = {
                "entry": False,
                "zone": False,
                "billing": False,
                "purchase": False
            }

        if e.event_type == "ENTRY":
            sessions[vid]["entry"] = True

        if e.event_type in [
            "ZONE_ENTER",
            "ZONE_DWELL"
        ]:
            sessions[vid]["zone"] = True

        if e.event_type == "BILLING_QUEUE_JOIN":
            sessions[vid]["billing"] = True

        if e.event_type == "PURCHASE":
            sessions[vid]["purchase"] = True

    entry = sum(
        1 for s in sessions.values()
        if s["entry"]
    )

    zone = sum(
        1 for s in sessions.values()
        if s["zone"]
    )

    billing = sum(
        1 for s in sessions.values()
        if s["billing"]
    )

    purchase = sum(
        1 for s in sessions.values()
        if s["purchase"]
    )

    return {
        "entry": entry,
        "zone_visit": zone,
        "billing_queue": billing,
        "purchase": purchase
    }