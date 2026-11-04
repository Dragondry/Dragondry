# NEXUS OS

A practical, mobile-first personal workspace with tasks, notes, search, and a FastAPI + SQLite backend.

> NEXUS OS is an application starter, not a phone operating system. It runs in a browser on Android, desktop, and tablet.

## Features
- Responsive dashboard with task and note management.
- Search across tasks and notes.
- Task status and priority, due dates, and quick filters.
- Notes with create, edit, and delete.
- Local-first mode: works without a server and stores data in this browser.
- Optional FastAPI backend with SQLite persistence and health status.
- API documentation at `/docs` when the backend is running.
- No account, API key, or external service required for local mode.

## Run the app

### Easiest: browser-only mode
Open `index.html` from this folder in a browser, or publish this folder using GitHub Pages (see below). Data is stored in the browser's local storage on that device.

### Full-stack mode
Requires Python 3.10+.

```bash
cd nexus-os
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux/Android Termux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

Open `http://127.0.0.1:8000` to use the app and `http://127.0.0.1:8000/docs` for interactive API docs.

The API stores data in `nexus-os.db` (or `NEXUS_DB_PATH` if set). The browser UI automatically uses the API when served by the backend; otherwise it falls back to local mode.

## API
- `GET /api/health`
- `GET /api/tasks`, `POST /api/tasks`
- `PATCH /api/tasks/{id}`, `DELETE /api/tasks/{id}`
- `GET /api/notes`, `POST /api/notes`
- `PATCH /api/notes/{id}`, `DELETE /api/notes/{id}`

## Tests
```bash
pip install -r requirements.txt
python -m unittest discover -s tests -v
```

## Deploy
For a private or public hosted instance, deploy the backend to a Python host and configure HTTPS. Do not expose a writable instance publicly without adding authentication and rate limiting. The included app is intended for personal/local use; it does not claim to provide multi-user security.

## Project layout
- `index.html`, `app.js`, `styles.css`: responsive browser application.
- `backend/main.py`: FastAPI + SQLite service.
- `tests/`: API tests.
- `Dockerfile`: container build.
