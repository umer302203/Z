#!/usr/bin/env bash
# push_backup.sh — Push ENTIRE project as snapshot under agi-charon-video/ in remote repo.
# Preserves remote repo's other content (other AI folders). Token lives in .git/config only.
# Usage: bash scripts/push_backup.sh [commit-message]
set -e
BASE="/home/z/my-project"
cd "$BASE"
PREFIX="agi-charon-video"
MSG="${1:-backup: project snapshot $(date '+%Y-%m-%d %H:%M')}"

git fetch origin main
LOCAL=$(git rev-parse HEAD)

# Worktree must be clean enough; stash untracked noise is left alone (ignored files stay)
git checkout -q -B backup-tmp origin/main

# Remove old snapshot folder if present, then overlay my full tree under PREFIX
git rm -rq --ignore-unmatch "$PREFIX" 2>/dev/null || true
git read-tree --prefix="$PREFIX/" -u "$LOCAL"
git commit -qm "$MSG (local $LOCAL)"

# Return to local mainline worktree state
git checkout -q main 2>/dev/null || git checkout -q -
git push -q origin backup-tmp:main
git branch -qD backup-tmp
echo "[backup] pushed snapshot under $PREFIX/ -> origin/main"
git log --oneline -1 origin/main
