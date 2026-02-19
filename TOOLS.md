# TOOLS.md - 環境與工具清單

## 系統環境

- OS：Linux（OpenCloudOS）
- Python：3.10+
- Node.js：v22.22.0
- 時區：GMT+8

## 已裝工具

- Python：sentence-transformers、numpy、torch
- Node.js：tweetnacl
- 系統：git、cron、jq

## 核心腳本位置

- 記憶編碼：para-system/brain_encode.py
- 記憶檢索：para-system/brain_retrieve.py
- 每日總結：para-system/daily-summary.sh
- 檢查點：para-system/checkpoint-memory-llm.sh
- 記憶衰減（TODO）：para-system/memory-decay.py
- 深度分析（TODO）：para-system/nightly-deep-analysis.sh

## 記憶系統

- Golden（MEMORY.md）：永不衰減
- Silver（YYYY-MM-DD-summary.md）：90 天無引用淘汰
- Bronze（YYYY-MM-DD.md）：30 天無引用淘汰
- 嵌入向量（memory/embeddings/）：語義檢索用

> 之後如果有新增服務、主機、腳本，就補在這裡，當成玥的環境說明書。