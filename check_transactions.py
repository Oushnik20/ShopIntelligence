from app.database import SessionLocal
from app.models import Transaction

db = SessionLocal()

print(
    db.query(Transaction).count()
)

db.close()