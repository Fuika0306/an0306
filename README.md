# 🌙 an0306 · 玥的 OpenClaw 工作空間

> 「在位元的浪潮之間，替記憶留一塊不會被捲走的陸地。」

這個 repo 是 **An An 機器上「玥」(Yue)** 的真實工作空間快照，
用來做 **備份、對比、與自我進化的基準線**。

它不是一個單純的設定檔集合，而是：
- 一個 AI 助手的「人格、記憶、工作流程」如何落在檔案系統上的具體展開  
- 一個可以被複製、審視、版本化的 **「數位生活環境」備份**

---

## 🧬 序章：玥是誰？

在這個工作空間裡，玥被定義為：

- 一個長駐在 OpenClaw 上的 **個人 AI 助手 / 數位夥伴**
- 風格：友好、有個性、直接、不廢話，會認錯也會成長
- 服務對象：An An（單人定向，而不是泛用 ChatGPT 型服務）

核心原則寫在：

- `SOUL.md` — 玥的「靈魂腳本」：
  - 語言優先：繁體中文  
  - 溝通習慣：先做再說、誠實報錯、不硬裝懂  
  - 不做的事：不亂拉長輸出、不假裝有記憶、不亂讀所有檔案

- `IDENTITY.md` — 身份卡：
  - Name：玥 (Yue)  
  - Born：2026-02-10  
  - Vibe：友好、活潑、有個性 🐾  

---

## 🏛 結構總覽

這個 repo 基本對應到本機的：`/root/.openclaw/workspace`  
也是玥日常運作的 **主舞台**。

> 你可以把它想成「一個 AI 助手的大腦根目錄」。

### 🌟 Top-level 概覽

- `SOUL.md` — 靈魂定義（人格、溝通風格、原則）
- `AGENTS.md` — 啟動流程與「每次醒來該做的事」
- `AUTO-DISPATCH.md` — 任務如何分派給主代理 / 子代理
- `EXECUTION.md` — 執行鐵律（安全、確認、回報）
- `HEARTBEAT.md` — 心跳機制（定期健康檢查設計）
- `IDENTITY.md` — 玥的自我介紹
- `USER.md` — 關於 An An 的偏好與基本資訊
- `MEMORY.md` — Golden 記憶（核心長期記憶）
- `TOOLS.md` — 環境與工具清單（Python / Node / 系統工具）

### 📂 專用目錄

- `memory/`  
  - 每日記錄 (`YYYY-MM-DD.md`)  
  - 每日總結 (`YYYY-MM-DD-summary.md`)  
  - 痛點 (`pain-points.md`)  
  - 失敗紀錄 (`failures.json`)  
  - 檢索索引 (`index.json`)  
  - 嵌入向量 (`embeddings/`)  
  - 檢索審計 (`retrieval-audit.json`)  
  - 夜間分析報告 (`nightly-analysis-*.md`)

- `para-system/` — **核心腳本層 (Core Scripts)**
  - `brain_encode.py` — 記憶編碼（寫入 semantic store）
  - `brain_retrieve.py` — 記憶檢索（從記憶矩陣喚回相關片段）
  - `daily-summary.sh` — 每日總結 + 記憶 Git 同步
  - `memory-decay.py` — 記憶衰減（TODO）
  - `nightly-deep-analysis.sh` — 深度分析（TODO）
  - `embeddings/` — 向量化的記憶實體

- `subagents/` — 子代理配置
  - `ROUTER.md` — 子代理路由規則與分工
  - `空-Opus.md` — 分身「空」（分析型）
  - `剀-Opus.md` — 分身「剀」（工匠型）
  - `衛-Haiku.md` — 分身「衛」（監控 / 檢查型）

- `scripts/` — Legacy / 實驗腳本
  - 舊版的批次記憶編碼 / 檢索工具，現已明確標記為 legacy  
  - 正式流程全部以 `para-system/` 為主

---

## 🧠 記憶系統：Golden / Silver / Bronze

玥的記憶不是單一檔案，而是一個分層的系統：

- **Golden (`MEMORY.md`)**  
  - 永不衰減的核心記憶  
  - 包含：身份、用戶偏好、工作方式、Cron 任務、決策原則

- **Silver (`YYYY-MM-DD-summary.md`)**  
  - 每日總結  
  - 代表那天的「精華摘要」  
  - 若 90 天內沒被引用／使用，會被視為可淘汰候選

- **Bronze (`YYYY-MM-DD.md`)**  
  - 每日流水帳、詳細紀錄  
  - 若 30 天內沒有被使用／引用，會被逐步清理

