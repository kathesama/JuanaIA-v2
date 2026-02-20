import httpx
import pytest

from common.errors import DownstreamError
from common.http_client import HttpClient


def test_get_retries_once_on_timeout():
    calls = {"count": 0}

    def handler(request):
        calls["count"] += 1
        if calls["count"] == 1:
            raise httpx.TimeoutException("boom")
        return httpx.Response(200, json={"ok": True})

    transport = httpx.MockTransport(handler)
    client = HttpClient(base_url="http://test", timeout_seconds=0.01, transport=transport)

    result = client.get("/health", correlation_id="cid-1")
    assert result == {"ok": True}
    assert calls["count"] == 2


def test_post_timeout_no_retry():
    def handler(request):
        raise httpx.TimeoutException("boom")

    transport = httpx.MockTransport(handler)
    client = HttpClient(base_url="http://test", timeout_seconds=0.01, transport=transport)

    with pytest.raises(DownstreamError) as exc:
        client.post("/ask", correlation_id="cid-2", json={"q": "hi"})

    assert exc.value.code == "downstream_timeout"


def test_error_status_raises_downstream_error():
    def handler(request):
        return httpx.Response(500, json={"error": "fail"})

    transport = httpx.MockTransport(handler)
    client = HttpClient(base_url="http://test", transport=transport)

    with pytest.raises(DownstreamError) as exc:
        client.get("/health", correlation_id="cid-3")

    assert exc.value.code == "downstream_error"
