import pandas as pd
from app.database import SessionLocal
from app.models import Transaction

db = SessionLocal()

# Load CSV
df = pd.read_csv('data/pos_transactions_new.csv')

# Map some transactions to STORE_BLR_001
inserted = 0
for idx, row in df.iterrows():
    # Create transaction with STORE_BLR_001
    txn_id = f'TXN_{row["order_id"]}_BLR001'
    
    timestamp = f"{row['order_date']} {row['order_time']}"
    
    txn = Transaction(
        transaction_id=txn_id,
        store_id='STORE_BLR_001',
        visitor_id=f'VIS_{idx % 50}',
        timestamp=timestamp,
        amount=float(row['total_amount'])
    )
    
    db.add(txn)
    inserted += 1
    
    if inserted >= 50:
        break

db.commit()
print(f'Added {inserted} transactions for STORE_BLR_001')
db.close()