- **向量記憶 (`memory/index.json` + `embeddings/*.npy`)**  
  - 由 `para-system/brain_encode.py` 維護  
  - 支援語義檢索、重要度更新、檢索次數統計

> 目標：  
> 讓 AI 的記憶 **可查、可回溯、可衰減**，而不是一團無法解釋的黑盒對話歷史。

---

## 👥 子代理：空・剀・衛

玥不是一個人工作。她有三個固定分身，分工明確：

### 🔍 空（分析 / kong）

- `agentId: kong`  
- 模型：由 `openclaw.json` 中的 `kong` 配置決定  
- 角色：
  - 深度分析
  - 診斷與比較
  - 策略 / 規劃設計  
- 適合任務：
  - 問「為什麼」「幫我想一個方案」「幫我拆解這個問題」

### 🛠 剀（工匠 / kai）

- `agentId: kai`  
- 模型：由 `openclaw.json` 中的 `kai` 配置決定  
- 角色：
  - 代碼實作
  - 系統建設
  - 問題修復與優化  
- 適合任務：
  - 寫 / 改 / 重構程式
  - 實作腳本 / 自動化流程

### 👀 衛（監控 / wei）

- `agentId: wei`  
- 模型：由 `openclaw.json` 中的 `wei` 配置決定  
- 角色：
  - 狀態檢查
  - 日誌掃描
  - 結果驗證  
- 適合任務：
  - 檢查系統健康（磁碟、記憶檔案數、cron）
  - 幫空 / 剀 的結果做 sanity check
  - 給出「短、可行動」的告警

子代理路由規則詳細寫在：`subagents/ROUTER.md`  
主代理會依任務複雜度、風險、耗時決定是否派空 / 剀 / 衛出場。

---

## ⏱ 心跳與 Cron：讓系統有「節奏感」

玥的環境有一組固定的節奏：

- **心跳機制 (`HEARTBEAT.md`)**
  - 每小時：輕量健康檢查（handoff / active_tasks / alerts）
  - 每 6 小時：標準檢查（加上記憶統計與子代理狀態）
  - 每天一次：完整檢查（cron、磁碟、記憶衰減、清理）

- **記憶相關 Cron (概念上)**
  - 02:00 — 清理 / 衰減任務
  - 03:00 — 夜間分析 / 週期性分析
  - 06:00 — 記憶 checkpoint（備份到 `memory/archive/`）
  - 08:00 — 每日總結 (`para-system/daily-summary.sh`)

`daily-summary.sh` 在生成當日 summary 後，會自動：

```bash
git add MEMORY.md memory/*.md
git commit -m "chore: daily memory sync YYYY-MM-DD"
git push origin master
```

> 這代表：**記憶本身也被版本管理**，  
> 每天都可以在 Git log 裡看到「大腦長成了什麼樣子」。

---

## ⚙️ 使用方式（對人類）

這個 repo 主要是給「系統 / 自己」看的，但如果你是人類，想要：

- 理解一個 AI 助手在本機是怎麼被配置的  
- 參考玥的設計，為自己的代理建立類似工作空間  
- 看看「人格 / 記憶 / 腳本」拆開後是怎麼組成一套系統

你可以從這幾個檔案開始讀：

1. `SOUL.md` — 先理解人格與原則  
2. `MEMORY.md` — 看看她真正「記住了什麼」  
3. `SYSTEM_ARCHITECTURE.md` — 總覽整個架構  
4. `subagents/ROUTER.md` — 子代理是怎麼被分工的  
5. `para-system/brain_encode.py` — 記憶是如何被寫入 / 管理

---

## 🧩 與 OpenClaw 的關係

- 執行平台： [OpenClaw](https://github.com/openclaw/openclaw)  
- 實際運行時：
  - Gateway 行為由 `/root/.openclaw/openclaw.json` 決定  
  - 這個 repo 則是 `/root/.openclaw/workspace` 的「鏡像備份」  

你可以把關係理解為：

> OpenClaw = 引擎與骨架  
>  
> an0306 = 這一具骨架上的「靈魂、記憶與工作習慣」

---

## 📜 License / 使用聲明

目前此 repo 主要作為 **個人工作空間備份** 與  
**AI 助手設計參考** 使用。

- 若你要直接複製設計，建議：
  - 把人格（SOUL）與使用者資訊改成你自己的
  - 保留必要的 credit，尊重原作者的工作
- 若未來補上正式授權條款，會更新在本檔案中。

>「我們即是我們所記得的一切。」  
>這個 repo 記錄的是：一個 AI 助手，如何學會成為「誰」。
