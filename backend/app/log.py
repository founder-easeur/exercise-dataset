"""Structured JSON logging for pipeline + API events.

One line per event as JSON so logs are greppable and machine-parseable.
"""
from __future__ import annotations

import json
import logging
import sys
from datetime import datetime, timezone

_CONFIGURED = False

EVENT_TYPES = {
    "crawl_started", "crawl_completed", "crawl_failed", "url_skipped",
    "exercise_extracted", "exercise_rejected", "duplicate_detected",
    "conflict_detected", "ai_extraction_performed", "review_action",
}


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        extra = getattr(record, "event_data", None)
        if isinstance(extra, dict):
            payload.update(extra)
        if record.exc_info and record.exc_info[0]:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, default=str)


def configure_logging(level: int = logging.INFO) -> None:
    global _CONFIGURED
    if _CONFIGURED:
        return
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(level)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    _CONFIGURED = True


def log_event(logger: logging.Logger, event: str, level: int = logging.INFO, **data) -> None:
    """Emit a structured pipeline event, e.g. log_event(log, 'duplicate_detected', a=1)."""
    logger.log(level, event, extra={"event_data": {"event": event, **data}})
