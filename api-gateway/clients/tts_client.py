from schemas.downstream import TTSSpeakResponse
from common.http_client import HttpClient


class TTSClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def speak(self, *, correlation_id: str, text: str) -> dict:
        payload = self._http.post("/speak", correlation_id=correlation_id, json={"text": text})
        data = TTSSpeakResponse.model_validate(payload)
        return data.model_dump()
