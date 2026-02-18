#!/usr/bin/env python3
# 語義編碼 - 將 memory/*.md 轉成向量並建立索引

import json
from pathlib import Path

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    print("⚠️ 需要安裝：pip install sentence-transformers")
    exit(1)

MEMORY_DIR = Path.home() / ".openclaw/workspace/memory"
EMBEDDINGS_DIR = MEMORY_DIR / "embeddings"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def encode_memory() -> None:
    EMBEDDINGS_DIR.mkdir(exist_ok=True)
    model = SentenceTransformer(MODEL_NAME)
    index = {}

    for fpath in MEMORY_DIR.glob("*.md"):
        if fpath.name.startswith("."):
            continue

        with open(fpath, "r", encoding="utf-8") as f:
            text = f.read()

        # 限制長度避免太大的輸入
        embedding = model.encode(text[:1000])
        vec_path = EMBEDDINGS_DIR / f"{fpath.name}.vec"

        with open(vec_path, "w") as f:
            json.dump(embedding.tolist(), f)

        index[fpath.name] = {
            "path": str(fpath),
            "size": len(text),
            "encoded_at": str(Path(fpath).stat().st_mtime),
        }

    with open(EMBEDDINGS_DIR / "index.json", "w") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    print(f"✅ 編碼完成：{len(index)} 個文件")


if __name__ == "__main__":
    encode_memory()
