import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel


# --- Request Models ---

class RunRequest(BaseModel):
    prospect_name: str
    company_name: str


# --- Sub-models ---

class BigFiveScores(BaseModel):
    openness: int        # 1-10
    conscientiousness: int
    extraversion: int
    agreeableness: int
    neuroticism: int


class PersonalityProfile(BaseModel):
    big_five: BigFiveScores
    disc_type: str                     # D, I, S, or C
    buying_motivators: list[str]
    communication_style: str
    objection_patterns: list[str]
    raw_output: str                    # full text from profiler agent


class ValueProposition(BaseModel):
    title: str
    emotional_hook: str
    rational_justification: str


class Email(BaseModel):
    subject: str
    body: str
    ps_line: str


class EmailSequence(BaseModel):
    email_1: Email
    email_2: Email
    email_3: Email
    raw_output: str                    # full text from copywriter agent


# --- Pipeline Result ---

class RunResult(BaseModel):
    prospect_name: str
    company_name: str
    research_summary: str
    profile_raw: str = ""
    personality_profile: Optional[PersonalityProfile] = None
    strategy_brief: str
    emails_raw: str = ""
    email_sequence: Optional[EmailSequence] = None
    raw_crew_output: str


class RunResponse(BaseModel):
    status: str                        # "success" | "error"
    result: Optional[RunResult] = None
    error: Optional[str] = None


# --- Async Job Models ---

class JobStatus(str, Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"


class JobSubmitResponse(BaseModel):
    """Returned immediately from POST /api/run — before the pipeline executes."""
    job_id: str
    status: JobStatus
    message: str = "Pipeline job submitted. Poll /api/jobs/{job_id} for status."


class JobStatusResponse(BaseModel):
    """Full job status including result once completed."""
    job_id: str
    prospect_name: str
    company_name: str
    status: JobStatus
    created_at: datetime.datetime
    completed_at: Optional[datetime.datetime] = None
    result: Optional[RunResult] = None
    error: Optional[str] = None


class JobListItem(BaseModel):
    """Lightweight job record for the list endpoint."""
    job_id: str
    prospect_name: str
    company_name: str
    status: JobStatus
    created_at: datetime.datetime
    completed_at: Optional[datetime.datetime] = None

    model_config = {"from_attributes": True}
