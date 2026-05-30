from collections import defaultdict

from sqlalchemy.orm import Session

from .models import Event
from .models import Transaction


def get_metrics(
    db: Session,
    store_id: str
):

    events = db.query(Event).filter(
        Event.store_id == store_id,
        Event.is_staff == False
    ).all()

    visitors = {
        e.visitor_id
        for e in events
    }

    transactions = db.query(
        Transaction
    ).filter(
        Transaction.store_id == store_id
    ).all()

    converted_visitors = {
        t.visitor_id
        for t in transactions
    }

    conversion_rate = 0

    if visitors:
        conversion_rate = round(
            (
                len(converted_visitors)
                /
                len(visitors)
            ) * 100,
            2
        )

    dwell = defaultdict(list)

    for e in events:

        if (
            e.zone_id
            and
            e.dwell_ms > 0
        ):
            dwell[e.zone_id].append(
                e.dwell_ms
            )

    avg_dwell = {}

    for zone, vals in dwell.items():

        avg_dwell[zone] = round(
            sum(vals) / len(vals) / 1000,
            2
        )

    queue_depth = len(
        [
            e
            for e in events
            if e.event_type ==
            "BILLING_QUEUE_JOIN"
        ]
    )

    abandoned = len(
        [
            e
            for e in events
            if e.event_type ==
            "BILLING_QUEUE_ABANDON"
        ]
    )

    abandonment_rate = 0

    if queue_depth:
        abandonment_rate = round(
            abandoned
            /
            queue_depth
            *
            100,
            2
        )

    return {
        "store_id": store_id,
        "unique_visitors": len(visitors),
        "conversion_rate": conversion_rate,
        "avg_dwell_per_zone": avg_dwell,
        "queue_depth": queue_depth,
        "abandonment_rate": abandonment_rate
    }