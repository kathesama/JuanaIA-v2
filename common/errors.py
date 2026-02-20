from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class AppError(Exception):
    code: str
    message: str
    status_code: int = 500
    details: Optional[Dict[str, Any]] = None
    correlation_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "error": {
                "code": self.code,
                "message": self.message,
            }
        }
        if self.details is not None:
            payload["error"]["details"] = self.details
        if self.correlation_id:
            payload["error"]["correlation_id"] = self.correlation_id
        return payload


@dataclass
class DownstreamError(AppError):
    service: str = "unknown"
    url: str = ""
    upstream_status: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        payload = super().to_dict()
        payload["error"]["service"] = self.service
        payload["error"]["url"] = self.url
        if self.upstream_status is not None:
            payload["error"]["upstream_status"] = self.upstream_status
        return payload
