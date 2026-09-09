"""URL validation + SSRF protection for the crawler.

Every external URL passes validate_external_url() before any network activity,
and redirect targets are re-validated. Private, loopback, link-local and
cloud-metadata ranges are refused.
"""
from __future__ import annotations

import ipaddress
import socket
from urllib.parse import urlsplit

import httpx

ALLOWED_SCHEMES = {"http", "https"}

BLOCKED_HOSTNAMES = {
    "localhost", "ip6-localhost", "ip6-loopback", "metadata.google.internal",
    "instance-data", "metadata",
}

# Ports commonly used by internal services.
BLOCKED_PORTS = {22, 25, 110, 135, 139, 143, 445, 465, 587, 993, 995, 1433, 3306,
                 5432, 6379, 8086, 9200, 27017}


class UnsafeURLError(ValueError):
    """Raised when a URL is refused by policy (SSRF guard)."""


def _blocked_ip(ip: ipaddress.IPv4Address | ipaddress.IPv6Address) -> bool:
    return (
        ip.is_private
        or ip.is_loopback
        or ip.is_link_local
        or ip.is_reserved
        or ip.is_multicast
        or ip.is_unspecified
    )


def resolve_ips(host: str) -> list[str]:
    try:
        infos = socket.getaddrinfo(host, None)
    except socket.gaierror:
        return []
    return list({info[4][0] for info in infos})


def validate_url_string(url: str) -> str:
    """Pure string-level validation (scheme/host/port/userinfo)."""
    if not url or len(url) > 800 or any(c in url for c in " \t\r\n"):
        raise UnsafeURLError("malformed or oversized URL")
    parts = urlsplit(url)
    if parts.scheme.lower() not in ALLOWED_SCHEMES:
        raise UnsafeURLError(f"scheme not allowed: {parts.scheme!r}")
    host = (parts.hostname or "").lower().rstrip(".")
    if not host:
        raise UnsafeURLError("missing host")
    if host in BLOCKED_HOSTNAMES:
        raise UnsafeURLError(f"blocked hostname: {host}")
    # Literal IPs are checked directly
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        pass
    else:
        if _blocked_ip(ip):
            raise UnsafeURLError(f"blocked IP literal: {host}")
        return url
    if parts.port and parts.port in BLOCKED_PORTS:
        raise UnsafeURLError(f"blocked port: {parts.port}")
    if parts.username or parts.password:
        raise UnsafeURLError("credentials in URL are not allowed")
    return url


def validate_external_url(url: str) -> str:
    """Full validation incl. DNS resolution against private ranges (DNS pinning
    basics: every resolved address must be public)."""
    validate_url_string(url)
    parts = urlsplit(url)
    host = (parts.hostname or "").lower().rstrip(".")
    for ip_str in resolve_ips(host):
        try:
            ip = ipaddress.ip_address(ip_str)
        except ValueError:
            raise UnsafeURLError(f"unresolvable address {ip_str} for {host}")
        if _blocked_ip(ip):
            raise UnsafeURLError(f"{host} resolves to non-public address {ip_str}")
    return url


class SafeRedirectValidator:
    """httpx event hook that re-validates every redirect location."""

    def __call__(self, request: httpx.Request) -> None:  # pragma: no cover - thin guard
        if request.url is None:
            return
        url = str(request.url)
        try:
            validate_url_string(url)
        except UnsafeURLError as exc:
            raise httpx.HTTPError(f"redirect refused: {exc}") from exc
