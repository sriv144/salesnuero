import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.db.database import init_db
from app.services.job_runner import recover_interrupted_jobs

log = logging.getLogger("salesnuero")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: initialize DB and recover interrupted jobs on startup."""
    log.info("SalesNeuro starting up — initializing database...")
    init_db()
    recover_interrupted_jobs()
    log.info("Database ready.")
    yield
    log.info("SalesNeuro shutting down.")


app = FastAPI(
    title="SalesNeuro API",
    description="AI Buyer Psychology Intelligence & Outreach platform",
    version="0.2.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "0.2.0"}
