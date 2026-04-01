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


# --- Response Models ---

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
