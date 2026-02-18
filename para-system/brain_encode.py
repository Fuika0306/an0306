#!/usr/bin/env python3
import os
import json
from datetime import datetime, timezone

from sentence_transformers import SentenceTransformer

WORKSPACE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MEMORY_FILE = os.path.join(WORKSPACE, "MEMORY.md")
MEMORY_DIR = os.path.join(WORKSPACE, "memory")
EMBED_DIR = os.path.join(WORKSPACE, "para-system", "embeddings")
INDEX_FILE = os.path.join(EMBED_DIR, "index.json")

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def load_text(path: str) -> str:
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def ensure_dirs():
    os.makedirs(EMBED_DIR, exist_ok=True)


def encode_texts(model, items):
    texts = [it["text"] for it in items]
    embeddings = model.encode(texts, show_progress_bar=False, normalize_embeddings=True)
    # convert to plain python lists to avoid numpy dependency
    return [emb.tolist() for emb in embeddings]


def main():
    ensure_dirs()

    today = datetime.now().date().isoformat()
    today_file = os.path.join(MEMORY_DIR, f"{today}.md")

    items = []

    # MEMORY.md
    mem_text = load_text(MEMORY_FILE)
    if mem_text.strip():
        items.append({
            "id": "MEMORY.md",
            "path": MEMORY_FILE,
            "text": mem_text,
        })

    # today's memory file (if exists)
    today_text = load_text(today_file)
    if today_text.strip():
        items.append({
            "id": f"{today}.md",
            "path": today_file,
            "text": today_text,
        })

    if not items:
        print("No memory files to encode.")
        return

    print(f"Encoding {len(items)} items with {MODEL_NAME} ...")
    model = SentenceTransformer(MODEL_NAME)
    vectors = encode_texts(model, items)

    index_entries = []
    for item, vec in zip(items, vectors):
        basename = os.path.basename(item["id"])
        vec_path = os.path.join(EMBED_DIR, basename + ".vec.json")
        with open(vec_path, "w", encoding="utf-8") as vf:
            json.dump({"vector": vec}, vf)

        stat = os.stat(item["path"])
        index_entries.append({
            "id": item["id"],
            "source_path": item["path"],
            "vector_path": vec_path,
            "size": stat.st_size,
            "encoded_at": datetime.now(timezone.utc).isoformat(),
        })

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump({"items": index_entries}, f, ensure_ascii=False, indent=2)

    print(f"Wrote {len(index_entries)} embeddings to {EMBED_DIR}")


if __name__ == "__main__":
    main()
