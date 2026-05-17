from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health() -> None:
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_tokens_default_length() -> None:
    r = client.get("/tokens")
    assert r.status_code == 200
    body = r.json()
    assert "token" in body
    assert len(body["token"]) > 20


def test_tokens_custom_length() -> None:
    r = client.get("/tokens?length=64")
    assert r.status_code == 200
    assert len(r.json()["token"]) > 50


def test_tokens_rejects_short_length() -> None:
    r = client.get("/tokens?length=4")
    assert r.status_code == 400
    assert "length" in r.json()["detail"]


def test_regions_structure() -> None:
    """Skip in environments without AWS creds — check structure only when reachable."""
    r = client.get("/regions")
    if r.status_code == 502:
        return  # No AWS creds — that's fine for offline tests
    assert r.status_code == 200
    body = r.json()
    assert body["count"] > 0
    assert isinstance(body["regions"], list)

