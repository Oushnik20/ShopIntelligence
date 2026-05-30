# Engineering Choices

## Detection Model

Options Considered

- YOLOv8
- RT-DETR
- MediaPipe

AI suggested YOLOv8 because of strong community support and integration with ByteTrack.

Chosen:
YOLOv8

Reason:
Fast inference, mature ecosystem, easy deployment.

---

## Event Schema Design

Options Considered

- Raw frame records
- Aggregated visitor sessions
- Event-driven schema

Chosen:
Event-driven schema

Reason:
Supports real-time analytics and simpler ingestion.

---

## API Architecture

Options Considered

- Flask
- FastAPI
- Node.js Express

Chosen:
FastAPI

Reason:
Built-in validation, OpenAPI support, asynchronous capability.