# Store Intelligence Platform

**AI-powered retail analytics platform** that transforms CCTV video streams and POS transactions into actionable business intelligence for retail operations.

## Overview

This platform processes multi-camera retail store footage to generate real-time visitor analytics, dwell-time metrics, queue monitoring, conversion funnels, and operational anomaly detection.

**Architecture**: YOLOv8 (person detection) → ByteTrack (visitor tracking) → Event generation → SQLite persistence → FastAPI backend → Streamlit dashboard

**Status**: ✅ Production Ready - All features implemented, tested, and verified working

---

## Supported Stores

- `STORE_BLR_001` (existing implementation)
- `STORE_BLR_002` (new Store 2 support)

Store-specific camera coordinates are loaded from:

- `configs/store1.json`
- `configs/store2.json`

---

## Features

### Visitor Analytics
- Visitor counting
- Unique visitor tracking
- Entry and exit detection

### Zone Analytics
- Zone entry, dwell, and exit tracking
- Most visited zone reporting

### Queue Monitoring
- Billing queue join detection
- Queue completion and abandonment tracking
- Average queue time, completion, and abandonment rates

### Conversion Analytics
- Visitor → Zone → Billing → Purchase funnel
- Conversion rate calculation
- POS transaction integration

### Anomaly Detection
- Queue spike detection
- Dead zone detection
- Conversion drop alerts

### Platform Features
- Multi-store support
- REST APIs
- SQLite persistence
- Docker deployment
- Streamlit dashboard with store selector
- Automated tests

---

## Architecture

```

CCTV Cameras
(Store 1 and Store 2 runners)
↓
YOLOv8 Detection
↓
ByteTrack Tracking
↓
Event Generation
↓
SQLite Database
↓
FastAPI Backend
↓
Streamlit Dashboard

```

---

## Camera Responsibilities

### Store 1
- `pipeline/run_cam3.py` → Entry Analytics
- `pipeline/run_cam1_cam2.py` → Zone Analytics
- `pipeline/run_cam5.py` → Billing Queue Analytics

### Store 2
- `pipeline/run_store2_entry1.py` → Entry Camera 1
- `pipeline/run_store2_entry2.py` → Entry Camera 2
- `pipeline/run_store2_zone.py` → Zone Camera
- `pipeline/run_store2_billing.py` → Billing Camera

---

## Event Types

| Event Type | Description |
|------------|-------------|
| ENTRY | Visitor crosses entry line |
| EXIT | Visitor exits through entry line |
| ZONE_ENTER | Visitor enters a monitored zone |
| ZONE_DWELL | Visitor spends time in a zone |
| ZONE_EXIT | Visitor leaves a monitored zone |
| BILLING_QUEUE_JOIN | Visitor enters billing queue |
| BILLING_QUEUE_COMPLETED | Visitor completes queue and exits billing |
| BILLING_QUEUE_ABANDON | Visitor leaves billing queue early |

---

## Event Schema

Every generated event includes:

- `store_id`
- `camera_id`
- `event_type`
- `visitor_id`
- `timestamp`

Optional fields include:

- `gender`
- `age`
- `age_bucket`
- `group_id`
- `group_size`
- `zone_name`
- `zone_type`
- `is_revenue_zone`

---

## Technology Stack

### Backend
- FastAPI
- SQLAlchemy
- SQLite

### Computer Vision
- YOLOv8
- ByteTrack
- OpenCV

### Dashboard
- Streamlit

### Testing
- Pytest

### Deployment
- Docker
- Docker Compose

---

## APIs

### Complete REST API Endpoints

#### 1. Ingest Events
**POST** `/events/ingest`

Ingests visitor events from CCTV pipeline.

Request body (array):
```json
[{
  "event_id": "ENTRY_123_1234567890",
  "store_id": "STORE_BLR_002",
  "camera_id": "CAM_ZONE_1",
  "visitor_id": "VIS_42",
  "event_type": "ENTRY",
  "timestamp": "2026-06-03T14:22:10Z",
  "zone_id": null,
  "dwell_ms": 0,
  "is_staff": false,
  "confidence": 0.95,
  "metadata": {}
}]
```

Response:
```json
{"inserted": 1}
```

---

#### 2. Get Store Metrics
**GET** `/stores/{store_id}/metrics`

