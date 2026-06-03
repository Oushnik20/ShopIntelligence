# API Reference

Complete REST API documentation for Store Intelligence Platform.

---

## Base URL

**Development**: `http://localhost:8000`  
**Production**: `https://shopintelligence.onrender.com` (update as needed)

---

## Authentication

Currently: **No authentication required** (internal network assumption)

Future: JWT tokens for multi-tenant deployments

---

## Error Handling

### Error Response Format

```json
{
  "detail": "Error message explaining what went wrong",
  "status_code": 400
}
```

### HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad request (invalid schema) |
| 404 | Not found |
| 500 | Server error |

---

## Endpoints

### 1. Root / Service Info

**GET** `/`

Returns service information and version.

**Response (200)**:
```json
{
  "service": "Store Intelligence API",
  "version": "1.0",
  "status": "operational"
}
```

**Example**:
```bash
curl http://localhost:8000/
```

---

### 2. Health Check

**GET** `/health`

Returns service health status and last event timestamp.

**Response (200)**:
```json
{
  "status": "healthy",
  "last_event_timestamp": "2026-06-03T14:22:49.248123"
}
```

**Use Cases**:
- Monitoring service availability
- Uptime checks
- Load balancer health probes

**Example**:
```bash
curl http://localhost:8000/health
```

---

### 3. Ingest Events

**POST** `/events/ingest`

Ingest visitor events from CCTV pipeline or external sources.

**Request Body**:
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

**Field Descriptions**:

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| event_id | string | Yes | Unique event identifier (recommended: TYPE_ID_TIMESTAMP) |
| store_id | string | Yes | Valid: `STORE_BLR_001`, `STORE_BLR_002` |
| camera_id | string | Yes | Camera identifier (e.g., "CAM_ZONE_1") |
| visitor_id | string | Yes | Unique visitor ID (e.g., "VIS_42") |
| event_type | string | Yes | See Event Types below |
| timestamp | datetime | Yes | ISO 8601 format |
| zone_id | string | No | Zone identifier if applicable |
| dwell_ms | integer | No | Dwell time in milliseconds (0 for instantaneous events) |
| is_staff | boolean | No | True if staff member, false if customer |
| confidence | float | No | Detection confidence (0-1) |
| metadata | object | No | Additional data as JSON |

**Response (200)**:
```json
{
  "inserted": 1,
  "errors": []
}
```

**Response (400 - Validation Error)**:
```json
{
  "detail": "Invalid event_type. Valid types: ENTRY, EXIT, ZONE_ENTER, ...",
  "status_code": 400
}
```

**Event Types**:
- `ENTRY` - Visitor enters store
- `EXIT` - Visitor leaves store
- `ZONE_ENTER` - Visitor enters zone
- `ZONE_DWELL` - Visitor dwells in zone
- `ZONE_EXIT` - Visitor leaves zone
- `BILLING_QUEUE_JOIN` - Enters billing queue
- `BILLING_QUEUE_COMPLETED` - Completes billing
- `BILLING_QUEUE_ABANDON` - Abandons queue

**Legacy Type Mapping** (auto-converted):
- `entry` → `ENTRY`
- `exit` → `EXIT`
- `zone_entered` → `ZONE_ENTER`
- `zone_exited` → `ZONE_EXIT`
- `queue_completed` → `BILLING_QUEUE_COMPLETED`
- `queue_abandoned` → `BILLING_QUEUE_ABANDON`

**Example**:
```bash
curl -X POST http://localhost:8000/events/ingest \
  -H "Content-Type: application/json" \
  -d '[{
    "event_id": "ENTRY_1_1234567890",
    "store_id": "STORE_BLR_002",
    "camera_id": "CAM_ENTRY",
    "visitor_id": "VIS_1",
    "event_type": "ENTRY",
    "timestamp": "2026-06-03T14:22:10Z",
    "zone_id": null,
    "dwell_ms": 0,
    "is_staff": false,
    "confidence": 0.95,
    "metadata": {}
  }]'
```

---

### 4. Get Store Metrics

**GET** `/stores/{store_id}/metrics`

Returns 11 key performance indicators for a store.

**Path Parameters**:

| Parameter | Type | Required | Values |
|-----------|------|----------|--------|
| store_id | string | Yes | `STORE_BLR_001`, `STORE_BLR_002` |

