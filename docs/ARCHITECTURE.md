# Architecture

## Goals

- Keep the scheduling logic isolated, pure, and heavily tested.
- Keep the stack small enough to understand end to end: one language, one process, one database file.

## Request flow

```
Browser -> FastAPI route -> SQLModel session -> SQLite
                |
                +-> Jinja2 template (HTML response)
```

Interactivity will come from HTMX partial swaps rather than a JS framework.

## Data model

- **Deck**: a named collection of cards.
- **Card**: front/back markdown plus its current scheduling state
  (`ease_factor`, `interval_days`, `repetitions`, `due_at`).
- **Review**: append-only log of every answer. The dashboard is computed from this table.

All datetimes are timezone-aware UTC (`models.utcnow()`). SQLModel's datetime
column type stores UTC and returns aware UTC, even on SQLite. Convert to local
time only at the display layer.

## Scheduler

`retain.scheduler.schedule(state, rating, now)` is a pure function that returns
the new `CardState` and the next due datetime. It takes `now` as an argument, so
tests never depend on the clock.

Choices worth knowing:

- Four buttons (Again, Hard, Good, Easy) map to SM-2 quality 1, 3, 4, 5.
- A lapse (Again) resets repetitions and sets the interval to 1 day. Ease is unchanged.
- Intervals after the second repetition use the ease factor from *before* the current update.
- Ease is clamped at 1.3, and intervals are capped at 100 years.

## Decisions to revisit

- Migrations: the app uses `create_all` for now. Add Alembic before the first schema change that matters.
- Scheduler: consider FSRS as an alternative, behind the same function signature.
- Auth: single-user for now. Multi-user needs a `user_id` on decks.
