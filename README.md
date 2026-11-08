# Retain

Spaced-repetition flashcards with built-in habit tracking.

Most people forget what they study within days, and most habit apps only count
streaks. Retain schedules each card for review right when you are about to forget
it, then shows your consistency and retention over time.

## Status

Early development. See the [roadmap](#roadmap) and the open
[milestones](../../milestones).

## Features

- [x] SM-2 scheduling algorithm (`src/retain/scheduler.py`), unit tested
- [x] Data model for decks, cards, and review history
- [ ] Create and edit decks and cards (markdown, code snippets)
- [ ] Review session with Again / Hard / Good / Easy ratings
- [ ] Progress dashboard: reviews per day, retention, streaks, upcoming workload
- [ ] Daily goals and a calendar heatmap

## Stack

| Layer | Choice | Why |
| --- | --- | --- |
| Web framework | FastAPI | Typed, fast, great docs |
| UI | Jinja2 templates + HTMX (planned) | Server-rendered, no JS build step |
| Database | SQLite via SQLModel | Zero setup, easy to swap for Postgres |
| Tests | pytest | Standard |
| Lint / format | Ruff | One fast tool for both |
| CI | GitHub Actions | Lint and tests on Python 3.11 to 3.13 |

## Quickstart

```bash
git clone https://github.com/<you>/retain.git
cd retain
python -m venv .venv && source .venv/bin/activate
make install
make run          # http://127.0.0.1:8000
```

## Development

```bash
make test         # pytest with coverage
make lint         # ruff check + format check
make format       # auto-fix and format
make check        # lint + test (what CI runs)
```

Configuration is via environment variables:

| Variable | Default | Purpose |
| --- | --- | --- |
| `RETAIN_DATABASE_URL` | `sqlite:///./retain.db` | SQLAlchemy database URL |

## Project layout

```
src/retain/
  main.py        FastAPI app and routes
  models.py      SQLModel tables: Deck, Card, Review
  scheduler.py   Pure SM-2 scheduling logic (no I/O)
  db.py          Engine and session dependency
  templates/     Jinja2 templates
  static/        CSS
tests/           pytest suite
docs/            Architecture notes and AI session log
scripts/         Repo helpers (issue creation)
```

## Roadmap

1. Project setup and data model
2. Deck and card creation
3. Scheduler integration and review history
4. Review session interface
5. Progress dashboard
6. Polish, docs, and deployment

## Contributing

Work happens in small issues merged through pull requests. See
[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for design notes and
[docs/AI_LOG.md](docs/AI_LOG.md) for how AI assistance is documented.

## License

MIT. See [LICENSE](LICENSE).
