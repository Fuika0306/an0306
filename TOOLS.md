# TOOLS.md - 環境與工具清單

TOOLS.md 就是這個工作空間的「環境配置清單」。

## 系統環境

- OS：Linux（OpenCloudOS）
- Python：3.10+
- Node.js：v22.22.0
- 時區：GMT+8

## 已裝工具

- **Python**：
  - sentence-transformers
  - numpy
  - torch
- **Node.js**：
  - tweetnacl
- **系統工具**：
  - git
  - cron
  - jq

## 核心腳本 / 任務

- 記憶編碼與檢索
- 每日總結
- 週期性深度分析
- 記憶檢查點（checkpoint）

## 記憶系統結構

- **Golden**：永不衰減的核心記憶
- **Silver**：90 天無引用淘汰的活躍記憶
- **Bronze**：30 天無引用淘汰的臨時快照
- **嵌入向量**：用於語義檢索的向量表示

> 之後如果有新增服務、主機、腳本，就補在這裡，當成玥的環境說明書。