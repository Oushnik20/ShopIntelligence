import sys
import os
import pandas as pd

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)
from app.database import SessionLocal
from app.models import Transaction

CSV_FILE = "data/pos_transactions_new.csv"

db = SessionLocal()

df = pd.read_csv(CSV_FILE)

inserted = 0

for idx, row in df.iterrows():

    txn_id = f"TXN_{row['order_id']}"

    exists = db.get(
        Transaction,
        txn_id
    )

    if exists:
        continue

    # Combine order_date and order_time for timestamp
    timestamp = f"{row['order_date']} {row['order_time']}"

    # Map store_id: ST1008 -> STORE_BLR_002
    store_id_map = {
        'ST1008': 'STORE_BLR_002',
        'ST1009': 'STORE_BLR_001'
    }
    
    mapped_store = store_id_map.get(
        row['store_id'],
        'STORE_BLR_002'
    )

    txn = Transaction(
        transaction_id=txn_id,
        store_id=mapped_store,
        visitor_id=f"VIS_{idx % 50}",
        timestamp=timestamp,
        amount=float(
            row['total_amount']
        )
    )

    db.add(txn)

    inserted += 1

db.commit()

db.close()

print(
    f"Inserted {inserted} transactions"
)