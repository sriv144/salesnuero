import logging
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import ProspectRun
from app.models.schemas import (
    RunRequest,
    RunResult,
    RunResponse,
    JobSubmitResponse,
    JobStatus,
    JobStatusResponse,
    JobListItem,
)
from app.services.job_runner import submit_job, get_job, list_jobs, list_completed_by_prospect

log = logging.getLogger("salesnuero.routes")

router = APIRouter(prefix="/api", tags=["pipeline"])


def _db_run_to_result(run: ProspectRun) -> RunResult:
    """Convert a completed ProspectRun ORM object to a RunResult schema."""
    return RunResult(
        prospect_name=run.prospect_name,
        company_name=run.company_name,
        research_summary=run.research_summary or "",
        profile_raw=run.profile_raw or "",
        strategy_brief=run.strategy_brief or "",
        emails_raw=run.emails_raw or "",
        raw_crew_output=run.raw_crew_output or "",
    )


def _db_run_to_job_status(run: ProspectRun) -> JobStatusResponse:
    """Convert a ProspectRun ORM object to a JobStatusResponse schema."""
    result = None
    if run.status == "completed":
        result = _db_run_to_result(run)

    return JobStatusResponse(
        job_id=run.id,
        prospect_name=run.prospect_name,
        company_name=run.company_name,
        status=JobStatus(run.status),
        created_at=run.created_at,
        completed_at=run.completed_at,
        result=result,
        error=run.error_message,
    )


# ── Job submission ─────────────────────────────────────────────────────────────

@router.post("/run", response_model=JobSubmitResponse, status_code=202)
def run_prospect_pipeline(request: RunRequest) -> JobSubmitResponse:
    """
    Submit a prospect pipeline job for async execution.

    Returns immediately with a job_id. Poll GET /api/jobs/{job_id}
    to check status and retrieve results when complete.

    The pipeline runs in a background thread — typical duration 2-5 minutes.
    """
    try:
        job_id = submit_job(
            prospect_name=request.prospect_name,
            company_name=request.company_name,
        )
        log.info(f"Submitted job {job_id} for {request.prospect_name} @ {request.company_name}")
        return JobSubmitResponse(
            job_id=job_id,
            status=JobStatus.pending,
        )
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        log.error(f"Failed to submit job: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to submit job: {e}")


# ── Job status polling ─────────────────────────────────────────────────────────

@router.get("/jobs/{job_id}", response_model=JobStatusResponse)
def get_job_status(job_id: str, db: Session = Depends(get_db)) -> JobStatusResponse:
    """
    Poll the status of a pipeline job.

    Returns status: 'pending' | 'running' | 'completed' | 'failed'.
    When status is 'completed', the full result is included.
    When status is 'failed', the error message is included.
    """
    run = get_job(job_id, db)
    if not run:
        raise HTTPException(status_code=404, detail=f"Job '{job_id}' not found")
    return _db_run_to_job_status(run)


@router.get("/jobs", response_model=list[JobListItem])
def list_all_jobs(limit: int = 50, db: Session = Depends(get_db)) -> list[JobListItem]:
    """
    List recent pipeline jobs (newest first).

    Query params:
    - limit: max number of jobs to return (default 50, max 200)
    """
    limit = min(limit, 200)
    runs = list_jobs(db, limit=limit)
    return [
        JobListItem(
            job_id=run.id,
            prospect_name=run.prospect_name,
            company_name=run.company_name,
            status=JobStatus(run.status),
            created_at=run.created_at,
            completed_at=run.completed_at,
        )
        for run in runs
    ]


# ── Backward-compatible prospect endpoints ─────────────────────────────────────

@router.get("/prospects", response_model=list[RunResult])
def list_prospects(db: Session = Depends(get_db)) -> list[RunResult]:
    """
    Return all completed prospect runs (backward-compatible with v1 API).
    Use GET /api/jobs for the full job list including pending/failed.
    """
    runs = (
        db.query(ProspectRun)
        .filter(ProspectRun.status == "completed")
        .order_by(ProspectRun.created_at.desc())
        .all()
    )
    return [_db_run_to_result(r) for r in runs]


@router.get("/prospects/{prospect_name}", response_model=RunResponse)
def get_prospect(prospect_name: str, db: Session = Depends(get_db)) -> RunResponse:
    """
    Return the most recent completed run for a given prospect name.
    Backward-compatible with the v1 API.
    """
    runs = list_completed_by_prospect(prospect_name, db)
    if not runs:
        raise HTTPException(
            status_code=404,
            detail=f"No completed run found for prospect '{prospect_name}'",
        )
    return RunResponse(status="success", result=_db_run_to_result(runs[0]))
