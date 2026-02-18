# 記憶摘要加載器

> 更新時間：2026-02-18 GMT+8

## 加載策略

- 對話開始：只讀 `MEMORY.md`（Golden，<500 token）
- 需要細節時：按需檢索 `memory/` 目錄下的具體文件
- 永遠不要一次加載所有記憶文件

## 快速索引

| 需要什麼     | 讀取文件                 |
|------------|------------------------|
| 用戶信息     | `USER.md`              |
| 今日日誌     | `memory/YYYY-MM-DD.md` |
| 痛點記錄     | `memory/pain-points.md`|
| 失敗記錄     | `memory/failures.json` |

## 檢索規則

1. 簡單查詢（「今天做了什麼」）→ 讀今日日誌
2. 用戶偏好查詢 → 讀 `MEMORY.md` + `USER.md`
3. 歷史查詢 → 讀 `memory/YYYY-MM-DD.md`
4. 系統問題 → 讀 `memory/pain-points.md`

## 不要做的事

- ❌ 對話開始時讀取所有 `memory/` 文件
- ❌ 一次性加載超過 1000 token 的記憶文件
- ❌ 重複讀取同一個文件（除非內容已更新）
