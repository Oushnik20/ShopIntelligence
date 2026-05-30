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

    zone_id = Column(String, nullable=True)

    dwell_ms = Column(Integer)

    is_staff = Column(Boolean)

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

