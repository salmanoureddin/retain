from datetime import UTC, datetime, timedelta

import pytest

from retain.scheduler import MAX_INTERVAL_DAYS, MIN_EASE, CardState, Rating, schedule

NOW = datetime(2026, 1, 1, 9, 0, tzinfo=UTC)


def test_first_good_review_is_one_day():
    state, due = schedule(CardState(), Rating.GOOD, NOW)
    assert (state.repetitions, state.interval_days) == (1, 1)
    assert due == NOW + timedelta(days=1)


def test_second_good_review_is_six_days():
    state, _ = schedule(CardState(), Rating.GOOD, NOW)
    state, due = schedule(state, Rating.GOOD, NOW)
    assert state.interval_days == 6
    assert due == NOW + timedelta(days=6)


def test_third_review_multiplies_by_ease():
    state = CardState()
    for _ in range(3):
        state, _ = schedule(state, Rating.GOOD, NOW)
    assert state.interval_days == 15  # round(6 * 2.5)


def test_good_leaves_ease_unchanged_and_easy_raises_it():
    good, _ = schedule(CardState(), Rating.GOOD, NOW)
    easy, _ = schedule(CardState(), Rating.EASY, NOW)
    assert good.ease_factor == pytest.approx(2.5)
    assert easy.ease_factor == pytest.approx(2.6)


def test_hard_lowers_ease_but_still_counts_as_a_pass():
    state, _ = schedule(CardState(), Rating.HARD, NOW)
    assert state.ease_factor == pytest.approx(2.36)
    assert state.repetitions == 1


def test_again_resets_progress_and_keeps_ease():
    state = CardState(ease_factor=2.3, interval_days=15, repetitions=4)
    new, due = schedule(state, Rating.AGAIN, NOW)
    assert (new.repetitions, new.interval_days) == (0, 1)
    assert new.ease_factor == 2.3
    assert due == NOW + timedelta(days=1)


def test_ease_never_drops_below_minimum():
    state = CardState()
    for _ in range(50):
        state, _ = schedule(state, Rating.HARD, NOW)
    assert state.ease_factor == MIN_EASE


def test_schedule_does_not_mutate_input():
    state = CardState()
    schedule(state, Rating.EASY, NOW)
    assert state == CardState()


def test_interval_is_capped():
    state = CardState(ease_factor=2.5, interval_days=MAX_INTERVAL_DAYS, repetitions=10)
    new, due = schedule(state, Rating.EASY, NOW)
    assert new.interval_days == MAX_INTERVAL_DAYS
    assert due == NOW + timedelta(days=MAX_INTERVAL_DAYS)
