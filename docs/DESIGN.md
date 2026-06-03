# Architecture & Design Documentation

Complete system architecture, design patterns, and implementation details.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Store Intelligence Platform               │
└─────────────────────────────────────────────────────────────┘

Layer 1: Input Sources
├── CCTV Cameras (multiple stores, multiple cameras per store)
├── POS Transactions (CSV files)
└── Manual Event Ingestion (API POST)

Layer 2: Processing Pipeline
├── YOLOv8n - Person Detection (320x320 @ ~45 FPS)
├── ByteTrack - Multi-Object Tracking (stable IDs across frames)
├── Geometry Engine - Zone/Queue boundary detection
└── Event Generator - Business event creation

Layer 3: Persistence Layer
├── SQLite Database
│   ├── events table (17 columns, indexed on store_id, visitor_id)
│   ├── transactions table (5 columns, indexed on store_id)
│   └── Automatic schema creation on startup
└── File System
    └── generated_events.jsonl (event backup/logging)

Layer 4: Analytics Engine (FastAPI Backend)
├── Metrics Module (11 KPIs)
├── Funnel Module (4-stage tracking)
├── Anomaly Module (3 detection types)
└── Revenue Module (POS aggregation)

Layer 5: API Layer (FastAPI/Uvicorn)
├── 7 REST endpoints
├── JSON request/response
├── Automatic OpenAPI/Swagger documentation
└── Request logging with trace IDs

Layer 6: Presentation Layer (Streamlit)
├── Real-time dashboard
├── 8 metric cards
├── Interactive charts (funnel, dwell time)
├── Store selector
└── Raw data explorers
```

---

## Data Flow

### Event Ingestion Flow

```
Video Frame
    ↓
YOLOv8 Detection → Bounding boxes + confidence scores
    ↓
ByteTrack → Stable visitor IDs (tracker_id → VIS_{id})
    ↓
Zone/Queue Geometry Check → Visitor position analysis
    ↓
Event Generator → Create business event
    ↓
API POST /events/ingest → JSON array
    ↓
Event Schema Validation (Pydantic) → Type mapping
    ↓
SQLite Insert → events table (indexed)
    ↓
Metrics Recalculation → Real-time KPI updates
```

### Query Flow

```
Streamlit Dashboard
    ↓
HTTP GET /stores/{store_id}/metrics
    ↓
FastAPI Handler
    ↓
SQLAlchemy ORM Query
    ↓
SQLite SELECT with filters
    ↓
Metrics Calculation (Python)
    ↓
JSON Response
    ↓
