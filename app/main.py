from fastapi import FastAPI
from sqlalchemy.orm import Session

from .database import Base
from .database import engine
from .database import SessionLocal

from .models import Event
from .ingestion import EventSchema

from .metrics import get_metrics
from .health import get_health
from .anomalies import get_anomalies
from .funnel import get_funnel
from .middleware import LoggingMiddleware
from .exceptions import generic_exception_handler

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    LoggingMiddleware
)
app.add_exception_handler(
    Exception,
    generic_exception_handler
)

@app.post("/events/ingest")
def ingest(events: list[EventSchema]):

    db: Session = SessionLocal()

    inserted = 0

    for e in events:

        exists = db.get(Event, e.event_id)

        if exists:
            continue

        # row = Event(**e.model_dump())
        data = e.model_dump()

        data["event_metadata"] = data.pop("metadata")

        row = Event(**data)

        db.add(row)

        inserted += 1

    db.commit()

    db.close()

    return {
        "inserted": inserted
    }


@app.get("/stores/{store_id}/metrics")
def metrics(store_id: str):

    db = SessionLocal()

    result = get_metrics(db, store_id)

    db.close()

    return result

@app.get("/stores/{store_id}/funnel")
def funnel(store_id: str):

    db = SessionLocal()

    result = get_funnel(
        db,
        store_id
    )

    db.close()

    return result


@app.get("/stores/{store_id}/anomalies")
def anomalies(store_id: str):

    return get_anomalies()


@app.get("/health")
def health():

    db = SessionLocal()

    result = get_health(db)

    db.close()

    return result