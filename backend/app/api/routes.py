from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.models.schemas import RunRequest, RunResponse, RunResult
from app.agents.crew_service import run_pipeline

router = APIRouter(prefix="/api", tags=["pipeline"])

# In-memory store for completed runs (replace with DB later)
_runs: dict[str, RunResult] = {}


@router.post("/run", response_model=RunResponse)
def run_prospect_pipeline(request: RunRequest):
    """
    Trigger the 4-agent SalesNeuro pipeline for a prospect.
    Returns the full research summary, personality profile, strategy brief, and 3-email sequence.
    """
    try:
        result = run_pipeline(
            prospect_name=request.prospect_name,
            company_name=request.company_name,
        )
        run_key = f"{request.prospect_name}::{request.company_name}"
        _runs[run_key] = result
        return RunResponse(status="success", result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/prospects", response_model=list[RunResult])
def list_prospects():
    """Return all previously run prospect results."""
    return list(_runs.values())


@router.get("/prospects/{prospect_name}", response_model=RunResponse)
def get_prospect(prospect_name: str):
    """Return the most recent run result for a given prospect name."""
    matches = [v for k, v in _runs.items() if k.startswith(prospect_name + "::")]
    if not matches:
        raise HTTPException(status_code=404, detail="Prospect not found")
    return RunResponse(status="success", result=matches[-1])
