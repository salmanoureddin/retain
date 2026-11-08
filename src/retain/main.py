from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, func, select

from retain import __version__
from retain.db import get_session, init_db
from retain.models import Card, Deck, utcnow

BASE_DIR = Path(__file__).parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    init_db()
    yield


app = FastAPI(title="Retain", version=__version__, lifespan=lifespan)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": __version__}


@app.get("/", response_class=HTMLResponse)
def index(request: Request, session: Session = Depends(get_session)) -> HTMLResponse:
    decks = session.exec(select(Deck).order_by(Deck.name)).all()
    due_count = session.exec(
        select(func.count()).select_from(Card).where(Card.due_at <= utcnow())
    ).one()
    return templates.TemplateResponse(
        request, "index.html", {"decks": decks, "due_count": due_count}
    )
