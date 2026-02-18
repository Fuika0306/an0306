#!/usr/bin/env python3
# 記憶衰減檢查腳本

import os
from datetime import datetime

MEMORY_DIR = os.path.expanduser("~/.openclaw/workspace/memory")

SILVER_DECAY_DAYS = 90  # summary 類（Silver）
BRONZE_DECAY_DAYS = 30  # daily 類（Bronze）


def check_decay() -> None:
    now = datetime.now()
    for fname in os.listdir(MEMORY_DIR):
        if not fname.endswith(".md"):
            continue

        fpath = os.path.join(MEMORY_DIR, fname)
        mtime = datetime.fromtimestamp(os.path.getmtime(fpath))
        age_days = (now - mtime).days

        if "summary" in fname and age_days > SILVER_DECAY_DAYS:
            print(f"⚠️ Silver 衰減：{fname} ({age_days} 天)")
        if "daily" in fname and age_days > BRONZE_DECAY_DAYS:
            print(f"⚠️ Bronze 衰減：{fname} ({age_days} 天)")


if __name__ == "__main__":
    check_decay()
