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

CSV_FILE = "data/pos_transactions.csv"

db = SessionLocal()

df = pd.read_csv(CSV_FILE)

inserted = 0

for idx, row in df.iterrows():

    txn_id = f"TXN_{idx}"

    exists = db.get(
        Transaction,
        txn_id
    )

    if exists:
        continue

    txn = Transaction(
        transaction_id=txn_id,
        store_id="STORE_BLR_002",
        visitor_id=f"VIS_{idx % 50}",
        timestamp=str(
            row.iloc[0]
        ),
        amount=float(
            row.iloc[-1]
        )
    )

    db.add(txn)

    inserted += 1

db.commit()

db.close()

print(
    f"Inserted {inserted} transactions"
)