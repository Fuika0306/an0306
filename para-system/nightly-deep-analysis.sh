#!/bin/bash

WORKSPACE="$HOME/.openclaw/workspace"
MEMORY_DIR="$WORKSPACE/memory"
ANALYSIS_FILE="$MEMORY_DIR/nightly-analysis-$(date +%Y-%m-%d).md"

echo "🌙 開始夜間深度分析..."

GOLDEN_COUNT=$(find "$MEMORY_DIR" -name "MEMORY.md" | wc -l)
SILVER_COUNT=$(find "$MEMORY_DIR" -name "*summary*.md" | wc -l)
BRONZE_COUNT=$(find "$MEMORY_DIR" -name "20*.md" | wc -l)
DISK_USAGE=$(du -sh "$MEMORY_DIR" | cut -f1)
LAST_MODIFIED=$(ls -lt "$MEMORY_DIR"/*.md 2>/dev/null | head -1 | awk '{print $6, $7, $8}')

cat > "$ANALYSIS_FILE" << EOF
# 夜間深度分析 — $(date +%Y-%m-%d)

## 記憶系統狀態
- Golden 記憶：$GOLDEN_COUNT 個
- Silver 記憶：$SILVER_COUNT 個
- Bronze 記憶：$BRONZE_COUNT 個
- 磁盤使用：$DISK_USAGE

## 最近活動
- 最後修改：$LAST_MODIFIED

## 衰減檢查
$(python3 "$WORKSPACE/para-system/memory-decay.py" 2>/dev/null || echo "衰減檢查跳過")

## 建議
- 定期備份記憶文件
- 檢查磁盤空間
- 清理過期的 Bronze 記憶

---
**分析時間：** $(date '+%Y-%m-%d %H:%M:%S')
EOF

echo "✅ 分析完成：$ANALYSIS_FILE"
