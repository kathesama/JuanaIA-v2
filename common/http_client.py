from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

import httpx

from common.errors import DownstreamError


@dataclass
class HttpClient:
    base_url: str
    timeout_seconds: float = 10.0
    default_headers: Optional[Dict[str, str]] = None
    transport: Optional[httpx.BaseTransport] = None

    def _client(self) -> httpx.Client:
        return httpx.Client(
            base_url=self.base_url,
            timeout=self.timeout_seconds,
            headers=self.default_headers,
            transport=self.transport,
        )

    def get(self, path: str, *, correlation_id: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._request("GET", path, correlation_id=correlation_id, params=params, retries=1)

    def post(self, path: str, *, correlation_id: str, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._request("POST", path, correlation_id=correlation_id, json=json, retries=0)

    def _request(
        self,
        method: str,
        path: str,
        *,
        correlation_id: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        retries: int = 0,
    ) -> Dict[str, Any]:
        headers = {"X-Correlation-Id": correlation_id}
        if self.default_headers:
            headers.update(self.default_headers)

        attempt = 0
        while True:
            attempt += 1
            try:
                with self._client() as client:
                    response = client.request(method, path, headers=headers, params=params, json=json)
                if response.status_code >= 400:
                    raise DownstreamError(
                        code="downstream_error",
                        message=f"{method} {path} failed",
                        status_code=502,
                        details={"body": response.text},
                        correlation_id=correlation_id,
                        service=self.base_url,
                        url=str(response.url),
                        upstream_status=response.status_code,
                    )
                return response.json()
            except httpx.TimeoutException as exc:
                if method == "GET" and attempt <= retries:
                    continue
                raise DownstreamError(
                    code="downstream_timeout",
                    message=f"Timeout calling {method} {path}",
                    status_code=504,
                    details={"error": str(exc)},
                    correlation_id=correlation_id,
                    service=self.base_url,
                    url=f"{self.base_url}{path}",
                ) from exc
            except httpx.RequestError as exc:
                if method == "GET" and attempt <= retries:
                    continue
                raise DownstreamError(
                    code="downstream_unreachable",
                    message=f"Request error calling {method} {path}",
                    status_code=502,
                    details={"error": str(exc)},
                    correlation_id=correlation_id,
                    service=self.base_url,
                    url=f"{self.base_url}{path}",
                ) from exc
