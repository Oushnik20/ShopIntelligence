# Setup & Deployment Guide

Complete step-by-step guide for setting up and deploying Store Intelligence Platform.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Database Setup](#database-setup)
4. [Loading Sample Data](#loading-sample-data)
5. [Docker Deployment](#docker-deployment)
6. [Verification Checklist](#verification-checklist)
7. [Production Deployment](#production-deployment)

---

## Prerequisites

### System Requirements
- **OS**: Windows, macOS, or Linux
- **Python**: 3.11 or higher
- **RAM**: 2GB minimum (4GB recommended)
- **Disk**: 2GB free space (for models and data)
- **Docker** (optional): For containerized deployment

### Check Python Version
```bash
python --version
```

### Install Dependencies
```bash
# Windows/macOS/Linux
pip install --upgrade pip
```

---

## Local Development Setup

### Step 1: Clone/Extract Project

```bash
cd /path/to/store-intelligence
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed fastapi uvicorn sqlalchemy pydantic streamlit 
requests pandas pytest httpx opencv-python-headless ultralytics supervision 
numpy lap scipy
```

### Step 4: Verify Installation

```bash
python -c "import fastapi, streamlit, pandas, torch; print('All imports OK')"
```

---

## Database Setup

### Initialize Database

The SQLite database is automatically created on first API run. To manually initialize:

```bash
python -c "
from app.database import Base, engine
Base.metadata.create_all(bind=engine)
print('Database initialized successfully')
"
```

### Verify Database Creation

```bash
python check_transactions.py
```

Expected output:
```
Transactions in DB: 101
Events in DB: 92
```

### Reset Database (Clean Slate)

```bash
# Delete existing database
rm store.db

# Initialize fresh
python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"
```

---

## Loading Sample Data

### Option 1: Load Pre-Generated Events

```bash
# Step 1: Generate events (if pipeline videos available)
python pipeline/run_store2_zone.py

# Step 2: Ingest events to API
python scripts/load_events.py
```

### Option 2: Load POS Transactions

```bash
python scripts/load_transactions.py
```

**Output:**
```
Inserted 101 transactions
```

### Option 3: Load Both (Recommended)

```bash
# Terminal 1: Start API
uvicorn app.main:app --reload

# Terminal 2: Load data
python scripts/load_transactions.py
python scripts/load_events.py
```

### Verify Data Loaded

```bash
python -c "
from app.database import SessionLocal
from app.models import Event, Transaction

db = SessionLocal()
events = db.query(Event).count()
transactions = db.query(Transaction).count()
print(f'Events: {events}, Transactions: {transactions}')
db.close()
"
```

---

## Running the Full Stack

### Terminal Setup (3 terminals recommended)

**Terminal 1: API Backend**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
- Runs on: `http://localhost:8000`
- Swagger Docs: `http://localhost:8000/docs`

**Terminal 2: Load Data** (one-time)
```bash
python scripts/load_transactions.py
python scripts/load_events.py
```

**Terminal 3: Streamlit Dashboard**
```bash
streamlit run dashboard/app.py
```
- Runs on: `http://localhost:8501`
- Select store: `STORE_BLR_002` (contains all sample data)

---

## Docker Deployment

### Prerequisites
- Docker installed and running
- Docker Compose installed

### Build Container

```bash
docker build -t store-intelligence .
```

### Run with Docker Compose

```bash
docker-compose up --build
```

**What starts:**
- FastAPI on `http://localhost:8000`
- Streamlit on `http://localhost:8501`
- SQLite database at `/app/store.db`

### Access Services

```bash
# API
curl http://localhost:8000/health

# Dashboard (in browser)
http://localhost:8501
```

### Stop Containers

```bash
docker-compose down
```

### View Logs

```bash
docker-compose logs -f api
```

---

## Verification Checklist

Use this checklist to verify complete setup:

### Database ✅
- [ ] `store.db` file exists
- [ ] `python check_transactions.py` returns event/transaction counts
- [ ] No database errors in logs

### API Backend ✅
- [ ] `uvicorn app.main:app --reload` starts without errors
- [ ] `http://localhost:8000/health` returns 200 status
- [ ] `http://localhost:8000/docs` shows Swagger UI
- [ ] All 7 endpoints accessible:
  - GET `/`
  - GET `/health`
  - POST `/events/ingest`
  - GET `/stores/{store_id}/metrics`
  - GET `/stores/{store_id}/funnel`
  - GET `/stores/{store_id}/anomalies`
  - GET `/stores/{store_id}/revenue`

### Tests ✅
- [ ] `python -m pytest tests/ -v` returns 5 passed
- [ ] All test files pass:
  - `test_ingest.py`
  - `test_metrics.py`
  - `test_funnel.py`
  - `test_anomalies.py`

### Dashboard ✅
- [ ] `streamlit run dashboard/app.py` starts
- [ ] Dashboard loads at `http://localhost:8501`
- [ ] Store selector shows `STORE_BLR_001` and `STORE_BLR_002`
- [ ] Metrics cards display (8 cards visible)
- [ ] Conversion funnel chart renders
- [ ] Zone dwell time chart renders
- [ ] Anomalies section shows alerts (if any)

### Data ✅
- [ ] STORE_BLR_002 shows:
  - Visitors: 50
  - Conversion: 90.0%
  - Queue Depth: 11
  - Most Visited Zone: ZONE_1

---

## Production Deployment

### Environment Setup

Create `.env` file:
```
API_HOST=0.0.0.0
API_PORT=8000
DATABASE_URL=sqlite:///store.db
LOG_LEVEL=INFO
```

### Scale API

```bash
# Using Gunicorn (multiple workers)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app.main:app
```

### Database Backup

```bash
# Backup SQLite database
cp store.db store.db.backup

# Schedule regular backups (cron job)
# 0 2 * * * /path/to/backup.sh
```

### SSL/HTTPS

Update `docker-compose.yml` to use reverse proxy (nginx):
```yaml
services:
  nginx:
    image: nginx:latest
    ports:
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
```

### Monitoring

```bash
# Check API health regularly
curl -I http://localhost:8000/health

# Monitor logs
tail -f logs/api.log
```

### Scaling Considerations

- **Horizontal**: Run multiple API instances behind load balancer
- **Vertical**: Increase server RAM/CPU for video processing
- **Database**: Consider PostgreSQL for production instead of SQLite
- **Caching**: Add Redis for dashboard query results

---

## Troubleshooting Setup

### Python version mismatch
```bash
# Verify Python 3.11+
python --version

# Use explicit version if available
python3.11 -m venv venv
```

### Permission errors
```bash
# Windows: Run terminal as Administrator
# Linux/macOS: Use sudo or check folder permissions
chmod -R 755 /path/to/store-intelligence
```

### Port already in use
```bash
# Check what's using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Use different port
uvicorn app.main:app --port 8001
```

### Import errors
```bash
# Reinstall all dependencies
pip install -r requirements.txt --force-reinstall

# Clear pip cache
pip cache purge
```

### Database locked error
```bash
# Close all connections and restart
rm store.db
python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"
```

---

## Next Steps

1. ✅ Complete setup verification checklist
2. ✅ Load sample data (`scripts/load_transactions.py`)
3. ✅ Run tests (`python -m pytest tests/ -v`)
4. ✅ Open dashboard (`http://localhost:8501`)
5. ✅ Select STORE_BLR_002 and view analytics
6. 📚 Read [DESIGN.md](docs/DESIGN.md) for architecture details
7. 📚 Read [CHOICES.md](docs/CHOICES.md) for engineering rationale

---

## Support

For issues:
1. Check [README.md](README.md) Troubleshooting section
2. Review test files for API usage examples
3. Check Swagger docs: `http://localhost:8000/docs`
4. Inspect `store.db` with SQLite client
