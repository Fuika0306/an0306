#!/bin/bash
# 每日總結模板生成腳本 + 記憶檔案 Git 同步

WORKSPACE="$HOME/.openclaw/workspace"
MEMORY_DIR="$WORKSPACE/memory"
TODAY=$(date +%Y-%m-%d)
SUMMARY_FILE="$MEMORY_DIR/${TODAY}-summary.md"

if [ -f "$SUMMARY_FILE" ]; then
  echo "⚠️ 今天已有總結：$SUMMARY_FILE"
else
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
fi

# --- 以下：記憶檔案自動 Git 同步 ---

cd "$WORKSPACE" || exit 0

# 只在這個 workspace 是 Git repo 的情況下同步
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  # 加上當天記憶與總結，以及核心記憶
  git add MEMORY.md memory/*.md 2>/dev/null

  # 若沒有任何變更，直接結束
  if git diff --cached --quiet; then
    echo "ℹ️ 無記憶變更需要同步，略過 Git 提交。"
    exit 0
  fi

  MSG="chore: daily memory sync $(date +%F)"
  git commit -m "$MSG" 2>/dev/null || echo "⚠️ Git commit 失敗（可能無變更）。"
  git push origin master 2>/dev/null || echo "⚠️ Git push 失敗，請稍後手動同步。"
else
  echo "ℹ️ $WORKSPACE 不是 Git repository，略過 Git 同步。"
fi
