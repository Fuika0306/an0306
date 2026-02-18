#!/usr/bin/env python3
# 記憶檢索 - 用語義相似度從索引中找相關記憶

import json
import sys
from pathlib import Path

try:
    from sentence_transformers import SentenceTransformer
    import numpy as np
except ImportError:
    print("⚠️ 需要安裝：pip install sentence-transformers numpy")
    exit(1)

MEMORY_DIR = Path.home() / ".openclaw/workspace/memory"
EMBEDDINGS_DIR = MEMORY_DIR / "embeddings"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def retrieve(query: str, top_k: int = 3):
    model = SentenceTransformer(MODEL_NAME)
    query_embedding = model.encode(query)

    with open(EMBEDDINGS_DIR / "index.json", "r") as f:
        index = json.load(f)

    scores = []

    for fname, meta in index.items():
        vec_path = EMBEDDINGS_DIR / f"{fname}.vec"
        if not vec_path.exists():
            continue

        with open(vec_path, "r") as f:
            embedding = np.array(json.load(f))

        similarity = float(
            np.dot(query_embedding, embedding)
            / (np.linalg.norm(query_embedding) * np.linalg.norm(embedding) + 1e-8)
        )

        scores.append((fname, similarity, meta["path"]))

    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_k]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python brain_retrieve.py '查詢文本'")
        exit(1)

    query = sys.argv[1]
    results = retrieve(query)

    print(f"🔍 查詢：{query}")
    for fname, score, path in results:
        print(f"  {fname} (相似度: {score:.2f})")
        print(f"   → {path}")
