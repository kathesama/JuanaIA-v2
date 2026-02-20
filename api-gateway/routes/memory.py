from fastapi import APIRouter, Depends, Request

from routes.deps import get_correlation_id
from common.config import load_config
from common.http_client import HttpClient
from clients.memory_client import MemoryClient

router = APIRouter()


@router.post("/resetMemory")
def reset_memory(request: Request):
    correlation_id = get_correlation_id(request)
    config = load_config()
    client = MemoryClient(HttpClient(base_url=config.memory.base_url, timeout_seconds=config.timeout_seconds))
    result = client.reset(correlation_id=correlation_id)
    return {"status": "ok", "memory": result.model_dump()}
