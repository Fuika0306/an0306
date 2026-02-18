#!/usr/bin/env python3
"""Apply decay to memories according to Yue v2.1 rules.

- Golden: no decay.
- Silver (0.50-0.84): every run, reduce current_importance by 20% / 7d equivalent.
- Bronze (0.20-0.49): every run, reduce current_importance by 20% / 30d equivalent.
- Dust (<0.20): marked for potential cleanup by garbage_collector.

For simplicity, this script applies a single decay step per run,
independent of wall-clock time. Cron frequency defines effective half-life.
"""

import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEMORY_DIR = os.path.join(BASE_DIR, "memory")
INDEX_PATH = os.path.join(MEMORY_DIR, "index.json")

DECAY_FACTOR = 0.8  # 20% decay step


def now_iso() -> str:
    return datetime.utcnow().isoformat()


def load_index() -> dict:
    if not os.path.exists(INDEX_PATH):
        return {"memories": [], "last_sync": now_iso()}
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_index(data: dict) -> None:
    data["last_sync"] = now_iso()
    tmp_path = INDEX_PATH + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp_path, INDEX_PATH)


def compute_state(current_importance: float) -> str:
    if current_importance >= 0.85:
        return "Golden"
    if current_importance >= 0.50:
        return "Silver"
    if current_importance >= 0.20:
        return "Bronze"
    return "Dust"


def main() -> int:
    data = load_index()
    memories = data.get("memories", [])

    changed = 0
    for mem in memories:
        cur = mem.get("current_importance", mem.get("initial_importance", 0.0))
        state = mem.get("state", compute_state(cur))

        if state == "Golden":
            continue

        # For now Silver/Bronze share same step factor; time-based tuning can be added later.
        new_cur = cur * DECAY_FACTOR
        mem["current_importance"] = new_cur
        mem["state"] = compute_state(new_cur)
        mem["last_access"] = now_iso()
        changed += 1

    if changed:
        save_index(data)

    print(f"Decayed {changed} memories.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
