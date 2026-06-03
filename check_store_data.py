from app.database import SessionLocal
from app.models import Event, Transaction

db = SessionLocal()

# Check STORE_BLR_001
events = db.query(Event).filter(Event.store_id == 'STORE_BLR_001').all()
transactions = db.query(Transaction).filter(Transaction.store_id == 'STORE_BLR_001').all()

print('STORE_BLR_001 Analysis:')
print(f'Number of events: {len(events)}')
if events:
    print(f'Event visitors: {[e.visitor_id for e in events]}')
    
print(f'\nNumber of transactions: {len(transactions)}')
if transactions:
    print(f'Transaction visitors (first 10): {[t.visitor_id for t in transactions[:10]]}')

# Check what's in STORE_BLR_002
events2 = db.query(Event).filter(Event.store_id == 'STORE_BLR_002').all()
print(f'\nSTORE_BLR_002:')
print(f'Number of events: {len(events2)}')

db.close()
