from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="juana-memory")

_memory: List[dict] = []


class RememberItem(BaseModel):
    text: str
    role: Optional[str] = "system"
    tags: Optional[List[str]] = []


@app.get("/health")
def health():
    return {"status": "ok", "service": "memory", "backend": "in-memory"}


@app.post("/remember")
def remember(item: RememberItem):
    doc = {
        "text": item.text,
        "role": item.role or "system",
        "tags": item.tags or [],
        "ts": datetime.utcnow().isoformat(),
    }
    _memory.append(doc)
    return {"status": "ok", "inserted_id": str(len(_memory) - 1)}


@app.get("/recall")
def recall(limit: int = 10):
    recent_raw = list(reversed(_memory))[:limit]
    recent = [doc["text"] for doc in recent_raw]
    return {"status": "ok", "recent": recent}


@app.post("/reset")
def reset():
    _memory.clear()
    return {"status": "ok", "message": "memoria limpiada"}
