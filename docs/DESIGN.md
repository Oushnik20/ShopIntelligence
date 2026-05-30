# Store Intelligence System Design

## Architecture

The system consists of four major layers:

1. Detection Layer
2. Event Ingestion Layer
3. Intelligence API
4. Dashboard Layer

### Detection Layer

Raw CCTV footage is processed using a person detection and tracking pipeline.

Planned stack:
- YOLOv8
- ByteTrack
- OpenCV

Output:
Structured behavioral events.

### Event Layer

Events are emitted in JSON format and ingested through the FastAPI endpoint.

### Intelligence API

The API computes:

- Visitor counts
- Conversion rates
- Funnel metrics
- Zone dwell metrics
- Operational anomalies

### Storage

SQLite is currently used for local development.

### AI-Assisted Decisions

AI tools were used to:
- Evaluate detection architectures
- Design event schema
- Generate and refine test cases

Suggestions were reviewed manually before implementation.