Returns 11 key performance indicators.

Example: `http://localhost:8000/stores/STORE_BLR_002/metrics`

Response:
```json
{
  "unique_visitors": 50,
  "conversion_rate": 90.0,
  "avg_dwell_per_zone": {"ZONE_1": 5.23},
  "queue_depth": 11,
  "avg_queue_time": 45,
  "queue_completed_count": 8,
  "queue_abandoned_count": 0,
  "queue_completion_rate": 100.0,
  "queue_abandonment_rate": 0.0,
  "most_visited_zone": "ZONE_1",
  "abandonment_rate": 0.0
}
```

---

#### 3. Get Conversion Funnel
**GET** `/stores/{store_id}/funnel`

Tracks visitor progression through 4-stage funnel.

Response:
```json
{
  "entry": 46,
  "zone_visit": 22,
  "billing_queue": 11,
  "purchase": 41
}
```

---

#### 4. Get Anomalies
**GET** `/stores/{store_id}/anomalies`

Real-time operational alerts.

Response:
```json
{
  "store_id": "STORE_BLR_002",
  "anomalies": [
    {
      "type": "QUEUE_SPIKE",
      "severity": "WARN",
      "suggested_action": "Open additional billing counter"
    },
    {
      "type": "DEAD_ZONE",
      "severity": "INFO",
      "suggested_action": "Check zone visibility"
    }
  ]
}
```

---

#### 5. Get Revenue Metrics
**GET** `/stores/{store_id}/revenue`

POS transaction analytics.

Response:
```json
{
  "total_revenue": 47828.94,
  "order_count": 101,
  "avg_basket_value": 473.55
}
```

---

#### 6. Health Check
**GET** `/health`

Service status and last event timestamp.

Response:
```json
{
  "status": "healthy",
  "last_event_timestamp": "2026-06-03T14:22:49.248123"
}
```

---

#### 7. Root Info
**GET** `/`

Service information.

Response:
```json
{
  "service": "Store Intelligence API",
  "version": "1.0",
  "status": "operational"
}
```

---

## Metrics

The platform calculates:

- Unique Visitors
- Conversion Rate
- Average Dwell Time
- Queue Depth
- Average Queue Time
- Queue Completed Count
- Queue Abandoned Count
- Queue Completion Rate
- Queue Abandonment Rate
- Most Visited Zone

---

## Running the Project

### Prerequisites
- Python 3.11+
- Docker & Docker Compose (optional, for containerized deployment)
- 2GB+ RAM
- CCTV videos or test pipeline scripts

### Local Setup

**1. Create Virtual Environment:**
```bash
python -m venv venv
```

**2. Activate Environment:**

Windows:
```bash
venv\Scripts\activate
```

macOS/Linux:
```bash
source venv/bin/activate
```

**3. Install Dependencies:**
```bash
pip install -r requirements.txt
```

**4. Start Backend API** (in terminal 1):
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
✅ API runs on `http://localhost:8000`
✅ Swagger docs: `http://localhost:8000/docs`

**5. Load Sample Data** (in terminal 2):
```bash
# Load POS transactions
python scripts/load_transactions.py

# Or load pre-generated events
python scripts/load_events.py
```

**6. Run Dashboard** (in terminal 3):
```bash
streamlit run dashboard/app.py
```
✅ Dashboard opens at `http://localhost:8501`
✅ Select store **STORE_BLR_002** (contains all sample data)

### Docker Deployment

**Build & Run with Docker Compose:**
```bash
docker-compose up --build
```
- Backend: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_metrics.py -v

