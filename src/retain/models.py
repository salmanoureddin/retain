"""Database models.

All datetimes are timezone-aware UTC. SQLModel's datetime column type stores
them as UTC and returns them as aware UTC, even on SQLite.
"""

from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


def utcnow() -> datetime:
    return datetime.now(UTC)


class Deck(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str = ""
    created_at: datetime = Field(default_factory=utcnow)


class Card(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    deck_id: int = Field(foreign_key="deck.id", index=True)
    front: str  # markdown
    back: str  # markdown
    created_at: datetime = Field(default_factory=utcnow)

    # Scheduling state (see retain.scheduler)
    ease_factor: float = 2.5
    interval_days: int = 0
    repetitions: int = 0
    due_at: datetime = Field(default_factory=utcnow, index=True)


class Review(SQLModel, table=True):
    """One row per answered card. Powers the progress dashboard."""

    id: int | None = Field(default=None, primary_key=True)
    card_id: int = Field(foreign_key="card.id", index=True)
    rating: int  # retain.scheduler.Rating value
    reviewed_at: datetime = Field(default_factory=utcnow, index=True)
    interval_days_after: int
    ease_factor_after: float
