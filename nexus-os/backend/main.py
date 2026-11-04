import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = Path(os.getenv("NEXUS_DB_PATH", str(ROOT / "nexus-os.db")))
app = FastAPI(title="NEXUS OS API", version="0.1.0", description="Personal workspace API")
@contextmanager
def db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def init_db():
    with db() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS tasks (
          id TEXT PRIMARY KEY, title TEXT NOT NULL, description TEXT NOT NULL DEFAULT '',
          priority TEXT NOT NULL DEFAULT 'Normal', status TEXT NOT NULL DEFAULT 'open',
          due_date TEXT, created_at TEXT NOT NULL, updated_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS notes (
          id TEXT PRIMARY KEY, title TEXT NOT NULL, content TEXT NOT NULL DEFAULT '',
          created_at TEXT NOT NULL, updated_at TEXT NOT NULL
        );
        """)
init_db()
def now(): return datetime.now(timezone.utc).isoformat()
class TaskIn(BaseModel):
    title: str = Field(min_length=1, max_length=180)
    description: str = Field(default="", max_length=2000)
    priority: str = Field(default="Normal", pattern="^(Low|Normal|High)$")
    status: str = Field(default="open", pattern="^(open|done)$")
    due_date: Optional[str] = None
class TaskPatch(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=180)
    description: Optional[str] = Field(default=None, max_length=2000)
    priority: Optional[str] = Field(default=None, pattern="^(Low|Normal|High)$")
    status: Optional[str] = Field(default=None, pattern="^(open|done)$")
    due_date: Optional[str] = None
class NoteIn(BaseModel):
    title: str = Field(min_length=1, max_length=180)
    content: str = Field(default="", max_length=10000)
class NotePatch(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=180)
    content: Optional[str] = Field(default=None, max_length=10000)
def rows(table):
    with db() as c: return [dict(r) for r in c.execute(f"SELECT * FROM {table} ORDER BY created_at DESC")]
@app.get("/api/health")
def health(): return {"ok": True, "service": "nexus-os", "version": "0.1.0"}
@app.get("/api/tasks")
def list_tasks(): return rows("tasks")
@app.post("/api/tasks", status_code=201)
def create_task(payload: TaskIn):
    import uuid
    stamp=now(); item=payload.model_dump(); item.update(id=str(uuid.uuid4()),created_at=stamp,updated_at=stamp)
    with db() as c: c.execute("INSERT INTO tasks VALUES (:id,:title,:description,:priority,:status,:due_date,:created_at,:updated_at)",item)
    return item
@app.patch("/api/tasks/{task_id}")
def update_task(task_id: str, payload: TaskPatch):
    changes=payload.model_dump(exclude_unset=True)
    with db() as c:
        old=c.execute("SELECT * FROM tasks WHERE id=?",(task_id,)).fetchone()
        if not old: raise HTTPException(404,"Task not found")
        item=dict(old); item.update(changes); item["updated_at"]=now()
        c.execute("UPDATE tasks SET title=:title,description=:description,priority=:priority,status=:status,due_date=:due_date,updated_at=:updated_at WHERE id=:id",item)
    return item
@app.delete("/api/tasks/{task_id}",status_code=204)
def remove_task(task_id: str):
    with db() as c:
        cur=c.execute("DELETE FROM tasks WHERE id=?",(task_id,))
        if not cur.rowcount: raise HTTPException(404,"Task not found")
@app.get("/api/notes")
def list_notes(): return rows("notes")
@app.post("/api/notes",status_code=201)
def create_note(payload: NoteIn):
    import uuid
    stamp=now(); item=payload.model_dump(); item.update(id=str(uuid.uuid4()),created_at=stamp,updated_at=stamp)
    with db() as c: c.execute("INSERT INTO notes VALUES (:id,:title,:content,:created_at,:updated_at)",item)
    return item
@app.patch("/api/notes/{note_id}")
def update_note(note_id: str,payload: NotePatch):
    changes=payload.model_dump(exclude_unset=True)
    with db() as c:
        old=c.execute("SELECT * FROM notes WHERE id=?",(note_id,)).fetchone()
        if not old: raise HTTPException(404,"Note not found")
        item=dict(old);item.update(changes);item["updated_at"]=now()
        c.execute("UPDATE notes SET title=:title,content=:content,updated_at=:updated_at WHERE id=:id",item)
    return item
@app.delete("/api/notes/{note_id}",status_code=204)
def remove_note(note_id: str):
    with db() as c:
        cur=c.execute("DELETE FROM notes WHERE id=?",(note_id,))
        if not cur.rowcount: raise HTTPException(404,"Note not found")
@app.get("/")
def home(): return FileResponse(ROOT / "index.html")
app.mount("/",StaticFiles(directory=ROOT,html=True),name="static")