# Quick test run
python -m pytest tests/ -q
```

**Expected Output**: ✅ 5 passed tests
- test_ingest.py - Event ingestion endpoint
- test_metrics.py - Metrics & health endpoints  
- test_funnel.py - Conversion funnel tracking
- test_anomalies.py - Anomaly detection

### Generate Events from Video

**Example: Process Store 2 Zone Video**
```bash
python pipeline/run_store2_zone.py
```

Supported pipelines:
- `pipeline/run_store2_entry1.py` - Entry camera 1
- `pipeline/run_store2_entry2.py` - Entry camera 2
- `pipeline/run_store2_zone.py` - Zone monitoring
- `pipeline/run_store2_billing.py` - Billing queue
- `pipeline/run_cam1_cam2.py` - Store 1 zones
- `pipeline/run_cam3.py` - Store 1 entry
- `pipeline/run_cam5.py` - Store 1 billing

Events are saved to `pipeline/generated_events.jsonl` and can be ingested via:
```bash
python scripts/load_events.py
```


Triggered when:

```
queue_count >= 5
```

Recommended Action:

```
Open additional billing counter
```

### Dead Zone

Triggered when:

```
zone_entries == 0 (during business hours)
```

Recommended Action:

```
Check zone visibility / camera calibration
```

### Conversion Drop

Triggered when:

```
conversion_rate < 10% AND unique_visitors >= 5
```

Recommended Action:

```
Investigate customer journey bottlenecks
```

---

## Store Layout

The store layout is modeled as logical business zones.

Examples:

* Entry Zone
* Product Display Area
* Makeup Testing Area
* Billing Counter

This enables camera-independent analytics.

---

## Screenshots

### Dashboard

The Streamlit dashboard provides real-time store analytics including visitor metrics, conversion funnel, dwell analysis, and anomaly monitoring.

![Dashboard](docs/dashboard.png)

---

### API Documentation

Interactive FastAPI Swagger documentation exposing all analytics endpoints.

![Swagger](docs/swagger.png)

---

### Entry Detection (CAM3)

YOLOv8 and ByteTrack are used to detect and track visitors entering the store through the main entrance.

![Entry Detection](docs/cam3.png)

---

### Queue Monitoring (CAM5)

Billing area monitoring with queue-zone detection used for queue depth analytics and anomaly generation.

![Queue Monitoring](docs/cam5.png)

---

## Sample Outputs

### STORE_BLR_002 (Production Data - Sample Run)

**Metrics:**
- Unique Visitors: **50**
- Conversion Rate: **90.0%**
- Queue Depth: **11**
- Average Zone Dwell Time: **5.23 seconds**
- Most Visited Zone: **ZONE_1**
- Queue Completion Rate: **100%**
- Active Anomalies: **2** (Queue Spike, Dead Zone)

**Conversion Funnel:**
- Entry: 46 visitors
- Zone Visit: 22 visitors (47.8% → Zone)
- Billing Queue: 11 visitors (50% → Queue)
- Purchase: 41 visitors (89.1% → Purchase)

**Revenue Metrics:**
- Total Revenue: **₹47,828.94**
- Order Count: **101**
- Average Basket Value: **₹473.55**

---

## Configuration

### Store Geometry (Zone Polygons)

Store configurations are loaded from JSON files:

**configs/store1.json:**
```json
{
  "entry_line": [900],
  "zone_polygon": [[0,0],[1920,0],[1920,1080],[0,1080]],
  "queue_polygon": [[450,250],[1400,250],[1400,1080],[450,1080]]
}
```

**configs/store2.json:**
```json
{
  "entry_line": [900, 900],
  "zone_polygon": [[0,0],[1920,0],[1920,1080],[0,1080]],
  "queue_polygon": [[450,250],[1400,250],[1400,1080],[450,1080]]
}
```

Update these coordinates to match your store layout.

---

## Project Structure

```
store-intelligence/
├── app/                          # FastAPI backend
│   ├── main.py                  # REST API endpoints
│   ├── models.py                # SQLAlchemy ORM models
│   ├── database.py              # Database configuration
│   ├── ingestion.py             # Event schema & validation
│   ├── metrics.py               # Analytics calculations (11 KPIs)
│   ├── funnel.py                # Conversion funnel tracking
│   ├── anomalies.py             # Anomaly detection rules
│   ├── revenue.py               # POS transaction analytics
│   ├── health.py                # Service health status
│   ├── middleware.py            # Request logging & tracing
│   ├── logger.py                # Structured JSON logging
│   └── exceptions.py            # Global error handling
│
├── dashboard/                    # Streamlit frontend
│   └── app.py                   # Analytics dashboard UI
│
├── pipeline/                     # Computer vision pipeline
│   ├── detector.py              # YOLOv8 person detection
│   ├── tracker.py               # ByteTrack multi-object tracking
│   ├── event_generator.py       # Event creation & persistence
│   ├── store_config.py          # Store geometry loading
│   ├── generated_events.jsonl   # Generated events file
│   ├── run_cam1_cam2.py         # Store 1 zone camera
│   ├── run_cam3.py              # Store 1 entry camera
│   ├── run_cam5.py              # Store 1 billing queue camera
│   ├── run_store2_entry1.py     # Store 2 entry camera 1
│   ├── run_store2_entry2.py     # Store 2 entry camera 2
│   ├── run_store2_zone.py       # Store 2 zone camera
│   └── run_store2_billing.py    # Store 2 billing camera
│
├── scripts/                      # Utility scripts
│   ├── load_events.py           # Ingest generated events to API
│   └── load_transactions.py     # Load POS CSV to database
│
├── tests/                        # Unit tests (all passing ✅)
│   ├── test_ingest.py           # Event ingestion tests
│   ├── test_metrics.py          # Metrics & health tests
│   ├── test_funnel.py           # Funnel tests
│   └── test_anomalies.py        # Anomaly tests
│
├── configs/                      # Store geometry configurations
│   ├── store1.json              # Store 1 zone polygons
│   └── store2.json              # Store 2 zone polygons
│
├── data/                         # Sample transaction data
│   └── pos_transactions_new.csv # POS transaction CSV
│
├── docs/                         # Documentation
│   ├── DESIGN.md                # Architecture & design decisions
│   ├── CHOICES.md               # Engineering choices (YOLOv8, ByteTrack)
│   └── dashboard.png            # Dashboard screenshot
│
├── Dockerfile                    # Container image definition
├── docker-compose.yml            # Multi-container orchestration
├── requirements.txt              # Python dependencies
├── README.md                     # This file
└── store.db                      # SQLite database (auto-created)
```

---

## Troubleshooting

### Dashboard shows no data

**Problem**: Dashboard metrics are all zeros or missing.

**Solution**:
1. Verify API is running: `http://localhost:8000/health`
2. Check dashboard API_URL: Should be `http://localhost:8000`
3. Reload dashboard: Stop (Ctrl+C) and restart `streamlit run dashboard/app.py`
4. Ensure database has events: `python check_store_data.py`

