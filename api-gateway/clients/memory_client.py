from typing import List

from schemas.downstream import MemoryRecallResponse, MemoryRememberResponse, MemoryResetResponse
from common.http_client import HttpClient


class MemoryClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def recall(self, *, correlation_id: str, limit: int = 10) -> List[str]:
        payload = self._http.get("/recall", correlation_id=correlation_id, params={"limit": limit})
        data = MemoryRecallResponse.model_validate(payload)
        return data.recent

    def remember(self, *, correlation_id: str, text: str, role: str, tags: List[str]) -> None:
        payload = {"text": text, "role": role, "tags": tags}
        resp = self._http.post("/remember", correlation_id=correlation_id, json=payload)
        MemoryRememberResponse.model_validate(resp)

    def reset(self, *, correlation_id: str) -> MemoryResetResponse:
        resp = self._http.post("/reset", correlation_id=correlation_id, json={})
        return MemoryResetResponse.model_validate(resp)
