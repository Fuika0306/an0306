#!/usr/bin/env python3
import os
import json
import sys
from typing import List, Dict

from sentence_transformers import SentenceTransformer

WORKSPACE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EMBED_DIR = os.path.join(WORKSPACE, "para-system", "embeddings")
INDEX_FILE = os.path.join(EMBED_DIR, "index.json")

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K = 3


def load_index() -> Dict:
    if not os.path.exists(INDEX_FILE):
        raise FileNotFoundError(f"index.json not found at {INDEX_FILE}. Run brain_encode.py first.")
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def load_vectors(index: Dict):
    vectors = []
    for item in index.get("items", []):
        with open(item["vector_path"], "r", encoding="utf-8") as vf:
            data = json.load(vf)
            vectors.append(data["vector"])
    if not vectors:
        raise RuntimeError("No vectors loaded from embeddings directory.")
    return vectors


def dot(a, b) -> float:
    return sum(x * y for x, y in zip(a, b))


def cosine_similarity(query_vec, vectors):
    # embeddings are already normalized, so cosine = dot
    return [dot(query_vec, v) for v in vectors]


def retrieve(query: str, top_k: int = TOP_K) -> List[Dict]:
    index = load_index()
    items = index.get("items", [])
    if not items:
        raise RuntimeError("Index contains no items.")

    model = SentenceTransformer(MODEL_NAME)
    q_vec = model.encode([query], show_progress_bar=False, normalize_embeddings=True)[0].tolist()
    vecs = load_vectors(index)

    scores = cosine_similarity(q_vec, vecs)

    ranked = sorted(zip(items, scores), key=lambda x: x[1], reverse=True)
    results = []
    for item, score in ranked[:top_k]:
        # load a short preview
        try:
            with open(item["source_path"], "r", encoding="utf-8") as f:
                text = f.read(400)
        except FileNotFoundError:
            text = "[source file missing]"

        results.append({
            "id": item["id"],
            "score": float(score),
            "source_path": item["source_path"],
            "preview": text,
        })

    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: brain_retrieve.py <query>")
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    results = retrieve(query, top_k=TOP_K)

    print(json.dumps({"query": query, "results": results}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
