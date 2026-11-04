import os
import tempfile
import unittest
from pathlib import Path
from fastapi.testclient import TestClient

_tmp = tempfile.TemporaryDirectory()
os.environ["NEXUS_DB_PATH"] = str(Path(_tmp.name) / "test.db")
from backend.main import app
client = TestClient(app)

class NexusApiTests(unittest.TestCase):
    def test_health(self):
        self.assertTrue(client.get("/api/health").json()["ok"])
    def test_task_lifecycle(self):
        r=client.post("/api/tasks",json={"title":"Test task","priority":"High"})
        self.assertEqual(r.status_code,201); item=r.json(); task_id=item["id"]
        self.assertEqual(client.get("/api/tasks").status_code,200)
        self.assertEqual(client.patch(f"/api/tasks/{task_id}",json={"status":"done"}).json()["status"],"done")
        self.assertEqual(client.delete(f"/api/tasks/{task_id}").status_code,204)
        self.assertEqual(client.delete(f"/api/tasks/{task_id}").status_code,404)
    def test_note_lifecycle(self):
        r=client.post("/api/notes",json={"title":"Idea","content":"A useful thought"})
        self.assertEqual(r.status_code,201); note_id=r.json()["id"]
        self.assertEqual(client.patch(f"/api/notes/{note_id}",json={"title":"Updated"}).json()["title"],"Updated")
        self.assertEqual(client.delete(f"/api/notes/{note_id}").status_code,204)
    def test_validation(self):
        self.assertEqual(client.post("/api/tasks",json={"title":"","priority":"Urgent"}).status_code,422)
if __name__ == "__main__": unittest.main()
