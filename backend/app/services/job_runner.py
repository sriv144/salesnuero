"""
Async job runner for SalesNeuro pipeline execution.

Provides a thread-pool backed job queue so that:
1. POST /api/run returns immediately with a job_id
2. The pipeline runs in a background thread
3. GET /api/jobs/{job_id} can be polled for status

On server restart, any jobs that were "running" are marked "failed"
with an explanatory error message.
"""
import datetime
import logging
import uuid
from concurrent.futures import ThreadPoolExecutor, Future
from typing import Optional

from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.db.models import ProspectRun
from app.agents.crew_service import run_pipeline

log = logging.getLogger("salesnuero.job_runner")

# Max 2 concurrent pipeline jobs to avoid overloading the LLM API
_executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix="pipeline-worker")
_active_futures: dict[str, Future] = {}
MAX_QUEUE_SIZE = 10


def recover_interrupted_jobs() -> None:
    """
    On startup, mark any jobs still in 'pending' or 'running' state as 'failed'.
    These are jobs that were interrupted by a server restart.
    """
    db = SessionLocal()
    try:
        interrupted = (
            db.query(ProspectRun)
            .filter(ProspectRun.status.in_(["pending", "running"]))
            .all()
        )
        for job in interrupted:
            job.status = "failed"
            job.error_message = "Server restarted during execution. Please retry."
            job.completed_at = datetime.datetime.utcnow()
        if interrupted:
            db.commit()
            log.warning(f"Recovered {len(interrupted)} interrupted job(s) from previous run")
    finally:
        db.close()


def submit_job(prospect_name: str, company_name: str) -> str:
    """
    Create a pending job record in the DB and submit it to the thread pool.
    Returns the job_id (UUID string).
    Raises RuntimeError if the queue is full.
    """
    # Check queue depth
    db = SessionLocal()
    try:
        pending_count = (
            db.query(ProspectRun)
            .filter(ProspectRun.status.in_(["pending", "running"]))
            .count()
        )
        if pending_count >= MAX_QUEUE_SIZE:
            raise RuntimeError(
                f"Too many concurrent jobs ({pending_count}/{MAX_QUEUE_SIZE}). "
                "Please wait for existing jobs to complete."
            )

        job_id = str(uuid.uuid4())
        run = ProspectRun(
            id=job_id,
            prospect_name=prospect_name,
            company_name=company_name,
            status="pending",
            created_at=datetime.datetime.utcnow(),
        )
        db.add(run)
        db.commit()
        log.info(f"Submitted job {job_id} for {prospect_name} @ {company_name}")
    finally:
        db.close()

    # Submit to thread pool
    future = _executor.submit(_execute_job, job_id, prospect_name, company_name)
    _active_futures[job_id] = future
    return job_id


def _execute_job(job_id: str, prospect_name: str, company_name: str) -> None:
    """
    Background worker: runs the CrewAI pipeline and persists results.
    Always updates job status — never raises.
    """
    db = SessionLocal()
    try:
        # Mark as running
        job = db.query(ProspectRun).filter(ProspectRun.id == job_id).first()
        if not job:
            log.error(f"Job {job_id} not found in DB at execution start")
            return
        job.status = "running"
        db.commit()
        log.info(f"Starting pipeline for job {job_id}")

        # Run the pipeline
        result = run_pipeline(
            prospect_name=prospect_name,
            company_name=company_name,
        )

        # Persist results
        job = db.query(ProspectRun).filter(ProspectRun.id == job_id).first()
        if job:
            job.status = "completed"
            job.completed_at = datetime.datetime.utcnow()
            job.research_summary = result.research_summary
            job.profile_raw = result.profile_raw
            job.strategy_brief = result.strategy_brief
            job.emails_raw = result.emails_raw
            job.raw_crew_output = result.raw_crew_output
            db.commit()
            log.info(f"Job {job_id} completed successfully")

    except Exception as exc:
        log.error(f"Job {job_id} failed: {exc}", exc_info=True)
        try:
            job = db.query(ProspectRun).filter(ProspectRun.id == job_id).first()
            if job:
                job.status = "failed"
                job.error_message = str(exc)[:2000]
                job.completed_at = datetime.datetime.utcnow()
                db.commit()
        except Exception as db_exc:
            log.error(f"Failed to persist error state for job {job_id}: {db_exc}")
    finally:
        db.close()
        _active_futures.pop(job_id, None)


def get_job(job_id: str, db: Session) -> Optional[ProspectRun]:
    """Retrieve a job record by ID."""
    return db.query(ProspectRun).filter(ProspectRun.id == job_id).first()


def list_jobs(db: Session, limit: int = 50) -> list[ProspectRun]:
    """Return recent jobs sorted by created_at descending."""
    return (
        db.query(ProspectRun)
        .order_by(ProspectRun.created_at.desc())
        .limit(limit)
        .all()
    )


def list_completed_by_prospect(prospect_name: str, db: Session) -> list[ProspectRun]:
    """Return all completed runs for a given prospect name."""
    return (
        db.query(ProspectRun)
        .filter(
            ProspectRun.prospect_name == prospect_name,
            ProspectRun.status == "completed",
        )
        .order_by(ProspectRun.created_at.desc())
        .all()
    )
