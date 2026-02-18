#!/bin/bash
# 每日總結模板生成腳本

WORKSPACE="$HOME/.openclaw/workspace"
MEMORY_DIR="$WORKSPACE/memory"
TODAY=$(date +%Y-%m-%d)
SUMMARY_FILE="$MEMORY_DIR/${TODAY}-summary.md"

if [ -f "$SUMMARY_FILE" ]; then
  echo "⚠️ 今天已有總結：$SUMMARY_FILE"
  exit 0
fi

cat > "$SUMMARY_FILE" << EOF
# 每日總結 — $TODAY
> 生成時間：$(date '+%Y-%m-%d %H:%M:%S')

## 今日活動
- [ ] 活動 1
- [ ] 活動 2

## 決策記錄
- 決策 1：原因
- 決策 2：原因

## 學習收穫
- 學到 1
- 學到 2

## 明日計劃
- [ ] 計劃 1
- [ ] 計劃 2

---
**狀態：** 待填充
EOF

echo "✅ 總結文件已生成：$SUMMARY_FILE"
