#!/usr/bin/env python3
"""Garbage-collect Dust memories and their embeddings.

Usage:
  python3 scripts/garbage_collector.py --age 7          # dry-run
  python3 scripts/garbage_collector.py --age 7 --execute  # actually delete

- Only considers memories with state == "Dust".
- age (days) is compared to last_access.
- Always preserves at least 10 memories overall for safety.
"""

import argparse
import json
import os
from datetime import datetime, timedelta

import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEMORY_DIR = os.path.join(BASE_DIR, "memory")
INDEX_PATH = os.path.join(MEMORY_DIR, "index.json")
EMBED_DIR = os.path.join(MEMORY_DIR, "embeddings")
ARCHIVE_DIR = os.path.join(MEMORY_DIR, "archive")


def now() -> datetime:
    return datetime.utcnow()


def parse_iso(ts: str) -> datetime:
    try:
        return datetime.fromisoformat(ts)
    except Exception:
        return now()


def load_index() -> dict:
    if not os.path.exists(INDEX_PATH):
        return {"memories": [], "last_sync": now().isoformat()}
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_index(data: dict) -> None:
    data["last_sync"] = now().isoformat()
    tmp_path = INDEX_PATH + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp_path, INDEX_PATH)


def archive_memory(mem: dict):
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    day = mem.get("creation_date", now().isoformat())[:10]
    path = os.path.join(ARCHIVE_DIR, f"{day}.jsonl")
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(mem, ensure_ascii=False) + "\n")


def delete_embedding(mem_id: int):
    path = os.path.join(EMBED_DIR, f"{mem_id}.npy")
    if os.path.exists(path):
        os.remove(path)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Garbage collect Dust memories.")
    parser.add_argument("--age", type=int, required=True, help="Minimum age in days (last_access) to delete")
    parser.add_argument("--execute", action="store_true", help="Actually delete instead of dry-run")

    args = parser.parse_args(argv)

    data = load_index()
    memories = data.get("memories", [])

    now_dt = now()
    cutoff = now_dt - timedelta(days=args.age)

    dust_candidates = []
    for mem in memories:
        if mem.get("state") != "Dust":
            continue
        last_access = parse_iso(mem.get("last_access", mem.get("creation_date", now_dt.isoformat())))
        if last_access <= cutoff:
            dust_candidates.append(mem)

    total = len(memories)
    # Safety: keep at least 10 memories
    max_delete = max(0, total - 10)
    to_delete = dust_candidates[:max_delete]

    print(f"Found {len(dust_candidates)} Dust memories older than {args.age} days.")
    print(f"Total memories: {total}, will delete at most {max_delete} (safety floor=10).")

    if not args.execute:
        for mem in to_delete:
            print(f"[DRY-RUN] would delete id={mem['id']} state={mem.get('state')} content={mem['content'][:50]!r}")
        return 0

    # Execute deletion
    remaining = []
    deleted = 0
    for mem in memories:
        if mem in to_delete:
            archive_memory(mem)
            delete_embedding(mem["id"])
            deleted += 1
        else:
            remaining.append(mem)

    data["memories"] = remaining
    save_index(data)

    print(f"Deleted {deleted} memories (archived before removal).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
