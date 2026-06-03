from sqlalchemy.orm import Session
from .models import Transaction


def get_revenue_metrics(
    db: Session,
    store_id: str
):

    txns = db.query(
        Transaction
    ).filter(
        Transaction.store_id == store_id
    ).all()

    total_revenue = round(
        sum(t.amount for t in txns),
        2
    )

    total_orders = len(txns)

    avg_basket = 0

    if total_orders:
        avg_basket = round(
            total_revenue / total_orders,
            2
        )

    return {
        "store_id": store_id,
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "avg_basket_value": avg_basket
    }