**Response (200)**:
```json
{
  "unique_visitors": 50,
  "conversion_rate": 90.0,
  "avg_dwell_per_zone": {
    "ZONE_1": 5.23,
    "ZONE_2": 3.45
  },
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

**Metrics Definitions**:

| Metric | Formula | Notes |
|--------|---------|-------|
| unique_visitors | Count(distinct visitor_id) | Excludes staff (is_staff=false) |
| conversion_rate | (visitors_with_txn / total_visitors) × 100 | % with POS transactions |
| avg_dwell_per_zone | sum(dwell_ms) / count / 1000 | Per zone, seconds |
| queue_depth | Count(BILLING_QUEUE_JOIN events) | Current queue size |
| avg_queue_time | avg(dwell_ms for COMPLETED) / 1000 | Seconds in queue |
| queue_completed_count | Count(BILLING_QUEUE_COMPLETED) | Transactions completed |
| queue_abandoned_count | Count(BILLING_QUEUE_ABANDON) | Abandoned transactions |
| queue_completion_rate | completed / (completed + abandoned) × 100 | % success rate |
| queue_abandonment_rate | abandoned / (completed + abandoned) × 100 | % drop rate |
| most_visited_zone | Zone with max ZONE_ENTER events | Most popular area |
| abandonment_rate | abandoned / all visitors × 100 | Overall store abandon % |

**Query Performance**: <100ms

**Example**:
```bash
# Get metrics for Store 2
curl http://localhost:8000/stores/STORE_BLR_002/metrics

# Response
{
  "unique_visitors": 50,
  "conversion_rate": 90.0,
  ...
}
```

---

### 5. Get Conversion Funnel

**GET** `/stores/{store_id}/funnel`

Returns visitor progression through 4-stage conversion funnel.

**Path Parameters**:

| Parameter | Type | Required | Values |
|-----------|------|----------|--------|
| store_id | string | Yes | `STORE_BLR_001`, `STORE_BLR_002` |

**Response (200)**:
```json
{
  "entry": 46,
  "zone_visit": 22,
  "billing_queue": 11,
  "purchase": 41
}
```

**Funnel Stages**:

| Stage | Definition | Criteria |
|-------|-----------|----------|
| entry | Visitors who entered | ENTRY event exists |
| zone_visit | Entered a zone | ZONE_ENTER event exists |
| billing_queue | Joined billing queue | BILLING_QUEUE_JOIN event exists |
| purchase | Completed transaction | Transaction record exists |

**Funnel Analysis**:
- Entry → Zone: `22/46 = 47.8%` conversion
- Zone → Queue: `11/22 = 50%` conversion
- Queue → Purchase: `41/46 = 89.1%` conversion

**Example**:
```bash
curl http://localhost:8000/stores/STORE_BLR_002/funnel

# Response
{
  "entry": 46,
  "zone_visit": 22,
  "billing_queue": 11,
  "purchase": 41
}
```

---

### 6. Get Anomalies

**GET** `/stores/{store_id}/anomalies`

Real-time operational anomalies and alerts.

**Path Parameters**:

| Parameter | Type | Required | Values |
|-----------|------|----------|--------|
| store_id | string | Yes | `STORE_BLR_001`, `STORE_BLR_002` |

**Response (200)**:
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

**Anomaly Types**:

| Type | Trigger | Severity | Action |
|------|---------|----------|--------|
| QUEUE_SPIKE | queue_visitors ≥ 5 | WARN | Open additional billing counter |
| DEAD_ZONE | zone_entries == 0 | INFO | Check zone visibility / camera |
| CONVERSION_DROP | rate < 10% AND visitors ≥ 5 | WARN | Investigate customer journey |

**Response Structure**:

```json
{
  "store_id": "STORE_BLR_002",
  "anomalies": [
    {
      "type": "string",
      "severity": "WARN|INFO|CRITICAL",
      "suggested_action": "string"
    }
  ]
}
```

**Example**:
```bash
curl http://localhost:8000/stores/STORE_BLR_002/anomalies

