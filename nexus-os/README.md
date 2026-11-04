# NEXUS OS

NEXUS OS is a mobile-first personal workspace with tasks, notes, an AI assistant, and installable Progressive Web App (PWA) support.

## Features
- Responsive dashboard, tasks, priorities, due dates, and notes.
- Workspace-aware AI chat using an OpenAI-compatible Chat Completions API.
- Bring your own key (BYOK): each user can supply an OpenAI API key in Settings; it is kept in browser session storage and sent per request, never saved in the NEXUS database.
- Installable PWA on supported Android and desktop browsers.
- Offline app-shell caching; API and AI require a connection.
- Local browser storage when used without the backend; SQLite for local development or PostgreSQL via `DATABASE_URL` for hosted deployments.
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

## Configure AI (BYOK)
Each user can paste their own OpenAI API key in **Settings → AI assistant**. The key is held in session storage for the current browser session and sent to the backend in an `X-OpenAI-API-Key` request header. The backend does not write this key to SQLite or logs. Use HTTPS and only send the key to a server you trust. The user is responsible for their provider's API charges.

A server owner may optionally set a fallback key using these environment variables (never put it in app.js or index.html):

- `OPENAI_API_KEY`: your API key from the AI provider.
- `OPENAI_MODEL`: optional; defaults to `gpt-4o-mini`.
- `OPENAI_BASE_URL`: optional OpenAI-compatible chat-completions endpoint.

Linux/macOS/Termux example:

```bash
export OPENAI_API_KEY="your-key"
export OPENAI_MODEL="gpt-4o-mini"
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

AI calls are sent through the server. With BYOK, provider usage is billed to the user whose key is supplied. A server fallback key, if configured, is billed to the server owner. The assistant can read recent tasks and notes from the server database, but it cannot directly modify them yet. Local-only browser mode does not include AI chat.

## Install as an app
Host the app on an HTTPS domain. Open it in Chrome on Android, then use the browser menu and choose **Install app** or **Add to Home screen**. On supported browsers the app also offers an Install app button. Desktop Chrome/Edge can install it from the address bar or menu.

This is a PWA, not a signed APK. It can be installed without an app store. A signed Play Store release or native APK is a separate packaging/release step.

## Deploy safely
For a free test deployment, use a Render Free web service and a Neon Free PostgreSQL database. Set `DATABASE_URL` in the Render service environment (use the pooled or direct Neon connection string with SSL enabled). Render Free services sleep after 15 minutes idle and have ephemeral local files, so do not rely on SQLite for hosted data. Configure HTTPS and the environment variables above. Before allowing public users, add authentication, per-user data isolation, rate limiting, abuse controls, and billing/usage limits. The included starter uses one shared workspace database and is not safe as a public multi-user service without those protections. Never publish your AI API key.

## Tests
```bash
pip install -r requirements.txt
python -m unittest discover -s tests -v
```
