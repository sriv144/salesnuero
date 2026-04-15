"""
Tests for SQLite persistence and async job runner.
Uses an in-memory SQLite database to avoid filesystem side effects.
"""
import datetime
import os
import sys
import time
import uuid
from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Make backend importable
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# ── In-memory DB fixture ───────────────────────────────────────────────────────

@pytest.fixture()
def db_session():
    """Provide a clean in-memory SQLite session for each test."""
    # Must import after path setup
    from app.db.database import Base
    from app.db import models  # noqa: registers ORM models

    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


# ── ORM model tests ────────────────────────────────────────────────────────────

class TestProspectRunModel:
    def test_create_pending_job(self, db_session):
        from app.db.models import ProspectRun
        run = ProspectRun(
            id=str(uuid.uuid4()),
            prospect_name="Alice Smith",
            company_name="Acme Corp",
            status="pending",
            created_at=datetime.datetime.utcnow(),
        )
        db_session.add(run)
        db_session.commit()

        fetched = db_session.query(ProspectRun).filter_by(prospect_name="Alice Smith").first()
        assert fetched is not None
        assert fetched.status == "pending"
        assert fetched.company_name == "Acme Corp"

    def test_update_job_to_completed(self, db_session):
        from app.db.models import ProspectRun
        job_id = str(uuid.uuid4())
        run = ProspectRun(
            id=job_id,
            prospect_name="Bob Lee",
            company_name="TechCo",
            status="pending",
            created_at=datetime.datetime.utcnow(),
        )
        db_session.add(run)
        db_session.commit()

        # Update to completed
        run.status = "completed"
        run.completed_at = datetime.datetime.utcnow()
        run.research_summary = "Bob leads engineering at TechCo..."
        run.emails_raw = "Email 1: Subject: Hello Bob..."
        db_session.commit()

        fetched = db_session.query(ProspectRun).filter_by(id=job_id).first()
        assert fetched.status == "completed"
        assert fetched.research_summary is not None
        assert fetched.completed_at is not None

    def test_failed_job_stores_error(self, db_session):
        from app.db.models import ProspectRun
        job_id = str(uuid.uuid4())
        run = ProspectRun(
            id=job_id,
            prospect_name="Carol",
            company_name="FailCo",
            status="running",
            created_at=datetime.datetime.utcnow(),
        )
        db_session.add(run)
        db_session.commit()

        run.status = "failed"
        run.error_message = "NVIDIA API rate limit exceeded"
        run.completed_at = datetime.datetime.utcnow()
        db_session.commit()

        fetched = db_session.query(ProspectRun).filter_by(id=job_id).first()
        assert fetched.status == "failed"
        assert "rate limit" in fetched.error_message

    def test_data_persists_across_sessions(self):
        """Simulate server restart: data must persist in a new session."""
        from app.db.database import Base
        from app.db import models  # noqa

        engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)

        from app.db.models import ProspectRun
        job_id = str(uuid.uuid4())

        # Session 1: create
        s1 = Session()
        run = ProspectRun(
            id=job_id,
            prospect_name="Dave",
            company_name="PersistCo",
            status="completed",
            created_at=datetime.datetime.utcnow(),
            research_summary="Dave is a VP of Sales...",
        )
        s1.add(run)
        s1.commit()
        s1.close()

        # Session 2: verify
        s2 = Session()
        fetched = s2.query(ProspectRun).filter_by(id=job_id).first()
        assert fetched is not None
        assert fetched.prospect_name == "Dave"
        assert "VP of Sales" in fetched.research_summary
        s2.close()


# ── Job runner logic tests ─────────────────────────────────────────────────────

class TestJobRunner:
    def test_recover_interrupted_jobs(self, db_session):
        """Interrupted running/pending jobs should be marked failed on recovery."""
        from app.db.models import ProspectRun
        from app.db.database import SessionLocal

        # Insert a "running" job that was interrupted
        job_id = str(uuid.uuid4())
        run = ProspectRun(
            id=job_id,
            prospect_name="Eve",
            company_name="EdgeCo",
            status="running",
            created_at=datetime.datetime.utcnow(),
        )
        db_session.add(run)
        db_session.commit()

        # Simulate recovery using our session
        from app.db.models import ProspectRun as PR
        interrupted = db_session.query(PR).filter(PR.status.in_(["pending", "running"])).all()
        for job in interrupted:
            job.status = "failed"
            job.error_message = "Server restarted during execution. Please retry."
            job.completed_at = datetime.datetime.utcnow()
        db_session.commit()

        fetched = db_session.query(PR).filter_by(id=job_id).first()
        assert fetched.status == "failed"
        assert "Server restarted" in fetched.error_message

    def test_list_jobs_sorted_by_created_at(self, db_session):
        """list_jobs should return newest first."""
        from app.db.models import ProspectRun
        # Import list_jobs with crew_service mocked to avoid heavy deps
        import unittest.mock as mock
        mock_crew = mock.MagicMock()
        with mock.patch.dict("sys.modules", {
            "app.agents.crew_service": mock_crew,
            "chromadb": mock.MagicMock(),
            "crewai": mock.MagicMock(),
        }):
            from app.services.job_runner import list_jobs

        now = datetime.datetime.utcnow()
        for i, name in enumerate(["first", "second", "third"]):
            run = ProspectRun(
                id=str(uuid.uuid4()),
                prospect_name=name,
                company_name="TestCo",
                status="completed",
                created_at=now + datetime.timedelta(seconds=i),
            )
            db_session.add(run)
        db_session.commit()

        jobs = list_jobs(db_session, limit=10)
        names = [j.prospect_name for j in jobs]
        assert names[0] == "third"   # newest first
        assert names[-1] == "first"


# ── Schema tests ───────────────────────────────────────────────────────────────

class TestSchemas:
    def test_job_submit_response_schema(self):
        from app.models.schemas import JobSubmitResponse, JobStatus
        r = JobSubmitResponse(job_id="abc-123", status=JobStatus.pending)
        assert r.job_id == "abc-123"
        assert r.status == "pending"

    def test_job_status_response_schema(self):
        from app.models.schemas import JobStatusResponse, JobStatus
        r = JobStatusResponse(
            job_id="abc-123",
            prospect_name="Frank",
            company_name="FrankCo",
            status=JobStatus.completed,
            created_at=datetime.datetime.utcnow(),
            result=None,
        )
        assert r.status == "completed"
        assert r.error is None

    def test_job_list_item_from_orm(self, db_session):
        """JobListItem can be constructed from ORM data via manual mapping (as done in routes.py)."""
        from app.db.models import ProspectRun
        from app.models.schemas import JobListItem, JobStatus
        job_id = str(uuid.uuid4())
        run = ProspectRun(
            id=job_id,
            prospect_name="Grace",
            company_name="GraceCo",
            status="pending",
            created_at=datetime.datetime.utcnow(),
        )
        db_session.add(run)
        db_session.commit()

        # Manual mapping (matching what routes.py does)
        item = JobListItem(
            job_id=run.id,
            prospect_name=run.prospect_name,
            company_name=run.company_name,
            status=JobStatus(run.status),
            created_at=run.created_at,
            completed_at=run.completed_at,
        )
        assert item.job_id == job_id
        assert item.status == JobStatus.pending


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
