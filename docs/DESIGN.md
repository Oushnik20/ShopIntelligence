# Design Decisions

## Problem

Retail stores require visibility into customer behavior, engagement, and conversion.

Traditional CCTV systems provide video but do not generate actionable insights.

The goal of this platform is to transform video streams into business intelligence.

---

# Detection Layer

## YOLOv8

Chosen because:

- Fast inference
- Strong person detection performance
- Lightweight deployment
- Easy integration

Model:

```

yolov8n

```

Tradeoff:

Lower accuracy than larger models but significantly faster.

---

# Tracking Layer

## ByteTrack

Chosen because:

- Stable identity assignment
- Works well in crowded scenes
- Lightweight implementation

Purpose:

Convert frame-level detections into visitor trajectories.

---

# Event Driven Architecture

Instead of directly computing metrics from video, the system generates events.

Benefits:

- Decoupled architecture
- Easier testing
- Reproducibility
- Future scalability

Examples:

```

ENTRY
ZONE_DWELL
BILLING_QUEUE_JOIN

```

---

# Storage Layer

## SQLite

Chosen because:

- Simple setup
- Zero infrastructure
- Portable
- Suitable for assessment scope

Tradeoff:

Not ideal for large-scale production workloads.

---

# Analytics Layer

Metrics are derived from stored events.

Examples:

- Visitor Count
- Conversion Rate
- Queue Depth
- Dwell Time

---

# Funnel Analytics

Customer journey modeled as:

```

ENTRY
↓
ZONE_VISIT
↓
BILLING_QUEUE
↓
PURCHASE

```

This allows identification of conversion drop-offs.

---

# Anomaly Detection

Rule-based detection used for simplicity.

Implemented:

- Queue Spike
- Conversion Drop
- Dead Zone

Future:

- ML-based anomaly detection
- Forecasting models

---

# Scalability Considerations

Future production deployment could replace:

SQLite → PostgreSQL

Local Processing → Kafka + Stream Processing

Batch Analytics → Real-time Analytics

---

# Assumptions

- One tracked ID corresponds to one visitor.
- Cameras have fixed viewpoints.
- POS transactions are available.
- Zone boundaries are predefined.

---

# Future Work

- Real-time RTSP ingestion
- Heatmaps
- Path analytics
- Multi-store deployment
- Cloud deployment
- Staff detection
- Customer segmentation