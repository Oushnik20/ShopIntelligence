from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Boolean
from sqlalchemy import Integer
from sqlalchemy import JSON
from sqlalchemy import Index

from .database import Base


class Event(Base):
    __tablename__ = "events"

    event_id = Column(String, primary_key=True)

    store_id = Column(String, index=True)
    camera_id = Column(String)

    visitor_id = Column(String, index=True)

    event_type = Column(String, index=True)

    timestamp = Column(String, index=True)

    # Zone information
    zone_id = Column(String, nullable=True)
    zone_name = Column(String, nullable=True)
    zone_type = Column(String, nullable=True)
    is_revenue_zone = Column(Boolean, nullable=True)

    # Dwell and engagement
    dwell_ms = Column(Integer)

    # Visitor attributes
    is_staff = Column(Boolean)
    gender = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    age_bucket = Column(String, nullable=True)

    # Group information
    group_id = Column(String, nullable=True)
    group_size = Column(Integer, nullable=True)

    confidence = Column(Float)

    event_metadata = Column(JSON)

    __table_args__ = (
        Index("idx_store_visitor", "store_id", "visitor_id"),
    )

class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(
        String,
        primary_key=True
    )

    store_id = Column(
        String,
        index=True
    )

    visitor_id = Column(
        String,
        index=True
    )

    timestamp = Column(String)

    amount = Column(Float)

