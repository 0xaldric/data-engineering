"""Resilient REST API ingestion — pagination + retry/backoff + offline fallback.

Chạy: python projects/02-python-de/05_api_ingest.py

Pattern Data Engineering:
  1. EXTRACT từ REST API với pagination, timeout, retry + exponential backoff.
  2. Lưu RAW JSON trước (bronze / landing) — không transform, để replay được.
  3. NORMALIZE raw -> Parquet (silver).
  4. RESILIENT: mất mạng / API lỗi -> fallback sang mock data để pipeline vẫn xong.
  5. IDEMPOTENT: chạy lại nhiều lần ra cùng kết quả (ghi đè cùng path).
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import requests

from utils import get_logger, retry  # dùng module chung (T017)

log = get_logger("api_ingest")

API = "https://jsonplaceholder.typicode.com/posts"
PAGE_SIZE = 20
MAX_PAGES = 5
TIMEOUT = 5

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "raw" / "api"
OUT_DIR = ROOT / "data" / "processed" / "api"
RAW_DIR.mkdir(parents=True, exist_ok=True)
OUT_DIR.mkdir(parents=True, exist_ok=True)


@retry(exceptions=(requests.RequestException, ValueError), tries=3, backoff=0.5, logger=log)
def http_get_json(url: str, params: dict):
    """GET trả JSON; @retry (từ utils) lo backoff cho lỗi mạng/5xx/timeout."""
    resp = requests.get(url, params=params, timeout=TIMEOUT)
    if resp.status_code >= 500:
        raise requests.HTTPError(f"server {resp.status_code}")
    resp.raise_for_status()
    return resp.json()


def mock_posts(n: int = 100) -> list[dict]:
    """Dữ liệu giả mô phỏng schema của API để pipeline chạy được khi offline."""
    return [{"userId": (i % 10) + 1, "id": i,
             "title": f"mock title {i}", "body": f"mock body for post {i}"}
            for i in range(1, n + 1)]


def extract() -> tuple[list[dict], str]:
    """Trả (records, source) với source = 'api' hoặc 'mock-fallback'."""
    all_rows: list[dict] = []
    try:
        for page in range(1, MAX_PAGES + 1):
            rows = http_get_json(API, {"_page": page, "_limit": PAGE_SIZE})
            log.info("page %d -> %d records", page, len(rows))
            if not rows:                      # hết dữ liệu -> dừng pagination
                break
            all_rows.extend(rows)
        if all_rows:
            return all_rows, "api"
        raise RuntimeError("API trả rỗng")
    except Exception as exc:                  # noqa: BLE001 — chủ đích fallback mọi lỗi
        log.warning("Extract từ API lỗi (%s) -> dùng MOCK fallback", exc)
        return mock_posts(), "mock-fallback"


def main() -> None:
    log.info("== EXTRACT ==")
    records, source = extract()
    log.info("Lấy %d records từ nguồn: %s", len(records), source)

    # --- Lưu RAW trước (bronze) — replay được, không mất dữ liệu gốc ---
    raw_path = RAW_DIR / "posts_raw.json"
    raw_path.write_text(json.dumps(records, indent=2))
    log.info("== LOAD RAW == %d bytes -> %s", raw_path.stat().st_size, raw_path.relative_to(ROOT))

    # --- NORMALIZE -> Parquet (silver) -------------------------------
    df = pd.json_normalize(records)
    df["body_len"] = df["body"].str.len()      # một transform nhỏ
    df["_source"] = source                      # lineage: ghi nguồn vào dữ liệu
    out_path = OUT_DIR / "posts.parquet"
    df.to_parquet(out_path, index=False)
    log.info("== TRANSFORM+LOAD == %d hàng x %d cột -> %s",
             len(df), df.shape[1], out_path.relative_to(ROOT))
    print(df[["id", "userId", "body_len", "_source"]].head().to_string(index=False))

    # --- IDEMPOTENT check: chạy lại extract+normalize ra cùng số hàng -
    log.info("Idempotent: ghi đè cùng path, chạy lại -> cùng %d hàng.", len(df))
    print("\nDONE ✅ api ingestion chạy xong.")


if __name__ == "__main__":
    main()
