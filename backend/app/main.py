import logging
import os
from contextlib import asynccontextmanager

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routes import router
from app.config import settings
from app.database import Base, SessionLocal, engine
from app.seed import ensure_seed
from app.services.conflict_sync import run_conflict_sync

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("country-risk-intel")

scheduler = BackgroundScheduler(timezone="Europe/Istanbul")


def _daily_conflict_job() -> None:
    log.info("Scheduled conflict RSS sync starting (12:00 TR).")
    with SessionLocal() as session:
        run = run_conflict_sync(session)
        log.info("Sync finished: %s — %s", run.status, run.message)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as session:
        ensure_seed(session)
    if settings.scheduler_enabled:
        try:
            scheduler.add_job(_daily_conflict_job, "cron", hour=12, minute=0)
            scheduler.start()
            log.info("APScheduler: günlük görev Europe/Istanbul 12:00 olarak ayarlandı.")
        except Exception:  # noqa: BLE001
            log.exception("APScheduler başlatılamadı; API yine de çalışır (manuel /api/sync kullanın).")
    yield
    if settings.scheduler_enabled:
        scheduler.shutdown(wait=False)


app = FastAPI(
    title="Country Risk Intelligence API",
    description="Lojistik ve dış ticaret odaklı ülke riski ve çatışma haber akışı.",
    version="1.0.0",
    lifespan=lifespan,
)

_origins = [o.strip() for o in settings.cors_origins.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins or ["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

_static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "static"))
if os.path.isdir(_static_dir):
    app.mount("/", StaticFiles(directory=_static_dir, html=True), name="frontend")
