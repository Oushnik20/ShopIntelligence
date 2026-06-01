# Store Intelligence Platform

AI-powered retail analytics platform that converts CCTV video streams and POS transactions into actionable store insights.

## Overview

This project processes multi-camera retail store footage to generate visitor analytics, dwell-time metrics, queue monitoring, conversion funnels, and anomaly detection.

The system uses computer vision for customer detection and tracking, generates business events, stores them in a database, and exposes analytics through REST APIs and a dashboard.

---

## Features

### Visitor Analytics
- Visitor counting
- Unique visitor tracking
- Entry detection

### Zone Analytics
- Zone dwell time measurement
- Product engagement analysis
- Zone-level insights

### Queue Monitoring
- Billing queue detection
- Queue depth monitoring
- Queue spike alerts

### Conversion Analytics
- Visitor → Zone → Billing → Purchase funnel
- Conversion rate calculation
- POS transaction integration

### Anomaly Detection
- Queue spike detection
- Dead zone detection
- Conversion drop alerts

### Platform Features
- REST APIs
- SQLite persistence
- Docker deployment
- Streamlit dashboard
- Automated tests

---

## Architecture

```

CCTV Cameras
(CAM1, CAM2, CAM3, CAM5)
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
Dashboard & Analytics

```

---

## Camera Responsibilities

### CAM3
Purpose:
- Entry monitoring

Generated Events:
- ENTRY

### CAM1 / CAM2
Purpose:
- Product interaction monitoring

Generated Events:
- ZONE_DWELL

### CAM5
Purpose:
- Billing area monitoring

Generated Events:
- BILLING_QUEUE_JOIN

---

## Event Types

| Event Type | Description |
|------------|-------------|
| ENTRY | Customer enters store |
| ZONE_DWELL | Customer spends time in a zone |
| BILLING_QUEUE_JOIN | Customer joins billing queue |

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

### Ingest Events

POST

```

/events/ingest

```

### Store Metrics

GET

```

/stores/{store_id}/metrics

```

### Funnel Analytics

GET

```

/stores/{store_id}/funnel

```

### Anomalies

GET

```

/stores/{store_id}/anomalies

```

### Health Check

GET

```

/health

```

---

## Metrics

The platform calculates:

- Unique Visitors
- Conversion Rate
- Average Dwell Time
- Queue Depth
- Abandonment Rate

---

## Anomaly Rules

### Queue Spike

Triggered when:

```

queue_count >= threshold

```

Recommended Action:

```

Open additional billing counter

```

### Conversion Drop

Triggered when:

```

conversion_rate < threshold

```

Recommended Action:

```

Investigate customer journey

```

---

## Store Layout

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

- Unique Visitors: 50
- Conversion Rate: 100%
- Queue Depth: 9
- Average Zone Dwell Time: 5.24 seconds
- Active Anomalies: Queue Spike Warning

---

## Running Locally

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate

Windows

```bash
venv\Scripts\activate
```

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