Streamlit Rendering (charts, cards)
```

---

## Module Architecture

### Backend Modules

#### app/main.py - REST API Server
**Responsibility**: Expose REST endpoints
**Technology**: FastAPI + Uvicorn
**Features**:
- 7 endpoints for analytics
- Automatic OpenAPI/Swagger documentation
- Request/response logging middleware
- Global exception handling

```python
@app.post("/events/ingest")  # Event ingestion
@app.get("/stores/{store_id}/metrics")  # 11 KPIs
@app.get("/stores/{store_id}/funnel")  # 4-stage funnel
@app.get("/stores/{store_id}/anomalies")  # Anomaly alerts
@app.get("/stores/{store_id}/revenue")  # POS analytics
@app.get("/health")  # Service status
@app.get("/")  # Service info
```

#### app/models.py - Data Models
**Responsibility**: Define database schema
**Technology**: SQLAlchemy 2.x
**Models**:
- `Event`: 17 columns, indexed on store_id/visitor_id/event_type/timestamp
- `Transaction`: 5 columns, indexed on store_id

#### app/metrics.py - Analytics Calculations
**Responsibility**: Compute 11 KPIs
**KPIs Calculated**:
1. `unique_visitors` - Distinct visitor count
2. `conversion_rate` - (visitors_with_transactions / total_visitors) * 100
3. `avg_dwell_per_zone` - Average time per zone
4. `queue_depth` - Current queue visitors
5. `avg_queue_time` - Average queue duration
6. `queue_completed_count` - Completed transactions
7. `queue_abandoned_count` - Abandoned queue events
8. `queue_completion_rate` - (completed / (completed + abandoned))
9. `queue_abandonment_rate` - (abandoned / (completed + abandoned))
10. `most_visited_zone` - Zone with highest entries
11. `abandonment_rate` - Overall store abandonment

#### app/funnel.py - Conversion Funnel
**Responsibility**: Track 4-stage visitor journey
**Stages**:
1. Entry - Visitors who entered store
2. Zone Visit - Visitors who visited a zone
3. Billing Queue - Visitors who joined billing queue
4. Purchase - Visitors who completed transaction

#### app/anomalies.py - Anomaly Detection
**Responsibility**: Detect operational anomalies
**Anomaly Types**:

1. **QUEUE_SPIKE** (WARNING)
   - Trigger: `queue_visitors >= 5`
   - Action: "Open additional billing counter"

2. **DEAD_ZONE** (INFO)
   - Trigger: `zone_entries == 0` (during business hours)
   - Action: "Check zone visibility / camera calibration"

3. **CONVERSION_DROP** (WARNING)
   - Trigger: `conversion_rate < 10% AND unique_visitors >= 5`
   - Action: "Investigate customer journey"

#### app/revenue.py - Revenue Analytics
**Responsibility**: Aggregate POS data
**Metrics**:
- Total revenue (sum of amounts)
- Order count (transaction count)
- Average basket value (total / count)

#### app/database.py - Database Configuration
**Responsibility**: SQLAlchemy setup
**Features**:
- SQLite database (`store.db`)
- Automatic table creation
- Session factory (SessionLocal)

#### app/ingestion.py - Event Schema
**Responsibility**: Event validation & type mapping
**EventSchema Fields**:
- Required: event_id, store_id, camera_id, visitor_id, event_type, timestamp
- Optional: zone_id, dwell_ms, is_staff, confidence, metadata
- Type Mapping: External → Internal (6 types → 8 types)

#### app/middleware.py - Request Logging
**Responsibility**: Log all API requests
**Features**:
- Trace ID generation (UUID)
- Latency measurement
- Store ID extraction
- Event count tracking

#### app/logger.py - Structured Logging
**Responsibility**: JSON-formatted logs
**Output Format**: `{trace_id, endpoint, store_id, event_count, latency_ms, status_code}`

#### app/exceptions.py - Error Handling
**Responsibility**: Global exception handler
**Response**: 500 JSON error with message

#### app/health.py - Health Status
**Responsibility**: Service health endpoint
**Response**: `{status: "healthy", last_event_timestamp}`

---

## Computer Vision Pipeline

### pipeline/detector.py - YOLOv8 Person Detection
**Model**: YOLOv8n (nano - 3.2M parameters)
**Input**: Frame (any resolution)
**Output**: `sv.Detections` with:
- xyxy: Bounding box coordinates
- confidence: Detection confidence (0-1)
- class_id: Class index (0=person only)

**Rationale for YOLOv8n**:
- Fast inference: ~45 FPS on CPU
- Good accuracy for person detection
- Lightweight: 6.3MB model file
- Easy deployment

**Tradeoff**: Larger models (YOLOv8m/l) have higher accuracy but slower inference

### pipeline/tracker.py - ByteTrack
**Technology**: ByteTrack for multi-object tracking
**Input**: Detections per frame
**Output**: Tracked objects with:
- xyxy: Bounding box
- tracker_id: Persistent visitor ID

**Rationale**:
- Stable identity assignment across frames
- Handles temporary occlusion
- Lightweight: No heavy re-ID network
- Integrates directly with YOLOv8

**Tradeoff**: Full re-identification systems could be more accurate but need more compute

### pipeline/store_config.py - Geometry Engine
**Responsibility**: Zone/queue boundary detection
**Methods**:
- `load_store_config()` - Load JSON geometries
- `point_inside_polygon()` - Point-in-polygon test (OpenCV)
- `get_zone_polygon()` - Zone boundaries
- `get_queue_polygon()` - Queue boundaries
- `get_entry_line()` - Entry line coordinates

**Supports**:
- Multi-polygon zones
- Multi-camera entry points (Store 2)
- Dynamic zone definitions

### pipeline/event_generator.py - Event Creation
**Responsibility**: Convert tracking data to business events
**Event Types Generated**:
- ENTRY (crosses entry line)
- EXIT (leaves store)
- ZONE_ENTER (enters zone)
- ZONE_DWELL (spends time in zone)
- ZONE_EXIT (leaves zone)
- BILLING_QUEUE_JOIN (enters queue)
- BILLING_QUEUE_COMPLETED (completes transaction)
- BILLING_QUEUE_ABANDON (abandons queue)

**Event Persistence**: JSONL file (`pipeline/generated_events.jsonl`)

---

## Database Schema

### events table
```sql
CREATE TABLE events (
  event_id TEXT PRIMARY KEY,
  store_id TEXT NOT NULL,
  camera_id TEXT,
  event_type TEXT NOT NULL,
  visitor_id TEXT NOT NULL,
  timestamp DATETIME,
  zone_id TEXT,
  dwell_ms INTEGER,
  is_staff BOOLEAN,
  confidence FLOAT,
  metadata JSON,
  INDEX idx_store_id,
  INDEX idx_visitor_id,
  INDEX idx_event_type,
  INDEX idx_timestamp
)
```

### transactions table
```sql
CREATE TABLE transactions (
  transaction_id TEXT PRIMARY KEY,
  store_id TEXT NOT NULL,
  visitor_id TEXT,
  timestamp DATETIME,
  amount FLOAT,
  INDEX idx_store_id
)
```

---

## Event Type Mapping

The system supports event type normalization for backward compatibility:

**External Format** → **Internal Format**
- entry → ENTRY
- exit → EXIT
- zone_entered → ZONE_ENTER
- zone_exited → ZONE_EXIT
- queue_completed → BILLING_QUEUE_COMPLETED
- queue_abandoned → BILLING_QUEUE_ABANDON

---

## API Response Format

All API responses follow standard JSON format:

**Success Response (2xx)**:
```json
{
  "data": {...},
  "status": "success",
  "timestamp": "2026-06-03T14:22:10Z"
}
```

**Error Response (4xx/5xx)**:
```json
{
  "error": "Error message",
  "status": "error",
  "code": 400
}
```

---

## Performance Characteristics

### Processing Latency
- Video Frame → Detection: ~22ms (YOLOv8n)
- Tracking → Event Generation: ~5ms
- API Query → Response: <100ms
- Dashboard Refresh: ~1-2 seconds

### Storage
- SQLite Database: ~50MB per 100k events
- Events JSONL: ~20MB per 100k events
- YOLOv8n Model: 6.3MB

### Scalability
- Current: Single instance, ~1000 events/minute
- Horizontal: Multiple API instances with load balancer
- Vertical: Increase CPU/RAM for faster processing
- Database: PostgreSQL recommended for >1M events

---

## Security Considerations

### Current Implementation
- No authentication (assumed internal network)
- No input sanitization beyond schema validation
- SQLite (single-file database, no multi-user isolation)

### Production Recommendations
- Add JWT authentication
- Validate all inputs server-side
- Use PostgreSQL with proper access control
- Enable HTTPS/TLS
- Implement rate limiting
- Add request signing for sensitive operations
- Regular security audits

---

## Configuration

### Store Configuration (JSON)
Each store has geometry configuration for zone/queue detection.

**Example: configs/store2.json**
```json
{
  "entry_line": [900, 900],
  "zone_polygon": [[0,0],[1920,0],[1920,1080],[0,1080]],
  "queue_polygon": [[450,250],[1400,250],[1400,1080],[450,1080]]
}
```

### Model Configuration
**YOLOv8 Parameters**:
- Model: yolov8n (nano)
- Input size: 320x320
- Confidence threshold: 0.5
- Class filter: [0] (person only)

**ByteTrack Parameters**:
- Track buffer: 30 frames
- Min hits: 3
- Max age: 30 frames

---

## Future Enhancements

### Short Term
1. Add demographic detection (age, gender estimation)
2. Group detection (family/couple identification)
3. Product interaction tracking
4. Heat map generation

### Medium Term
1. Multi-store federation (single dashboard)
2. Real-time alerts (SMS/Slack)
3. Historical trend analysis
4. Predictive analytics (peak hours)

### Long Term
1. Full re-identification system (improved tracking)
2. Facial recognition (with privacy controls)
3. Advanced anomaly detection (ML-based)
4. Integration with retail management systems (POS sync)


# Config-Driven Store Support

## Why JSON configs?

Coordinates and geometry are stored in `configs/store1.json` and `configs/store2.json`.

This enables:

- Reuse of detector/tracker/event generator code
- Store-specific entry lines, zone polygons, and queue polygons
- Cleaner separation of store geometry from pipeline logic

---

# Event Schema

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

# Event Mapping

New assessment event names are mapped to internal types to preserve compatibility.

Mapped events:

- `entry` → `ENTRY`
- `exit` → `EXIT`
- `zone_entered` → `ZONE_ENTER`
- `zone_exited` → `ZONE_EXIT`
- `queue_completed` → `BILLING_QUEUE_COMPLETED`
- `queue_abandoned` → `BILLING_QUEUE_ABANDON`

This retains support for older internal event names while embracing new event naming.

---

# Store 2 Pipeline Reuse

Store 2 reuses the existing architecture and modules:

- `pipeline/detector.py`
- `pipeline/tracker.py`
- `pipeline/event_generator.py`

New Store 2 runners only configure:

- `VIDEO_PATH`
- `STORE_ID`
- `CAMERA_ID`

---

# Analytics Layer

Metrics are derived from stored events, including:

- Unique visitors
- Conversion rate
- Average dwell time
- Queue depth
- Avg queue time
- Queue completed count
- Queue abandoned count
- Queue completion rate
- Queue abandonment rate
- Most visited zone

---

# Funnel Analytics

Customer journey model:

```
ENTRY
↓
ZONE_VISIT
↓
BILLING_QUEUE
↓
PURCHASE
```

This helps identify drop-off points in the customer journey.

---

# Dashboard Design

The dashboard supports multiple stores with a store selector.

Store selector values:

- `STORE_BLR_001`
- `STORE_BLR_002`

All API requests are made using the selected store.

---

# Scalability Considerations

Future enhancements may include:

- PostgreSQL instead of SQLite
- Real-time RTSP ingestion
- Cloud-based event streaming
- ML-based anomaly detection

---

# Assumptions

- One track ID corresponds to one visitor
- Cameras have fixed viewpoints
- POS transactions are available for revenue mapping
- Zone and queue boundaries are predefined