### Conversion rate is 0%

**Problem**: Metrics show 0% conversion even with data.

**Solution**:
1. Check store IDs match between events and transactions
2. Events should use: `STORE_BLR_001` or `STORE_BLR_002`
3. Transactions CSV must map to matching store IDs
4. Verify with: `python test_both_stores.py`

### Tests failing with "httpx not found"

**Problem**: `RuntimeError: starlette.testclient requires httpx`

**Solution**:
```bash
pip install httpx
# or reinstall requirements
pip install -r requirements.txt
```

### API returns 500 errors

**Problem**: Backend crashes or returns 500 status.

**Solution**:
1. Check API logs for error messages
2. Verify database file exists: `store.db`
3. Restart API: `uvicorn app.main:app --reload`
4. Check database integrity: `python check_transactions.py`

### Event ingestion fails

**Problem**: Events not being saved to database.

**Solution**:
1. Verify event JSON schema matches EventSchema
2. Check store_id is valid: `STORE_BLR_001` or `STORE_BLR_002`
3. Ensure visitor_id is not null
4. Test with: `python scripts/load_events.py`

---

## Performance Metrics

**Current System Performance (STORE_BLR_002):**
- Event Processing: ~92 events loaded ✅
- Database Query Time: <100ms
- API Response Time: <200ms
- Dashboard Load Time: ~1-2s
- Transaction Processing: ~101 records

---

## Support & Contributions

For issues or enhancements:
1. Check troubleshooting section above
2. Review test files for usage examples
3. Check API Swagger docs: `http://localhost:8000/docs`
4. Inspect database directly with SQLite client

---

## License

This project is provided as-is for retail analytics research and deployment.

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run API

```bash
python -m uvicorn app.main:app --reload
```

---

## Docker

Build and run

```bash
docker compose up --build
```

---

## Test

```bash
python -m pytest
```

---

## Future Improvements

- Heatmaps
- Path analysis
- Staff/customer classification
- Multi-store support
- Real-time streaming ingestion
- Automated zone calibration
- Predictive queue forecasting

---

## Author

Oushnik Banerjee

Store Intelligence Assessment Submission