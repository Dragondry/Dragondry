# NEXUS OS

NEXUS OS is a mobile-first personal workspace with tasks, notes, an AI assistant, and installable Progressive Web App (PWA) support.

## Features
- Responsive dashboard, tasks, priorities, due dates, and notes.
- Workspace-aware AI chat using an OpenAI-compatible Chat Completions API.
- Server-side AI key handling; provider key is never placed in frontend code.
- Installable PWA on supported Android and desktop browsers.
- Offline app-shell caching; API and AI require a connection.
- Local browser storage when used without the backend; SQLite when served by FastAPI.
- JSON backup export/import in local mode.

## Run locally
Requires Python 3.10+.

```bash
cd nexus-os
python -m venv .venv
# Linux/macOS/Termux: source .venv/bin/activate
# Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

Open http://127.0.0.1:8000. API docs: http://127.0.0.1:8000/docs.

## Configure the AI brain
Set these environment variables on the backend host (never in app.js or index.html):

- `OPENAI_API_KEY`: your API key from the AI provider.
- `OPENAI_MODEL`: optional; defaults to `gpt-4o-mini`.
- `OPENAI_BASE_URL`: optional OpenAI-compatible chat-completions endpoint.

Linux/macOS/Termux example:

```bash
export OPENAI_API_KEY="your-key"
export OPENAI_MODEL="gpt-4o-mini"
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

AI calls are sent through the server. Provider usage may cost money. The assistant can read recent tasks and notes from the server database, but it cannot directly modify them yet. Local-only browser mode does not include AI chat.

## Install as an app
Host the app on an HTTPS domain. Open it in Chrome on Android, then use the browser menu and choose **Install app** or **Add to Home screen**. On supported browsers the app also offers an Install app button. Desktop Chrome/Edge can install it from the address bar or menu.

This is a PWA, not a signed APK. It can be installed without an app store. A signed Play Store release or native APK is a separate packaging/release step.

## Deploy safely
Use a Python host or container platform and persistent disk for SQLite. Configure HTTPS and the environment variables above. Before allowing public users, add authentication, per-user data isolation, rate limiting, abuse controls, and billing/usage limits. The included starter uses one shared workspace database and is not safe as a public multi-user service without those protections. Never publish your AI API key.

## Tests
```bash
pip install -r requirements.txt
python -m unittest discover -s tests -v
```
