#!/usr/bin/env bash
# ============================================================================
# publish.sh — zemnanet blog post publisher
#
# Usage:
#   ./publish.sh "Title of the post" "news" "korea,devtools"
#   ./publish.sh "Title"                    # interactive
#   ./publish.sh --draft "Title"            # save as draft
#
# What it does:
#   1. Creates content/posts/<slug>.md from title + category + tags
#   2. Inserts the design system voice template (frontmatter + body skeleton)
#   3. Triggers Hugo dev preview URL (if --preview flag)
#   4. Optionally commits and pushes (if --git flag)
#
# Voice/structure comes from ~/.claude/skills/marketing-team/x-longform-post
# ============================================================================
set -euo pipefail

ROOT="$(cd "$(dirname "$(realpath "$0")")/.." && pwd)"
cd "$ROOT"

# --- args ---
DRAFT=false
PREVIEW=false
GIT=false
TITLE="${1:-}"
CATEGORY="${2:-}"
TAGS="${3:-}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --draft)    DRAFT=true; shift ;;
    --preview)  PREVIEW=true; shift ;;
    --git)      GIT=true; shift ;;
    *)          shift ;;
  esac
done

if [[ -z "$TITLE" ]]; then
  echo "Usage: $0 [--draft] [--preview] [--git] \"Title\" [category] [tags-csv]"
  exit 1
fi

# --- slug + date ---
SLUG=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g' | sed -E 's/^-+|-+$//g')
DATE=$(date +%Y-%m-%d)
FILE="content/posts/${DATE}-${SLUG}.md"

if [[ -f "$FILE" ]]; then
  echo "✗ Post already exists: $FILE"
  exit 1
fi

# --- category default ---
if [[ -z "$CATEGORY" ]]; then
  DAY_OF_WEEK=$(date +%u)  # 1=Mon..7=Sun
  case "$DAY_OF_WEEK" in
    1) CATEGORY="News" ;;
    2) CATEGORY="Code" ;;
    3) CATEGORY="Indonesia" ;;
    4) CATEGORY="Tools" ;;
    5) CATEGORY="Opinion" ;;
    6) CATEGORY="Build" ;;
    7) CATEGORY="Free" ;;
  esac
fi

# --- tags default ---
if [[ -z "$TAGS" ]]; then
  TAGS=$(echo "$CATEGORY" | tr '[:upper:]' '[:lower:]')
fi

DRAFT_FIELD="false"
[[ "$DRAFT" == "true" ]] && DRAFT_FIELD="true"

# --- write file ---
cat > "$FILE" <<EOF
---
title: "${TITLE}"
date: $(date +%Y-%m-%dT%H:%M:%S%z)
draft: ${DRAFT_FIELD}
description: ""
categories: ["${CATEGORY}"]
tags: [$(echo "$TAGS" | sed 's/,/", "/g' | sed 's/^/"/;s/$/"/')]
---

${TITLE}

<!--
Voice rules (from social-media-voice-guide):
- Simple declarative sentences. Short paragraphs.
- Contrarian angles backed by specific numbers and real examples.
- No corporate speak. No "I'm excited to share." No emoji in body text.
- Open with a hook that stops the scroll — contrarian claim, surprising number, or uncomfortable truth.
- End with a payoff: uncomfortable truth → "worth it" resolution.
-->

EOF

echo "✓ Created: $FILE"
echo "  title:    $TITLE"
echo "  category: $CATEGORY"
echo "  tags:     $TAGS"
echo "  draft:    $DRAFT_FIELD"

# --- preview ---
if [[ "$PREVIEW" == "true" ]]; then
  echo "→ Starting hugo server on :1313 (Ctrl-C to stop)"
  exec hugo server --port 1313 --bind 0.0.0.0
fi

# --- git commit + push ---
if [[ "$GIT" == "true" ]]; then
  git add "$FILE"
  git commit -m "post: $TITLE"
  echo "→ Committed. Push with: git push origin main"
fi
