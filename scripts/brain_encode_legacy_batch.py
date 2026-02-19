#!/usr/bin/env python3
"""[LEGACY BATCH ENCODER]

This script encodes MEMORY.md / today's memory file as coarse-grained embeddings.

- Historical / experimental tool kept for reference.
- Canonical, production encoder is: para-system/brain_encode.py

Use this only if you explicitly want the old batch-style behavior.
"""

import argparse
import json
import os
import sys
from datetime import datetime

import fcntl  # POSIX file lock
import numpy as np
from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEMORY_DIR = os.path.join(BASE_DIR, "memory")
INDEX_PATH = os.path.join(MEMORY_DIR, "index.json")
LOCK_PATH = os.path.join(MEMORY_DIR, "index.lock")
EMBED_DIR = os.path.join(MEMORY_DIR, "embeddings")

SIM_THRESHOLD = 0.75
DENSITY_BOOST = 0.2
IMPORTANCE_BOOST_FACTOR = 0.15  # current += initial * factor
IMPORTANCE_MAX = 2.0

MODEL_NAME = "all-MiniLM-L6-v2"


def load_model():
    # Lazy, singleton-ish load to avoid repeated downloads when reused.
    return SentenceTransformer(MODEL_NAME)


def now_iso() -> str:
    return datetime.utcnow().isoformat()


def ensure_index() -> dict:
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


def acquire_lock():
    os.makedirs(MEMORY_DIR, exist_ok=True)
    fd = os.open(LOCK_PATH, os.O_CREAT | os.O_RDWR)
    fcntl.flock(fd, fcntl.LOCK_EX)
    return fd


def release_lock(fd):
    try:
        fcntl.flock(fd, fcntl.LOCK_UN)
    finally:
        os.close(fd)


def load_embedding(mem_id: int):
    path = os.path.join(EMBED_DIR, f"{mem_id}.npy")
    if not os.path.exists(path):
        return None
    return np.load(path)


def save_embedding(mem_id: int, vec: np.ndarray):
    os.makedirs(EMBED_DIR, exist_ok=True)
    path = os.path.join(EMBED_DIR, f"{mem_id}.npy")
    np.save(path, vec)


def compute_state(current_importance: float) -> str:
    if current_importance >= 0.85:
        return "Golden"
    if current_importance >= 0.50:
        return "Silver"
    if current_importance >= 0.20:
        return "Bronze"
    return "Dust"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Encode a memory into Yue's semantic store.")
    parser.add_argument("content", help="Memory content text")
    parser.add_argument("--actor", default="Self", help="Self|空|剀|玥|User")
    parser.add_argument("--target", default="Core", help="Core|Subagents|Task|Memory")
    parser.add_argument("--domain", default="Role", help="World|Role|User")
    parser.add_argument("--score", type=float, default=0.5, help="Initial importance 0.0-1.0")

    args = parser.parse_args(argv)

    # !REMEMBER shortcut → force Golden-ish importance
    content = args.content.strip()
    initial_importance = max(0.0, min(args.score, 1.0))
    if "!REMEMBER" in content:
        initial_importance = max(initial_importance, 0.9)

    model = load_model()
    new_vec = model.encode(content, convert_to_tensor=True)

    lock_fd = acquire_lock()
    try:
        index = ensure_index()
        memories = index.get("memories", [])

        # Try semantic dedupe / reinforcement
        best_sim = -1.0
        best_mem = None
        best_mem_vec = None

        for mem in memories:
            mem_vec = load_embedding(mem["id"])
            if mem_vec is None:
                continue
            new_vec_np = new_vec.detach().cpu().numpy() if hasattr(new_vec, "detach") else np.array(new_vec)
            dot = np.dot(new_vec_np, mem_vec)
            norm = np.linalg.norm(new_vec_np) * np.linalg.norm(mem_vec)
            sim = float(dot / norm) if norm > 0 else 0.0
            if sim > best_sim:
                best_sim = sim
                best_mem = mem
                best_mem_vec = mem_vec

        if best_sim >= SIM_THRESHOLD and best_mem is not None:
            # Reinforce existing memory
            best_mem["access_count"] = best_mem.get("access_count", 0) + 1
            best_mem["density"] = best_mem.get("density", 0.0) + DENSITY_BOOST
            init_imp = best_mem.get("initial_importance", initial_importance)
            cur_imp = best_mem.get("current_importance", init_imp)
            cur_imp = min(cur_imp + init_imp * IMPORTANCE_BOOST_FACTOR, IMPORTANCE_MAX)
            best_mem["current_importance"] = cur_imp
            best_mem["state"] = compute_state(cur_imp)
            best_mem["last_access"] = now_iso()

            save_index(index)
            # Optionally, we could also blend embeddings; for now, keep original.
            print(f"Reinforced memory id={best_mem['id']} (sim={best_sim:.3f})")
            return 0

        # Otherwise, create new memory
        next_id = 1
        if memories:
            next_id = max(m["id"] for m in memories) + 1
        now = now_iso()

        mem = {
            "id": next_id,
            "content": content,
            "actor": args.actor,
            "target": args.target,
            "domain": args.domain,
            "initial_importance": initial_importance,
            "current_importance": initial_importance,
            "s_factor": 0.995,
            "density": 0.5,
            "access_count": 0,
            "retrieval_count": 0,
            "last_access": now,
            "creation_date": now,
            "state": compute_state(initial_importance),
        }
        memories.append(mem)
        index["memories"] = memories
        save_index(index)

        # Save embedding (convert to numpy)
        new_vec_np = new_vec.detach().cpu().numpy() if hasattr(new_vec, "detach") else new_vec
        save_embedding(next_id, new_vec_np)

        print(f"Created memory id={next_id}")
        return 0
    finally:
        release_lock(lock_fd)


if __name__ == "__main__":
    raise SystemExit(main())
