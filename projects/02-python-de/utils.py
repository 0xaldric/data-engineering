"""Shared utilities: logging, config, retry, custom exceptions.

Dùng chung cho mọi script trong Phase 1. Demo: python projects/02-python-de/utils.py
"""
from __future__ import annotations

import functools
import logging
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

import yaml

# ---------------------------------------------------------------------
# 1) Logging — cấu hình một chỗ, format có timestamp + level + tên logger
# ---------------------------------------------------------------------
_FMT = "%(asctime)s [%(levelname)-5s] %(name)s: %(message)s"
_DATEFMT = "%Y-%m-%d %H:%M:%S"


def get_logger(name: str, level: str = "INFO") -> logging.Logger:
    """Trả logger đã cấu hình; idempotent (không gắn handler trùng khi gọi lại)."""
    logger = logging.getLogger(name)
    if not logger.handlers:                       # tránh log bị nhân đôi
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(_FMT, datefmt=_DATEFMT))
        logger.addHandler(handler)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    logger.propagate = False
    return logger


# ---------------------------------------------------------------------
# 2) Config — tách khỏi code. Ưu tiên: defaults < YAML file < env vars
# ---------------------------------------------------------------------
@dataclass
class Config:
    api_url: str = "https://jsonplaceholder.typicode.com/posts"
    page_size: int = 20
    max_pages: int = 5
    timeout: int = 5
    log_level: str = "INFO"


_ENV_PREFIX = "DE_"  # vd DE_PAGE_SIZE=50 sẽ override page_size


def load_config(path: str | Path | None = None) -> Config:
    cfg = Config()
    # (a) từ YAML nếu có
    if path and Path(path).exists():
        data = yaml.safe_load(Path(path).read_text()) or {}
        for k, v in data.items():
            if hasattr(cfg, k):
                setattr(cfg, k, v)
    # (b) từ env vars (ưu tiên cao nhất) — ép kiểu theo default hiện có
    for field_name in cfg.__dataclass_fields__:
        env_key = _ENV_PREFIX + field_name.upper()
        if env_key in os.environ:
            current = getattr(cfg, field_name)
            raw = os.environ[env_key]
            setattr(cfg, field_name, type(current)(raw))
    return cfg


# ---------------------------------------------------------------------
# 3) Custom exceptions — phân loại lỗi theo tầng pipeline
# ---------------------------------------------------------------------
class PipelineError(Exception):
    """Base cho mọi lỗi pipeline."""


class ExtractError(PipelineError):
    pass


class TransformError(PipelineError):
    pass


class LoadError(PipelineError):
    pass


# ---------------------------------------------------------------------
# 4) Retry decorator — exponential backoff, tái dùng khắp nơi
# ---------------------------------------------------------------------
def retry(exceptions: tuple[type[Exception], ...] = (Exception,),
          tries: int = 3, backoff: float = 0.5,
          logger: logging.Logger | None = None) -> Callable:
    def decorator(fn: Callable) -> Callable:
        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            log = logger or get_logger("retry")
            for attempt in range(1, tries + 1):
                try:
                    return fn(*args, **kwargs)
                except exceptions as exc:
                    if attempt == tries:
                        log.error("'%s' thất bại sau %d lần: %s", fn.__name__, tries, exc)
                        raise
                    wait = backoff * (2 ** (attempt - 1))
                    log.warning("'%s' lỗi (%s), thử lại %d/%d sau %.1fs",
                                fn.__name__, exc, attempt + 1, tries, wait)
                    time.sleep(wait)
        return wrapper
    return decorator


# ---------------------------------------------------------------------
# 5) Redact secrets — không bao giờ log mật khẩu/token
# ---------------------------------------------------------------------
_SECRET_KEYS = {"password", "token", "secret", "api_key", "authorization"}


def redact(data: dict, mask: str = "***") -> dict:
    return {k: (mask if k.lower() in _SECRET_KEYS else v) for k, v in data.items()}


# ---------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------
def _demo() -> None:
    log = get_logger("utils.demo", level="DEBUG")
    log.info("== Logging ==")
    log.debug("debug detail (chỉ hiện khi level=DEBUG)")
    log.info("info bình thường")
    log.warning("cảnh báo")

    log.info("== Config (defaults < YAML < env) ==")
    os.environ["DE_PAGE_SIZE"] = "50"   # giả lập override từ môi trường
    cfg = load_config()
    log.info("config: api_url=%s page_size=%s (env override) log_level=%s",
             cfg.api_url, cfg.page_size, cfg.log_level)
    assert cfg.page_size == 50, "env override không hoạt động"

    log.info("== Redact secrets ==")
    creds = {"user": "admin", "password": "hunter2", "api_key": "sk-123"}
    log.info("connection params: %s", redact(creds))

    log.info("== Retry decorator ==")
    calls = {"n": 0}

    @retry(exceptions=(ValueError,), tries=3, backoff=0.05, logger=log)
    def flaky() -> str:
        calls["n"] += 1
        if calls["n"] < 3:
            raise ValueError(f"tạm lỗi lần {calls['n']}")
        return "thành công"

    result = flaky()
    log.info("flaky() -> %r sau %d lần gọi", result, calls["n"])

    log.info("== Custom exceptions ==")
    try:
        raise ExtractError("không kết nối được nguồn")
    except PipelineError as exc:
        log.error("Bắt được %s: %s", type(exc).__name__, exc)

    print("\nDONE ✅ utils demo chạy xong.")


if __name__ == "__main__":
    _demo()
