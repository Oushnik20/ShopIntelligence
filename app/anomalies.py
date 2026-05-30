from sqlalchemy.orm import Session

from .models import Event


def get_anomalies(
    db: Session,
    store_id: str
):

    events = db.query(Event).filter(
        Event.store_id == store_id,
        Event.is_staff == False
    ).all()

    anomalies = []

    queue_count = len(
        [
            e
            for e in events
            if e.event_type ==
            "BILLING_QUEUE_JOIN"
        ]
    )

    if queue_count >= 5:

        anomalies.append(
            {
                "type": "QUEUE_SPIKE",
                "severity": "WARN",
                "suggested_action":
                    "Open additional billing counter"
            }
        )

    zone_events = len(
        [
            e
            for e in events
            if e.event_type ==
            "ZONE_ENTER"
        ]
    )

    if zone_events == 0:

        anomalies.append(
            {
                "type": "DEAD_ZONE",
                "severity": "INFO",
                "suggested_action":
                    "Check zone visibility"
            }
        )

    visitors = len(
        set(
            e.visitor_id
            for e in events
        )
    )

    purchases = len(
        [
            e
            for e in events
            if e.event_type ==
            "PURCHASE"
        ]
    )

    conversion_rate = 0

    if visitors:
        conversion_rate = (
            purchases /
            visitors
        ) * 100

    if visitors >= 5 and conversion_rate < 10:

        anomalies.append(
            {
                "type": "CONVERSION_DROP",
                "severity": "CRITICAL",
                "suggested_action":
                    "Investigate customer journey"
            }
        )

    return {
        "store_id": store_id,
        "anomalies": anomalies
    }