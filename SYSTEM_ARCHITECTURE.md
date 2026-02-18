# SYSTEM_ARCHITECTURE.md - 玥 / Yue v2.2

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
│   ├── YYYY-MM-DD.md          # Bronze 每日日誌
│   ├── YYYY-MM-DD-summary.md  # Silver 每日總結
│   ├── handoff.md             # 當前狀態快照
│   ├── failures.json          # 失敗索引
│   ├── pain-points.md         # 觀察到的痛點
│   ├── retrieval-audit.json   # 檢索行為統計
│   ├── embeddings/            # 向量快取（可選）
│   └── archive/               # 歸檔記憶
├── para-system/
│   ├── brain_encode.py        # 記憶語義編碼
│   ├── brain_retrieve.py      # 記憶檢索
│   ├── memory-decay.py        # 記憶衰減檢查
│   ├── daily-summary.sh       # 每日總結生成
│   ├── nightly-deep-analysis.sh # 夜間深度分析
│   └── checkpoint-memory-llm.sh #（預留）用 LLM 做記憶檢查點
├── scripts/
│   ├── brain_encode.py        # 舊版 / 實驗用腳本（逐步淘汰）
│   ├── brain_retrieve.py
│   ├── decay_v2.py
│   ├── garbage_collector.py
│   └── README.md              # 說明 scripts/ 為實驗/備份用
├── subagents/
│   ├── ROUTER.md              # 子代理路由配置
│   ├── 空-Opus.md             # 🔍 空（分析）— 規劃與深度思考
│   ├── 剀-Opus.md             # 🛠️ 剀（工匠）— 實作與優化
│   └── 衛-Haiku.md            # 👀 衛（監控）— 監控與告警
└── ...
```

## 2. 記憶模型（簡化版：Golden / Silver / Bronze）

統一使用簡單模型，對齊 `MEMORY.md` 與 `HEARTBEAT.md`：

- **Golden**：
  - 長期核心記憶，寫在 `MEMORY.md`。
  - 永不衰減，僅透過人工/重大事件更新。

- **Silver**：
  - 每日/區段的總結，文件型態為 `YYYY-MM-DD-summary.md`。
  - 保留期：**90 天** 無引用 → 可淘汰或歸檔。

- **Bronze**：
  - 每日日誌，文件型態為 `YYYY-MM-DD.md`。
  - 保留期：**30 天** 無引用 → 可淘汰或歸檔。

- **embeddings/**：
  - 對 `memory/*.md` 做語義編碼後的向量快取，用於檢索。
  - 可隨時重建（`para-system/brain_encode.py`），不視為權威來源。

- **archive/**：
  - 歷史歸檔，放入不再日常使用但偶爾可能查詢的舊記錄。

衰減規則（由腳本落地）：

- Golden：永不衰減。
- Silver：90 天無引用（或無修改） → `memory-decay.py` 報警，可歸檔或刪除。
- Bronze：30 天無引用（或無修改） → `memory-decay.py` 報警，可歸檔或刪除。

## 3. 核心腳本職責（para-system/）

### 3.1 `para-system/brain_encode.py` — 記憶語義編碼

- 對 `memory/*.md` 做語義編碼，寫入 `memory/embeddings/*.vec`。
- 建立 `memory/embeddings/index.json`：
  - 紀錄檔案路徑、長度、最後編碼時間等 meta。
- 可透過 cron/手動定期重建，作為語義檢索的基礎。

### 3.2 `para-system/brain_retrieve.py` — 記憶檢索

- 輸入 query 字串，計算與 `embeddings` 中各檔案的 cosine 相似度。
- 回傳/列印最相關的數筆記憶（預設 top 3）。
- 用途：
  - 在回答問題前，先找相關日誌/總結作輔助。

### 3.3 `para-system/memory-decay.py` — 記憶衰減檢查

- 掃描 `memory/` 下的 `.md` 文件：
  - 檢查檔案最後修改時間與命名（`summary` / `daily` 等）。
  - 超過 Silver/Bronze 的保留期限時，在輸出中給出警示。
- 真正的「刪除/歸檔」由人或額外腳本決定，不自動動手。

### 3.4 `para-system/daily-summary.sh` — 每日總結生成

- 每日建立一份 `YYYY-MM-DD-summary.md` 模板，包含：
  - 今日活動
  - 決策記錄
  - 學習收穫
  - 明日計劃
- 若該日已存在 summary 檔案，則不覆蓋。

### 3.5 `para-system/nightly-deep-analysis.sh` — 夜間深度分析

- 統計：
  - Golden / Silver / Bronze 數量
  - 記憶目錄磁盤使用
  - 最近修改時間
- 執行 `memory-decay.py`，將衰減檢查輸出嵌入報告。
- 產出 `memory/nightly-analysis-YYYY-MM-DD.md` 報告，作為週期性健康檢查。

### 3.6 `para-system/checkpoint-memory-llm.sh`（預留）

- 未來可用來：
  - 呼叫 LLM 對當前記憶狀態做高層總結。
  - 產出新的 Golden 片段候選，再由人審核寫入 `MEMORY.md`。

## 4. 子代理（subagents）與路由

- `subagents/ROUTER.md` 描述具體路由規則與模型/超時設定。
- 具體分身：
  - `空-Opus.md`：深度分析、問題診斷、架構設計。
  - `剀-Opus.md`：代碼實作、腳本優化、工具整合。
  - `衛-Haiku.md`：心跳監控、指標追蹤、異常告警草稿。

詳細路由邏輯見 `subagents/ROUTER.md`，與 `AUTO-DISPATCH.md` 保持一致。

### 4.1 模型與超時配置一覽

| 角色           | Agent / 模型說明           | 超時   |
|----------------|----------------------------|--------|
| 玥（主代理）   | `openai-codex/gpt-5.1`     | -      |
| 🔍 空（分析）  | 見 `subagents/ROUTER.md`   | 120 s  |
| 🛠 剀（工匠）  | 見 `subagents/ROUTER.md`   | 180 s  |
| 👀 衛（監控）  | 見 `subagents/ROUTER.md`   | 30 s   |

> 真正的 provider 模型 ID 以 OpenClaw 配置檔為準；此表主要用於快速查看角色與超時設定。

## 5. 心跳與記憶閉環（當前版本）

- 心跳依 `HEARTBEAT.md`：
  - 輕量級：
    - 讀 `memory/handoff.md`
    - 檢查進行中任務（active_tasks）
    - 檢查 P0 警報（critical_alerts）
  - 標準級：
    - 包含輕量級所有項目
    - 加上記憶統計（Golden / Silver / Bronze 數量）
    - 子代理狀態（只看有無新消息 / 異常）
  - 完整級：
    - 包含標準級所有項目
    - 全系統檢查（cron 任務、記憶衰減、磁碟使用）
    - 可呼叫 `memory-decay.py` 並檢查是否需要清理或歸檔。

- 建議排程（部分已透過 OpenClaw cron 實作）：
  - 每日 02:00：清理 & 衰減檢查
  - 每日 03:30：`nightly-deep-analysis.sh`（深度分析報告）
  - 每日 06:00：記憶檢查點備份
  - 每日 08:00：每日總結
  - 每週：深度分析與系統優化建議

---

這份檔案描述的是「現在真的有的東西」，之後如果我們再調整記憶規則、子代理職責或技術棧，請一起更新這裡。
