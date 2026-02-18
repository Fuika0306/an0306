#!/usr/bin/env python3
"""Retrieve memories from memory/index.json using semantic similarity.

- Uses all-MiniLM-L6-v2 via sentence-transformers.
- Loads embeddings from memory/embeddings/{id}.npy.
- Increments retrieval_count for memories that are returned.
- Respects the same fcntl lock as brain_encode.py for safe updates.
"""

import argparse
import json
import os
from datetime import datetime

import fcntl
import numpy as np
from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEMORY_DIR = os.path.join(BASE_DIR, "memory")
INDEX_PATH = os.path.join(MEMORY_DIR, "index.json")
LOCK_PATH = os.path.join(MEMORY_DIR, "index.lock")
EMBED_DIR = os.path.join(MEMORY_DIR, "embeddings")

MODEL_NAME = "all-MiniLM-L6-v2"


def now_iso() -> str:
    return datetime.utcnow().isoformat()


def load_model():
    return SentenceTransformer(MODEL_NAME)


def acquire_lock():
    fd = os.open(LOCK_PATH, os.O_CREAT | os.O_RDWR)
    fcntl.flock(fd, fcntl.LOCK_EX)
    return fd


def release_lock(fd):
    try:
        fcntl.flock(fd, fcntl.LOCK_UN)
    finally:
        os.close(fd)


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


def load_embedding(mem_id: int):
    path = os.path.join(EMBED_DIR, f"{mem_id}.npy")
    if not os.path.exists(path):
        return None
    return np.load(path)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Retrieve semantic memories.")
    parser.add_argument("query", help="Query text")
    parser.add_argument("--top-k", type=int, default=5, help="Number of memories to return")
    parser.add_argument("--threshold", type=float, default=0.5, help="Minimum cosine similarity")

    args = parser.parse_args(argv)

    model = load_model()
    q_vec = model.encode(args.query, convert_to_tensor=True)

    lock_fd = acquire_lock()
    try:
        index = load_index()
        memories = index.get("memories", [])

        scored = []
        for mem in memories:
            emb = load_embedding(mem["id"])
            if emb is None:
                continue
            q_vec_np = q_vec.detach().cpu().numpy() if hasattr(q_vec, "detach") else np.array(q_vec)
            dot = np.dot(q_vec_np, emb)
            norm = np.linalg.norm(q_vec_np) * np.linalg.norm(emb)
            sim = float(dot / norm) if norm > 0 else 0.0
            if sim >= args.threshold:
                scored.append((sim, mem))

        scored.sort(key=lambda x: x[0], reverse=True)
        top = scored[: args.top_k]

        # Update retrieval_count & last_access
        for sim, mem in top:
            mem["retrieval_count"] = mem.get("retrieval_count", 0) + 1
            mem["last_access"] = now_iso()

        if top:
            save_index(index)

        # Pretty-print result
        for sim, mem in top:
            print("-" * 60)
            print(f"id: {mem['id']} | sim: {sim:.3f} | state: {mem.get('state', 'Unknown')}")
            print(f"actor={mem.get('actor')} target={mem.get('target')} domain={mem.get('domain')}")
            print(f"importance={mem.get('current_importance'):.3f} density={mem.get('density'):.3f}")
            print(mem["content"])

        if not top:
            print("No memories above threshold.")

        return 0
    finally:
        release_lock(lock_fd)


if __name__ == "__main__":
    raise SystemExit(main())
