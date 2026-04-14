from fastapi import APIRouter, HTTPException
from app.models.schemas import RunRequest, RunResponse, RunResult
from app.agents.crew_service import run_pipeline
from app.db.history import save_run, list_runs, get_run

router = APIRouter(prefix="/api", tags=["pipeline"])

# In-memory cache for performance (DB is source of truth)
_runs: dict[str, RunResult] = {}


@router.post("/run", response_model=RunResponse)
def run_prospect_pipeline(request: RunRequest):
    """
    Trigger the 4-agent SalesNeuro pipeline for a prospect.
    Returns the full research summary, personality profile, strategy brief, and 3-email sequence.
    Results are persisted to SQLite history database.
    """
    try:
        result = run_pipeline(
            prospect_name=request.prospect_name,
            company_name=request.company_name,
        )
        run_key = f"{request.prospect_name}::{request.company_name}"
        _runs[run_key] = result

        # Persist to database (non-critical if fails)
        save_run(result)

        return RunResponse(status="success", result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/v1/runs", response_model=list[dict])
def list_all_runs(limit: int = 50):
    """
    Return all previously run analyses with metadata.
    Returns: [{ id, prospect_name, company_name, created_at, status }, ...]
    """
    return list_runs(limit=limit)


@router.get("/v1/runs/{run_id}", response_model=RunResponse)
def get_run_detail(run_id: str):
    """Return the full run result including all 4 agent outputs."""
    result = get_run(run_id)
    if not result:
        raise HTTPException(status_code=404, detail="Run not found")
    return RunResponse(status="success", result=result)


@router.get("/prospects", response_model=list[RunResult])
def list_prospects():
    """Return all previously run prospect results from in-memory cache."""
    return list(_runs.values())


@router.get("/prospects/{prospect_name}", response_model=RunResponse)
def get_prospect(prospect_name: str):
    """Return the most recent run result for a given prospect name."""
    matches = [v for k, v in _runs.items() if k.startswith(prospect_name + "::")]
    if not matches:
        raise HTTPException(status_code=404, detail="Prospect not found")
    return RunResponse(status="success", result=matches[-1])
