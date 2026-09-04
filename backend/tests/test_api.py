"""API tests: endpoints, filters, pagination, exports."""
from __future__ import annotations

from tests.conftest import AUTH


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_openapi_documentation(client):
    r = client.get("/openapi.json")
    assert r.status_code == 200
    spec = r.json()
    assert "/api/v1/exercises" in spec["paths"]
    assert "/api/v1/exercises/{id_or_slug}" in spec["paths"]
    assert "/api/v1/muscles" in spec["paths"]
    assert "/api/v1/body-regions" in spec["paths"]
    assert "/api/v1/joints" in spec["paths"]
    assert "/api/v1/equipment" in spec["paths"]
    assert "/api/v1/exercises/search" in spec["paths"]


def test_list_exercises_empty(client):
    r = client.get("/api/v1/exercises")
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == 0 and body["items"] == []


def test_list_filter_pagination(client, seeded):
    r = client.get("/api/v1/exercises", params={"status": "all", "page_size": 10})
    body = r.json()
    assert body["total"] == 148
    assert len(body["items"]) == 10
    item = body["items"][0]
    for field in ("slug", "name", "type", "difficulty", "body_regions",
                  "primary_muscles", "equipment", "confidence", "review_status"):
        assert field in item, field


def test_consumer_default_returns_approved_only(client, seeded):
    r = client.get("/api/v1/exercises")
    assert r.json()["total"] == 148  # curated seeds are approved


def test_filters(client, seeded):
    # body region
    r = client.get("/api/v1/exercises", params={"status": "all", "body_region": "neck"})
    assert r.json()["total"] > 0
    assert all(any(br["slug"] == "neck" for br in it["body_regions"])
               for it in r.json()["items"])
    # muscle
    r = client.get("/api/v1/exercises", params={
        "status": "all", "muscle": "levator-scapulae"})
    assert r.json()["total"] >= 2
    # exercise type
    r = client.get("/api/v1/exercises", params={"status": "all", "type": "stretching"})
    assert r.json()["total"] > 5
    # equipment
    r = client.get("/api/v1/exercises", params={
        "status": "all", "equipment": "resistance-band"})
    assert r.json()["total"] >= 2
    # difficulty + confidence
    r = client.get("/api/v1/exercises", params={
        "status": "all", "difficulty": "beginner", "confidence_min": 0.5})
    assert r.json()["total"] > 5
    # search q
    r = client.get("/api/v1/exercises/search", params={"q": "neck"})
    assert r.json()["total"] >= 2


def test_exercise_detail(client, seeded):
    listing = client.get("/api/v1/exercises", params={"status": "all"}).json()["items"]
    slug = listing[0]["slug"]
    r = client.get(f"/api/v1/exercises/{slug}")
    assert r.status_code == 200
    detail = r.json()
    assert detail["instructions"]
    assert "sources" in detail and isinstance(detail["sources"], list)
    assert "provenance" not in detail  # research metadata excluded by default

    r2 = client.get(f"/api/v1/exercises/{slug}", params={"include": "research"})
    assert "provenance" in r2.json()

    assert client.get("/api/v1/exercises/does-not-exist").status_code == 404


def test_muscles_endpoints(client, seeded):
    r = client.get("/api/v1/muscles", params={"q": "levator scap"})
    assert r.json()["total"] == 1
    slug = r.json()["items"][0]["slug"]
    r2 = client.get(f"/api/v1/muscles/{slug}")
    body = r2.json()
    assert body["exercise_count"] >= 1
    assert "exercises" in body and "coverage" in body


def test_reference_endpoints(client, seeded):
    assert client.get("/api/v1/body-regions").json()["total"] == 16
    assert client.get("/api/v1/joints").json()["total"] == 23
    assert client.get("/api/v1/equipment").json()["total"] == 18
    assert client.get("/api/v1/exercise-types").json()["total"] == 12
    region = client.get("/api/v1/body-regions/neck").json()
    assert region["exercise_count"] > 0


def test_stats_and_coverage(client, seeded):
    dash = client.get("/api/v1/stats/dashboard").json()
    assert dash["total_exercises"] == 148
    assert dash["muscles_total"] == 121
    cov = client.get("/api/v1/stats/coverage/muscles").json()
    assert cov["total"] == 121
    assert cov["summary"]["missing"] + cov["summary"]["limited"] + \
        cov["summary"]["good"] + cov["summary"]["excellent"] + \
        cov["summary"]["needs_review"] == 121
    regions = client.get("/api/v1/stats/coverage/regions").json()["items"]
    assert any(r["slug"] == "neck" for r in regions)


def test_export_formats(client, seeded):
    r = client.get("/api/v1/export", params={"dataset": "exercises", "fmt": "json"})
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("application/json")
    assert len(r.json()["exercises"]) == 148
    r = client.get("/api/v1/export", params={"dataset": "exercises", "fmt": "jsonl"})
    lines = r.text.strip().split("\n")
    assert len(lines) == 148
    r = client.get("/api/v1/export", params={"dataset": "exercises", "fmt": "csv"})
    assert r.text.splitlines()[0].startswith("id,slug,name")
    r = client.get("/api/v1/export", params={"dataset": "muscles", "fmt": "json"})
    assert len(r.json()) == 121
    r = client.get("/api/v1/export", params={"dataset": "bogus"})
    assert r.status_code == 400


def test_review_queue_requires_auth_for_actions(client, seeded):
    item = {"action": "flag", "note": "test"}
    r = client.post("/api/v1/review/1/action", json=item)
    assert r.status_code == 401
    r = client.post("/api/v1/review/1/action", json=item, headers={"X-API-Key": "wrong"})
    assert r.status_code == 401


def test_crawl_admin_requires_auth(client):
    assert client.post("/api/v1/admin/crawl", json={"mode": "replay"}).status_code == 401
    r = client.post("/api/v1/admin/crawl", json={"mode": "bogus"}, headers=AUTH)
    assert r.status_code == 422
