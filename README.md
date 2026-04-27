# Taotech OSINT Toolkit

Taotech OSINT Toolkit is a full-stack internal OSINT platform with:
- a core Python OSINT engine,
- a Flask API layer,
- and a React cyber dashboard.

This guide is written to be practical and easy to follow.

## What You Get

- Username scanning (`maigret`, `sherlock`)
- Email scanning (`holehe`)
- Domain scanning (`theHarvester`)
- Flask REST API for frontend/backend integration
- React dashboard with scan pages and report download
- Structured HTML reports in `core/reports/`
- Logging in `logs.txt`

## Architecture (Dependency Flow)

`React -> Flask -> Bridge -> Core -> OSINT CLI tools`

- Frontend calls Flask endpoints only.
- Flask routes call `backend/services/osint_bridge.py` only.
- Bridge calls `core/modules/*` only.
- Core modules execute OSINT tools via subprocess.

## Project Structure

```text
taotech-osint/
├── main.py                       # CLI entrypoint
├── core/
│   ├── modules/                  # Core OSINT engine
│   ├── reporting/                # Structured report generator
│   ├── reports/                  # Generated HTML reports
│   └── utils/                    # Core runner/logger
├── backend/
│   ├── app.py                    # Flask app entrypoint
│   ├── routes/                   # API routes
│   ├── services/                 # Bridge/service layer
│   └── utils/                    # API helpers
├── frontend/                     # React + Vite dashboard
├── tests/                        # Pytest suite
├── requirements.txt
└── README.md
```

## Prerequisites

- Python `3.10+`
- Node.js `18+` and npm
- OSINT CLI tools accessible in PATH:
  - `maigret`
  - `sherlock`
  - `holehe`
  - `theHarvester`

> If a tool is missing, scans fail gracefully with a clear error message.

## Setup

### 1) Install Python dependencies

```bash
pip install -r requirements.txt
```

### 2) Install frontend dependencies

```bash
cd frontend
npm install
cd ..
```

## How To Run (Recommended Full Stack)

Use two terminals.

### Terminal A: Start Flask API

```bash
python -m backend.app
```

Backend runs on: `http://127.0.0.1:5000`

### Terminal B: Start React dashboard

```bash
cd frontend
npm run dev
```

Frontend runs on Vite URL (usually `http://127.0.0.1:5173`).

## API Reference

Base URL: `http://127.0.0.1:5000`

- `GET /api/health`
- `GET /api/osint/username?username=<value>`
- `GET /api/osint/email?email=<value>`
- `GET /api/osint/domain?domain=<value>`
- `GET /api/reports`
- `GET /api/reports/view/<filename>`
- `GET /api/reports/download/<filename>`

## CLI Usage (Optional)

You can run scans without Flask/React:

```bash
python main.py
```

Menu options:
1. Username Search
2. Email Search
3. Domain Search
4. Exit

## Reports

- A structured HTML report is generated after each scan.
- Location: `core/reports/`
- Report content includes:
  - scan timestamp
  - platform/tool status
  - extracted links
  - raw result snapshot

## Testing

Run backend/core tests:

```bash
python -m pytest -q
```

## Troubleshooting

- **No inputs found in frontend tsconfig**
  - Already handled by enabling JS in `frontend/tsconfig.json`.
- **Tool not found errors**
  - Install missing OSINT tool and ensure it is in PATH.
- **Frontend cannot reach backend**
  - Confirm backend is running on `http://127.0.0.1:5000`.
- **No reports listed**
  - Run at least one scan, then refresh `Reports` page.

## Security and Legal Notice

Use this toolkit only for legal, authorized, and ethical security research.
