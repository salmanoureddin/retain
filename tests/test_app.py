from datetime import timedelta

from retain.models import Card, Deck, utcnow


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_index_empty(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "No decks yet" in r.text
    assert "0</p>" in r.text


def test_index_counts_only_due_cards(client, session):
    deck = Deck(name="Python")
    session.add(deck)
    session.commit()
    session.refresh(deck)

    session.add(Card(deck_id=deck.id, front="a", back="b"))  # due now
    session.add(Card(deck_id=deck.id, front="c", back="d", due_at=utcnow() + timedelta(days=3)))
    session.commit()

    r = client.get("/")
    assert "Python" in r.text
    assert "1</p>" in r.text
    assert "card due today" in r.text