# Response
{
  "store_id": "STORE_BLR_002",
  "anomalies": [
    {
      "type": "QUEUE_SPIKE",
      "severity": "WARN",
      "suggested_action": "Open additional billing counter"
    }
  ]
}
```

---

### 7. Get Revenue Metrics

**GET** `/stores/{store_id}/revenue`

POS transaction analytics and revenue metrics.

**Path Parameters**:

| Parameter | Type | Required | Values |
|-----------|------|----------|--------|
| store_id | string | Yes | `STORE_BLR_001`, `STORE_BLR_002` |

**Response (200)**:
```json
{
  "total_revenue": 47828.94,
  "order_count": 101,
  "avg_basket_value": 473.55
}
```

**Metrics Definitions**:

| Metric | Formula |
|--------|---------|
| total_revenue | SUM(transaction.amount) |
| order_count | COUNT(transaction_id) |
| avg_basket_value | total_revenue / order_count |

**Example**:
```bash
curl http://localhost:8000/stores/STORE_BLR_002/revenue

# Response
{
  "total_revenue": 47828.94,
  "order_count": 101,
  "avg_basket_value": 473.55
}
```

---

## Request Examples

### Python (requests library)

```python
import requests

BASE_URL = "http://localhost:8000"
STORE_ID = "STORE_BLR_002"

# Get metrics
response = requests.get(f"{BASE_URL}/stores/{STORE_ID}/metrics")
metrics = response.json()
print(f"Conversion Rate: {metrics['conversion_rate']}%")

# Get funnel
response = requests.get(f"{BASE_URL}/stores/{STORE_ID}/funnel")
funnel = response.json()
print(f"Entry → Purchase: {funnel['entry']} → {funnel['purchase']}")

# Ingest events
events = [{
    "event_id": "EVT_123",
    "store_id": STORE_ID,
    "camera_id": "CAM_1",
    "visitor_id": "VIS_1",
    "event_type": "ENTRY",
    "timestamp": "2026-06-03T14:22:10Z",
    "zone_id": None,
    "dwell_ms": 0,
    "is_staff": False,
    "confidence": 0.95,
    "metadata": {}
}]
response = requests.post(f"{BASE_URL}/events/ingest", json=events)
print(f"Inserted: {response.json()['inserted']}")
```

### cURL

```bash
# Health check
curl http://localhost:8000/health

# Get metrics
curl http://localhost:8000/stores/STORE_BLR_002/metrics

# Get anomalies
curl http://localhost:8000/stores/STORE_BLR_002/anomalies

# Ingest events
curl -X POST http://localhost:8000/events/ingest \
  -H "Content-Type: application/json" \
  -d '[{"event_id":"EVT_1",...}]'
```

### JavaScript (fetch)

```javascript
const BASE_URL = "http://localhost:8000";
const STORE_ID = "STORE_BLR_002";

// Get metrics
fetch(`${BASE_URL}/stores/${STORE_ID}/metrics`)
  .then(r => r.json())
  .then(data => console.log("Conversion:", data.conversion_rate + "%"));

// Ingest events
const events = [{
  event_id: "EVT_123",
  store_id: STORE_ID,
  camera_id: "CAM_1",
  visitor_id: "VIS_1",
  event_type: "ENTRY",
  timestamp: new Date().toISOString(),
  zone_id: null,
  dwell_ms: 0,
  is_staff: false,
  confidence: 0.95,
  metadata: {}
}];

fetch(`${BASE_URL}/events/ingest`, {
  method: "POST",
  headers: {"Content-Type": "application/json"},
  body: JSON.stringify(events)
})
.then(r => r.json())
.then(data => console.log("Inserted:", data.inserted));
```

---

## Rate Limiting

Currently: **Unlimited** (recommend adding for production)

Suggested production limits:
- `/events/ingest`: 1000 requests/minute
- `/stores/{store_id}/metrics`: 100 requests/minute
- Other endpoints: 500 requests/minute

---

## Swagger/OpenAPI Documentation

Interactive API documentation available at:
```
http://localhost:8000/docs
```

Includes:
- Live API testing interface
- Request/response schemas
- Example values
- Error documentation

---

## API Versioning

Current version: `1.0`

Future versions will use `/v2/`, `/v3/` paths to maintain backward compatibility.

---

## Support & Feedback

- Check README.md for troubleshooting
- Review test files for usage examples
- Access Swagger docs for interactive testing
- Check application logs for error details
