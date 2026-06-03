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
    } & visitors

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

    queue_visitors = {
        e.visitor_id
        for e in events
        if e.event_type == "BILLING_QUEUE_JOIN"
    }

    completed_count = len(
        [
            e
            for e in events
            if e.event_type == "BILLING_QUEUE_COMPLETED"
        ]
    )

    abandoned_count = len(
        [
            e
            for e in events
            if e.event_type == "BILLING_QUEUE_ABANDON"
        ]
    )

    queue_times = [
        e.dwell_ms
        for e in events
        if e.event_type == "BILLING_QUEUE_COMPLETED"
        and e.dwell_ms > 0
    ]

    avg_queue_time = 0
    if queue_times:
        avg_queue_time = round(
            sum(queue_times) / len(queue_times) / 1000,
            2
        )

    queue_depth = len(queue_visitors)

    queue_exit_count = completed_count + abandoned_count
    queue_completion_rate = 0
    queue_abandonment_rate = 0

    if queue_exit_count:
        queue_completion_rate = round(
            completed_count / queue_exit_count * 100,
            2
        )
        queue_abandonment_rate = round(
            abandoned_count / queue_exit_count * 100,
            2
        )

    zone_counts = {}
    for e in events:
        if e.event_type in ("ZONE_ENTER", "ZONE_DWELL") and e.zone_id:
            zone_counts[e.zone_id] = zone_counts.get(e.zone_id, 0) + 1

    most_visited_zone = None
    if zone_counts:
        most_visited_zone = max(zone_counts, key=zone_counts.get)

    return {
        "store_id": store_id,
        "unique_visitors": len(visitors),
        "conversion_rate": conversion_rate,
        "avg_dwell_per_zone": avg_dwell,
        "queue_depth": queue_depth,
        "avg_queue_time": avg_queue_time,
        "queue_completed_count": completed_count,
        "queue_abandoned_count": abandoned_count,
        "queue_completion_rate": queue_completion_rate,
        "queue_abandonment_rate": queue_abandonment_rate,
        "most_visited_zone": most_visited_zone,
        "abandonment_rate": queue_abandonment_rate
    }