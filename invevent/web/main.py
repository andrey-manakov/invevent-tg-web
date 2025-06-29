import os
import datetime
from pathlib import Path
from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from invevent.models import Event, ensure_db

from dotenv import load_dotenv

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///db.sqlite")
ensure_db()  # create DB if it doesn't exist
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
BASE_DIR = Path(__file__).resolve().parents[2]
app = FastAPI()
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def root():
    return RedirectResponse("/webapp")

@app.get("/webapp", response_class=HTMLResponse)
def webapp(request: Request, db: SessionLocal = Depends(get_db)):
    # TODO: get user from Telegram (e.g. via query param or Telegram Web App init data)
    events = db.query(Event).all()
    event_points = [{
        "title": e.title,
        "lat": e.lat,
        "lng": e.lng,
        "description": e.description or "",
        "datetime": e.datetime.strftime("%Y-%m-%d %H:%M"),
        "id": e.id,
    } for e in events]
    return templates.TemplateResponse("webapp.html", {
        "request": request,
        "events": event_points,
    })

@app.post("/api/events")
def create_event(
    title: str = Form(...),
    description: str = Form(""),
    datetime_str: str = Form(...),
    lat: float = Form(...),
    lng: float = Form(...),
    db: SessionLocal = Depends(get_db),
):
    dt = datetime.datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M")
    event = Event(
        title=title,
        description=description,
        datetime=dt,
        lat=lat,
        lng=lng,
        creator_id=1  # TODO: fetch from session/user
    )
    db.add(event)
    db.commit()
    return RedirectResponse("/webapp", status_code=303)

@app.get("/api/events")
def list_events(db: SessionLocal = Depends(get_db)):
    events = db.query(Event).all()
    return [{
        "title": e.title,
        "lat": e.lat,
        "lng": e.lng,
        "description": e.description or "",
        "datetime": e.datetime.strftime("%Y-%m-%d %H:%M"),
        "id": e.id,
    } for e in events]
