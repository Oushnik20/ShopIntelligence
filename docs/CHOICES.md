# Engineering Choices

## Objective

The objective of this project is to transform retail CCTV footage and POS transaction data into actionable business insights including visitor analytics, dwell analysis, queue monitoring, conversion funnels, and anomaly detection.

---

## Why YOLOv8?

### Choice

YOLOv8n

### Reason

YOLOv8n was selected because it provides:

* Fast inference speed
* Good person detection accuracy
* Low hardware requirements
* Easy deployment on CPU-based systems

### Tradeoff

Larger models such as YOLOv8m or YOLOv8l may provide slightly higher accuracy but require significantly more compute resources.

---

## Why ByteTrack?

### Choice

ByteTrack for multi-object tracking.

### Reason

The platform requires assigning a consistent identity to visitors across video frames.

ByteTrack was chosen because:

* Strong tracking performance
* Lightweight implementation
* Robust handling of temporary occlusions
* Easy integration with YOLO detections

### Tradeoff

A more sophisticated re-identification system could improve long-term identity persistence but would increase complexity.

---

## Why Event-Driven Analytics?

### Choice

Generate events first and compute metrics later.

Examples:

* ENTRY
* ZONE_DWELL
* BILLING_QUEUE_JOIN

### Reason

Separating event generation from analytics provides:

* Better scalability
* Easier testing
* Simpler debugging
* Reusable event history

### Alternative Considered

Directly computing metrics from video streams.

This approach was rejected because it tightly couples video processing and business analytics.

---

## Why SQLite?

### Choice

SQLite database.

### Reason

SQLite provides:

* Zero infrastructure setup
* Simplicity
* Portability
* Easy local deployment

This is appropriate for an assessment-sized project.

### Tradeoff

For production-scale deployments, PostgreSQL would be preferred.

---

## Why FastAPI?

### Choice

FastAPI for backend services.

### Reason

FastAPI provides:

* Automatic API documentation
* Type validation
* High performance
* Simple development workflow

### Benefit

Rapid implementation of analytics endpoints.

---

## Why Streamlit?

### Choice

Streamlit dashboard.

### Reason

Streamlit allows rapid development of analytics dashboards with minimal frontend code.

Benefits:

* Fast iteration
* Simple deployment
* Easy visualization of metrics

---

## Why Separate Cameras by Function?

### Camera Allocation

### CAM3

Entry monitoring

Generated Event:

* ENTRY

### CAM1 / CAM2

Customer engagement monitoring

Generated Event:

* ZONE_DWELL

### CAM5

Billing area monitoring

Generated Event:

* BILLING_QUEUE_JOIN

### Reason

Each camera provides a distinct business signal, reducing processing complexity and simplifying event generation logic.

---

## Analytics Choices

### Conversion Funnel

Customer journey:

ENTRY
→ ZONE_VISIT
→ BILLING_QUEUE
→ PURCHASE

This model helps identify drop-off points in the customer journey.

---

### Queue Monitoring

Queue depth is estimated from tracked visitors present in the billing zone.

Business value:

* Staffing optimization
* Customer experience improvement

---

### Dwell Time Analytics

Dwell time is used as a proxy for customer engagement.

Longer dwell time may indicate:

* Product interest
* Promotional effectiveness
* Store layout effectiveness

---

## Anomaly Detection Strategy

Rule-based anomaly detection was selected.

Implemented anomalies:

* Queue Spike
* Conversion Drop
* Dead Zone

### Reason

Rule-based systems are:

* Easy to understand
* Easy to validate
* Suitable for assessment scope

### Future Improvement

Machine-learning-based anomaly detection using historical store behavior.

---

## Assumptions

* One tracker ID represents one visitor.
* Cameras have fixed viewpoints.
* Store layout remains stable.
* POS transactions are available.
* Visitor identities are anonymized.

---

## Future Enhancements

* Real-time RTSP stream ingestion
* Heatmap generation
* Path analysis
* Customer segmentation
* Staff/customer classification
* Multi-store support
* Cloud deployment
* Predictive queue forecasting
