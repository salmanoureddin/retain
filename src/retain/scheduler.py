"""Spaced-repetition scheduling (SM-2 family).

Pure functions only: no database, no clock. Callers pass ``now`` in, which
keeps this module trivial to unit test.

Reference: https://super-memory.com/english/ol/sm2.htm
"""

from dataclasses import dataclass, replace
from datetime import datetime, timedelta
from enum import IntEnum

MIN_EASE = 1.3
MAX_INTERVAL_DAYS = 36_500  # 100 years; also keeps date math in range
DEFAULT_EASE = 2.5


class Rating(IntEnum):
    """The four review buttons shown to the user."""

    AGAIN = 1
    HARD = 2
    GOOD = 3
    EASY = 4


# Map our four buttons onto SM-2's 0-5 quality scale. Quality < 3 is a lapse.
_QUALITY = {Rating.AGAIN: 1, Rating.HARD: 3, Rating.GOOD: 4, Rating.EASY: 5}


@dataclass(frozen=True)
class CardState:
    ease_factor: float = DEFAULT_EASE
    interval_days: int = 0
    repetitions: int = 0


def schedule(state: CardState, rating: Rating, now: datetime) -> tuple[CardState, datetime]:
    """Return the card's new state and the datetime it is next due."""
    quality = _QUALITY[rating]

    if quality < 3:
        # Lapse: restart the learning steps. Ease factor is left unchanged.
        new = replace(state, repetitions=0, interval_days=1)
        return new, now + timedelta(days=new.interval_days)

    if state.repetitions == 0:
        interval = 1
    elif state.repetitions == 1:
        interval = 6
    else:
        interval = max(1, round(state.interval_days * state.ease_factor))
    interval = min(interval, MAX_INTERVAL_DAYS)

    ease = state.ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    ease = max(MIN_EASE, ease)

    new = CardState(ease_factor=ease, interval_days=interval, repetitions=state.repetitions + 1)
    return new, now + timedelta(days=interval)
