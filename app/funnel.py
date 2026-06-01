from sqlalchemy.orm import Session

from .models import Event
from .models import Transaction


def get_funnel(
    db: Session,
    store_id: str
):

    events = db.query(Event).filter(
        Event.store_id == store_id,
        Event.is_staff == False
    ).all()

    entry_visitors = set()
    zone_visitors = set()
    billing_visitors = set()

    for e in events:

        if e.event_type == "ENTRY":
            entry_visitors.add(e.visitor_id)

        if e.event_type in [
            "ZONE_ENTER",
            "ZONE_DWELL"
        ]:
            zone_visitors.add(e.visitor_id)

        if e.event_type == "BILLING_QUEUE_JOIN":
            billing_visitors.add(e.visitor_id)

    purchase_visitors = {
        t.visitor_id
        for t in db.query(Transaction)
        .filter(
            Transaction.store_id == store_id
        )
        .all()
    }

    purchases = len(
        purchase_visitors
        & entry_visitors
    )

    return {
        "entry": len(entry_visitors),
        "zone_visit": len(zone_visitors),
        "billing_queue": len(billing_visitors),
        "purchase": purchases
    }