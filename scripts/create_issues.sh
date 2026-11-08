#!/usr/bin/env bash
# Creates milestones and issues on GitHub from the roadmap.
# Requires the GitHub CLI (https://cli.github.com), authenticated with `gh auth login`,
# and must be run from inside the cloned repo.
set -euo pipefail

REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner)"
echo "Creating milestones and issues in $REPO"

milestone() {
  gh api "repos/$REPO/milestones" -f title="$1" -f description="$2" >/dev/null
  echo "  milestone: $1"
}

issue() {  # milestone, title, body
  gh issue create --milestone "$1" --title "$2" --body "$3" >/dev/null
  echo "    issue: $2"
}

M1="1. Setup and data model"
M2="2. Decks and cards"
M3="3. Scheduler integration"
M4="4. Review session"
M5="5. Progress dashboard"
M6="6. Polish and deploy"

milestone "$M1" "Repo, CI, tooling, and models"
milestone "$M2" "CRUD for decks and cards"
milestone "$M3" "Wire the SM-2 scheduler into the app"
milestone "$M4" "The daily review experience"
milestone "$M5" "Stats and habit tracking"
milestone "$M6" "Docs, hardening, and deployment"

issue "$M1" "Add Alembic migrations" \
  "Replace \`create_all\` with Alembic. Generate an initial migration for Deck, Card, Review.

- [ ] Alembic configured against \`RETAIN_DATABASE_URL\`
- [ ] Initial migration committed
- [ ] \`make migrate\` target
- [ ] Docs updated"
issue "$M1" "Add mypy to CI" \
  "Type-check \`src/\` in CI. Fix or narrowly ignore any SQLModel typing noise."

issue "$M2" "Create, rename, and delete decks" \
  "- [ ] Form to create a deck (HTMX)
- [ ] Rename and delete with confirmation
- [ ] Tests for each route"
issue "$M2" "Create and edit cards with markdown" \
  "- [ ] Card form with front/back markdown
- [ ] Render markdown with markdown-it-py, including fenced code blocks
- [ ] Syntax highlighting for code snippets
- [ ] Sanitize rendered HTML"
issue "$M2" "Tag cards and filter by tag" \
  "- [ ] Tag model (many-to-many)
- [ ] Filter card list by tag"

issue "$M3" "Apply a rating to a card and persist the result" \
  "Service function that calls \`scheduler.schedule\`, updates the Card, and writes a Review row in one transaction.

- [ ] Function plus tests against an in-memory DB
- [ ] Lapses recorded correctly"
issue "$M3" "Query the due queue" \
  "- [ ] Due cards ordered by \`due_at\`
- [ ] Optional per-deck filter
- [ ] Daily new-card limit setting"

issue "$M4" "Review session page" \
  "- [ ] Show front, reveal back, then rate with Again / Hard / Good / Easy
- [ ] HTMX swaps the next card without a full reload
- [ ] Keyboard shortcuts (space to reveal, 1-4 to rate)
- [ ] Empty state when nothing is due"
issue "$M4" "Preview next intervals on rating buttons" \
  "Show the interval each button would produce (e.g. Good: 6d) using \`scheduler.schedule\` without saving."

issue "$M5" "Dashboard: reviews per day and retention" \
  "- [ ] Aggregate queries over Review
- [ ] Chart (server-rendered SVG or a small JS lib)
- [ ] Retention rate = non-lapse reviews / total reviews"
issue "$M5" "Streaks and daily goal" \
  "- [ ] Daily review goal setting
- [ ] Current and longest streak
- [ ] Calendar heatmap"
issue "$M5" "Upcoming workload forecast" \
  "Chart of cards due per day over the next 30 days."

issue "$M6" "Import and export decks" \
  "- [ ] Export a deck to JSON
- [ ] Import from JSON and CSV"
issue "$M6" "Dockerfile and deployment guide" \
  "- [ ] Dockerfile
- [ ] Deploy docs for one host (Fly.io, Railway, or similar)
- [ ] Health check wired to \`/health\`"
issue "$M6" "Accessibility and responsive pass" \
  "Keyboard-only run through every page, contrast check, and a mobile layout review."

echo "Done."
