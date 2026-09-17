"""Security tests: SSRF protection, URL validation, admin auth."""
from __future__ import annotations

import pytest

from app.pipeline.security import UnsafeURLError, validate_url_string
from tests.conftest import AUTH


@pytest.mark.parametrize("url", [
    "http://localhost/admin",
    "http://127.0.0.1:8000/api",
    "http://10.0.0.1/resource",
    "http://192.168.1.1/router",
    "http://169.254.169.254/latest/meta-data/",   # cloud metadata
    "http://metadata.google.internal/computeMetadata/v1/",
    "http://172.16.0.1/internal",
    "http://[::1]/",                               # IPv6 loopback
    "http://[fd00::1]/",                            # IPv6 private
    "ftp://example.com/file",
    "file:///etc/passwd",
    "javascript:alert(1)",
    "http://user:pass@example.com/",
    "http://example.com:5432/db",                   # DB port
    "not a url",
    "http://example.com/%0d%0aHeader: injected",    # CRLF
])
def test_unsafe_urls_rejected(url):
    with pytest.raises(UnsafeURLError):
        validate_url_string(url)


@pytest.mark.parametrize("url", [
    "https://www.orthoinfo.org/recovery/knee-conditioning-program/",
    "https://www.arthritis-uk.org/exercise",
    "http://example.org/page",
])
def test_safe_urls_accepted(url):
    assert validate_url_string(url) == url


def test_fetcher_refuses_private_targets():
    from app.pipeline.fetcher import Fetcher
    f = Fetcher(cache_dir="/tmp/easeur-test-cache")
    result = f.fetch("http://169.254.169.254/latest/meta-data/", use_cache=False)
    assert not result.ok
    assert result.error and "blocked" in result.error.lower()


def test_admin_endpoints_require_key(client, seeded):
    for path in ("/api/v1/audit",):
        assert client.get(path).status_code == 401
        assert client.get(path, headers=AUTH).status_code == 200
    for method, path in (("post", "/api/v1/admin/dedup"), ("post", "/api/v1/admin/validate")):
        assert client.request(method, path).status_code == 401


def test_health_is_public(client):
    assert client.get("/health").status_code == 200
