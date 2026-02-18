# SYSTEM_ARCHITECTURE.md - 玥 / Yue v2.1

> 真正跑在這台機器上的版本，以這個 workspace 為準。

## 1. 檔案與目錄結構

```text
./
├── MEMORY.md              # Golden 核心記憶
├── SOUL.md                # 靈魂 / 行為準則
├── USER.md                # 使用者資訊
├── AGENTS.md              # 工作空間說明與規則
├── IDENTITY.md            # 玥的自我定義
├── HEARTBEAT.md           # 心跳級別與檢查規則
├── SYSTEM_ARCHITECTURE.md # 本檔案
├── memory/
│   ├── YYYY-MM-DD.md      # 每日日誌（P1 / Silver 來源）
│   ├── failure-reports/   # 失敗與異常記錄
│   ├── failures.json      # 失敗索引
│   ├── index.json         # 神髓記憶索引（語義記憶）
│   ├── index.lock         # fcntl 鎖定用檔案
│   ├── pain-points.md     # 觀察到的痛點
│   ├── retrieval-audit.json # 檢索行為統計
│   ├── embeddings/        # 向量檔案 {id}.npy
│   └── archive/           # Dust 記憶歸檔 jsonl
├── scripts/
│   ├── brain_encode.py    # 新記憶編碼 + 語義查重 + 強化
│   ├── brain_retrieve.py  # 語義檢索 + retrieval_count
│   ├── decay_v2.py        # 重要性衰減 / 狀態更新
│   └── garbage_collector.py # Dust 垃圾回收 + 向量清理
├── subagents/
│   ├── 空-Opus.md         # 🔍 空（分析）— 規劃與深度思考
│   ├── 剀-Opus.md         # 🛠️ 剀（工匠）— 實作與優化
│   └── 衛-Haiku.md        # 👀 衛（監控）— 監控與告警
└── ...
```

## 2. 記憶模型（index.json）

`memory/index.json` 使用如下結構儲存語義記憶：

```jsonc
{
  "memories": [
    {
      "id": 1,
      "content": "記憶內容",
      "actor": "Self|空|剀|玥|User",
      "target": "Core|Subagents|Task|Memory",
      "domain": "World|Role|User",
      "initial_importance": 0.5,
      "current_importance": 0.5,
      "s_factor": 0.995,
      "density": 0.5,
      "access_count": 0,
      "retrieval_count": 0,
      "last_access": "ISO-8601",
      "creation_date": "ISO-8601",
      "state": "Golden|Silver|Bronze|Dust"
    }
  ],
  "last_sync": "ISO-8601"
}
```

狀態切分：

- `Golden`  : `current_importance >= 0.85`（核心原則、不衰減）
- `Silver`  : `0.50 ≤ current_importance < 0.85`
- `Bronze`  : `0.20 ≤ current_importance < 0.50`
- `Dust`    : `< 0.20`，等待垃圾回收

所有語義向量存於 `memory/embeddings/{id}.npy`。

## 3. 核心腳本職責

### 3.1 `scripts/brain_encode.py`

- 輸入一段文字（必填）與 meta（actor / target / domain / score）。
- 使用 `all-MiniLM-L6-v2` 產生向量。
- 讀取 `memory/index.json` + embeddings：
  - 若與既有記憶 cosine 相似度 `≥ 0.75` → 強化：
    - `access_count += 1`
    - `density += 0.2`
    - `current_importance += initial_importance × 0.15`（上限 2.0）
    - 更新 `state` 與 `last_access`
  - 否則：
    - 新增一筆記憶（自動遞增 `id`）
    - 寫入 embedding 檔案 `{id}.npy`
- 使用 `memory/index.lock` + `fcntl.flock` 實現排他鎖。
- 若文字中包含 `!REMEMBER`，會將 `initial_importance` 強制提升至至少 `0.9`。

### 3.2 `scripts/brain_retrieve.py`

- 根據 query 產生向量，與全部 embeddings 計算 cosine 相似度。
- 參數：
  - `--top-k`：回傳筆數（預設 5）
  - `--threshold`：最低相似度（預設 0.5）
- 對於入選的記憶：
  - `retrieval_count += 1`
  - 更新 `last_access`
- 在終端印出人類可讀格式（id / sim / state / content）。

### 3.3 `scripts/decay_v2.py`

- 對非 Golden 記憶套用一次性衰減：
  - `current_importance *= 0.8`（20% 減少）
  - 重新計算 `state`
  - 更新 `last_access`
- 實際半衰期由 cron 執行頻率決定（例如每天 1 次 ≈ README 中的 7/30 天節奏）。

### 3.4 `scripts/garbage_collector.py`

- 只處理 `state == "Dust"` 的記憶。
- 使用 `--age N` 判斷 `last_access` 是否早於 N 天之前。
- 安全機制：總記憶量至少保留 10 筆，不會一次清空。
- 流程：
  1. 找出 Dust 且超過 `age` 的候選。
  2. 將要刪除的記憶先寫入 `memory/archive/YYYY-MM-DD.jsonl`。
  3. 刪除對應的 `{id}.npy` 向量檔。
  4. 從 `index.json` 中移除。
- 預設為 dry-run；只有加上 `--execute` 才真正刪除。

## 4. 子代理（subagents）

> 檔案先佔位，具體工作流可隨使用習慣再細化。

- `subagents/空-Opus.md`：
  - 深度分析、問題診斷、架構設計。
  - 適合長文本分析、模式辨識、決策建議。
- `subagents/剀-Opus.md`：
  - 代碼實作、腳本優化、工具整合。
  - 負責把想法變成可執行的東西。
- `subagents/衛-Haiku.md`：
  - 心跳監控、指標追蹤、異常告警草稿。
  - 適合搭配 cron 任務，用於 watch dog 類工作。

## 5. 心跳與記憶閉環（當前版本）

- 心跳依 `HEARTBEAT.md`：
  - 輕量級：檢查 handoff / active_tasks / critical_alerts。
  - 標準/完整級：未來可在這基礎上掛載 `decay_v2.py` 與 `garbage_collector.py`。
- 建議後續：
  - 每日凌晨跑一次 `decay_v2.py`（通過 OpenClaw cron）。
  - 每週或每兩週跑一次 `garbage_collector.py --age 7`，先 dry-run 看結果再決定是否 `--execute`。

---

這份檔案描述的是「現在真的有的東西」，之後如果我們再調整記憶規則、子代理職責或技術棧，請一起更新這裡。