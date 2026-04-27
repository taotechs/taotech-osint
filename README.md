# Taotech OSINT Toolkit

Clean, modular, and beginner-friendly OSINT toolkit built with Python 3.10+.

## Features

- Username OSINT with `maigret` and `sherlock`
- Email OSINT with `holehe`
- Domain OSINT with `theHarvester`
- Menu-driven CLI
- Structured subprocess execution (`subprocess`, not `os.system`)
- Logging to `logs.txt`
- Report output in `reports/`

## Project Structure

```text
taotech-osint/
├── main.py
├── core/
│   └── modules/
│       ├── username.py
│       ├── email.py
│       └── domain.py
│   └── utils/
│       ├── runner.py
│       └── logger.py
├── backend/
│   ├── app.py
│   ├── routes/
│   │   ├── username_routes.py
│   │   ├── email_routes.py
│   │   └── domain_routes.py
│   ├── services/
│   │   ├── osint_bridge.py
│   │   └── osint_service.py
│   └── utils/
│       ├── response.py
│       └── logger.py
├── modules/
│   ├── username.py
│   ├── email.py
│   └── domain.py
├── utils/
│   ├── logger.py
│   └── runner.py
├── reports/
├── requirements.txt
└── README.md
```

## Installation

1. Make sure Python 3.10+ is installed.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

> You may also need to ensure CLI tools are available in your system PATH.

## Usage

Run:

```bash
python main.py
```

Then select:

1. Username Search
2. Email Search
3. Domain Search
4. Exit

## Flask API Usage

Run:

```bash
python -m backend.app
```

Available endpoints:

- `GET /api/health`
- `GET /api/reports`
- `GET /api/osint/username?username=target`
- `GET /api/osint/email?email=target@example.com`
- `GET /api/osint/domain?domain=example.com`
- `GET /reports/<filename>.html`

## React Frontend Usage

The dashboard frontend is in `frontend/` and consumes the Flask API at `http://127.0.0.1:5000`.

Run frontend:

```bash
cd frontend
npm install
npm run dev
```

## End-to-End Run

1. Start Flask backend:
```bash
python -m backend.app
```
2. Start React frontend in a new terminal:
```bash
cd frontend
npm run dev
```
3. Open the Vite URL (usually `http://127.0.0.1:5173`) and run scans from the dashboard.

## Architecture Flow

- React dashboard calls Flask API endpoints only.
- Flask routes call `backend/services/osint_bridge.py` only.
- Bridge layer calls `core/modules/*` only.
- Core modules call OSINT tool binaries (`maigret`, `sherlock`, `holehe`, `theHarvester`).

## Structured Reporting

- Each scan now generates a styled HTML report in `core/reports/`.
- Reports include timestamp, platforms found, extracted links, and raw result snapshot.
- Reports API:
  - `GET /api/reports`
  - `GET /api/reports/view/<filename>`
  - `GET /api/reports/download/<filename>`

## Notes

- Username scans save reports to the `reports/` directory.
- If a tool is not installed, the toolkit shows a clean error message and continues.
- All scan activities are logged in `logs.txt`.

## Disclaimer

Use this toolkit only for legal and authorized security research.
