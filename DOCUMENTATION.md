# Documentation Index

Complete documentation for Store Intelligence Platform.

---

## Quick Links

### For Users
- **[README.md](README.md)** - Project overview, features, and quick start
- **[SETUP.md](SETUP.md)** - Step-by-step setup and deployment guide
- **[API_REFERENCE.md](API_REFERENCE.md)** - Complete REST API documentation

### For Developers
- **[docs/DESIGN.md](docs/DESIGN.md)** - System architecture and design patterns
- **[docs/CHOICES.md](docs/CHOICES.md)** - Engineering choices and rationale
- **[docs/CHANGELOG.md](docs/CHANGELOG.md)** - Version history (create if needed)

---

## Documentation Files

### README.md
**Overview, features, running instructions, API endpoints, configuration**

- Project description
- Supported stores and features
- Technology stack
- All 7 API endpoints with examples
- Sample outputs with real data
- Configuration (zone geometries)
- Complete project structure
- Troubleshooting guide
- Performance metrics
- 2800+ lines

**When to read**: First time setup or overview

---

### SETUP.md
**Step-by-step installation and deployment guide**

- Prerequisites and system requirements
- Virtual environment setup (Windows, macOS, Linux)
- Python dependency installation
- Database initialization
- Loading sample data (3 options)
- Running full stack (3 terminals)
- Docker deployment
- Verification checklist (✅ 20+ items)
- Production deployment best practices
- Troubleshooting common issues

**When to read**: Before starting local development

---

### API_REFERENCE.md
**Complete REST API documentation with examples**

- Base URL configuration
- Authentication model
- Error handling and status codes
- 7 endpoints with:
  - Full request/response specs
  - Field descriptions and types
  - Example cURL/Python/JavaScript
  - Metrics definitions
  - Use cases
- Request examples in 3 languages
- Swagger docs reference
- API versioning strategy
- Rate limiting recommendations

**When to read**: When building integrations or client code

---

### docs/DESIGN.md
**System architecture and technical design**

- High-level system architecture diagram
- Data flow diagrams (event ingestion, query flow)
- Module architecture (11 backend modules)
- Computer vision pipeline (YOLOv8, ByteTrack)
- Database schema with SQL
- Event type mapping
- API response formats
- Performance characteristics
- Security considerations
- Future enhancement roadmap

**When to read**: Understanding system design or contributing features

---

### docs/CHOICES.md
**Engineering decisions and tradeoffs**

- Computer Vision Stack
  - YOLOv8n vs. alternatives
  - ByteTrack vs. alternatives
  - OpenCV geometry engine
  
- Backend Framework
  - FastAPI + Uvicorn comparison
  - SQLAlchemy 2.x rationale
  
- Database
  - SQLite for MVP, PostgreSQL for scale
  - Migration path
  
- Frontend
  - Streamlit vs. React
  - Development speed vs. features
  
- Deployment
  - Docker + Compose
  - Container vs. Virtual env
  
- Key Tradeoffs Summary
- Testing strategy
- Monitoring recommendations
- Security model

**When to read**: Understanding why certain technologies were chosen

---

## How to Use This Documentation

### I want to...

#### ...get started quickly
1. Read [README.md](README.md) - Project overview
2. Follow [SETUP.md](SETUP.md) - Installation steps
3. Verify with SETUP.md checklist

#### ...integrate with the API
1. Read [API_REFERENCE.md](API_REFERENCE.md) - Endpoints
2. Check API_REFERENCE.md examples (Python/cURL/JS)
3. Use `http://localhost:8000/docs` for interactive testing

#### ...understand the architecture
1. Read [docs/DESIGN.md](docs/DESIGN.md) - System design
2. Review data flow diagrams
3. Study module architecture

#### ...understand why X technology was chosen
1. Read [docs/CHOICES.md](docs/CHOICES.md) - Decision rationale
2. Review tradeoff tables
3. Check upgrade paths

#### ...deploy to production
1. Review [SETUP.md](SETUP.md) - Production deployment section
2. Read [docs/DESIGN.md](docs/DESIGN.md) - Security considerations
3. Configure environment variables
4. Set up monitoring (ELK, Prometheus)

#### ...modify the system
1. Read [docs/DESIGN.md](docs/DESIGN.md) - Architecture
2. Review [docs/CHOICES.md](docs/CHOICES.md) - Patterns
3. Study test files for examples
4. Update tests before making changes

---

## Documentation Updates

### Latest Changes
- ✅ README.md - Comprehensive project documentation
- ✅ SETUP.md - Complete installation guide
- ✅ API_REFERENCE.md - Detailed API specs
- ✅ docs/DESIGN.md - Architecture and design
- ✅ docs/CHOICES.md - Engineering rationale
- ✅ DOCUMENTATION.md - This file

### Current Version
**Store Intelligence Platform v1.0**  
Updated: June 3, 2026

---

## File Structure

```
store-intelligence/
├── README.md                 # Main documentation
├── SETUP.md                  # Installation guide
├── API_REFERENCE.md          # API documentation
├── DOCUMENTATION.md          # This file (index)
├── docs/
│   ├── DESIGN.md            # Architecture & design
│   ├── CHOICES.md           # Engineering choices
│   ├── CHANGELOG.md         # Version history (if needed)
│   └── dashboard.png        # Dashboard screenshot
└── ... (code files)
```

---

## Contributing to Documentation

When updating code:
1. Update relevant .md file
2. Keep examples current
3. Update API_REFERENCE.md if endpoints change
4. Add to CHANGELOG.md (if exists)
5. Keep architecture diagrams in sync

---

## Quick Reference

### Important URLs
- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **Dashboard**: http://localhost:8501
- **Health Check**: http://localhost:8000/health

### Important Commands
```bash
# Setup
python -m venv venv
pip install -r requirements.txt

# Run
uvicorn app.main:app --reload
streamlit run dashboard/app.py

# Test
python -m pytest tests/ -v

# Load Data
python scripts/load_transactions.py
python scripts/load_events.py

# Check
python check_transactions.py
```

### Key Files
- `app/main.py` - API endpoints
- `dashboard/app.py` - Dashboard UI
- `pipeline/detector.py` - YOLOv8 detection
- `pipeline/tracker.py` - ByteTrack tracking
- `app/models.py` - Database schema
- `requirements.txt` - Python dependencies

### Important Stores
- `STORE_BLR_001` - Primary store (1 event, 50 transactions)
- `STORE_BLR_002` - Full data store (92 events, 101 transactions) ← **Use this**

---

## Support

For issues not covered in documentation:
1. Check README.md Troubleshooting section
2. Review test files (`tests/`) for examples
3. Check API Swagger docs
4. Inspect application logs
5. Use SQLite browser to inspect database

---

## License

Store Intelligence Platform - All Rights Reserved

---

**Last Updated**: June 3, 2026  
**Status**: ✅ Production Ready
