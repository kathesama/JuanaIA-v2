from schemas.downstream import LLMGenerateResponse
from common.http_client import HttpClient


class LLMClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def generate(self, *, correlation_id: str, prompt: str) -> str:
        payload = self._http.post("/generate", correlation_id=correlation_id, json={"prompt": prompt})
        data = LLMGenerateResponse.model_validate(payload)
        return data.response
