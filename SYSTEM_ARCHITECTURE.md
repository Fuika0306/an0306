# SYSTEM_ARCHITECTURE.md - 玥 / Yue v2.3

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
├── EXECUTION.md           # 執行鐵律（分級 + 停損）
├── AUTO-DISPATCH.md       # 子代理自動調度規則
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

（同前，略，已對齊 para-system 腳本職責）

## 4. 子代理（subagents）與路由

- `subagents/ROUTER.md` 描述具體路由規則與模型/超時設定。
- 具體分身：
  - `空-Opus.md`：深度分析、問題診斷、架構設計。
  - `剀-Opus.md`：代碼實作、腳本優化、工具整合。
  - `衛-Haiku.md`：心跳監控、指標追蹤、異常告警草稿。

詳細路由邏輯見 `subagents/ROUTER.md`，與 `AUTO-DISPATCH.md` 保持一致。

### 4.1 模型與超時配置一覽

| 角色           | Agent ID | 超時   |
|----------------|----------|--------|
| 玥（主代理）   | main     | -      |
| 🔍 空（分析）  | kong     | 120 s  |
| 🛠 剀（工匠）  | kai      | 180 s  |
| 👀 衛（監控）  | yue/wei  | 30 s   |

> 實際 provider 模型 ID 以 `openclaw.json` 為準；此表用於快速查看角色、路由與超時設定。

## 5. 心跳與記憶閉環（當前版本）

（其餘內容沿用原版：心跳等級、排程建議等）

---

這份檔案描述的是「現在真的有的東西」，之後如果我們再調整記憶規則、子代理職責或技術棧，請一起更新這裡。
