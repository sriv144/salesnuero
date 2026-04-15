"""
SQLAlchemy ORM models for SalesNeuro persistence.
"""
import uuid
import datetime
from typing import Optional
from sqlalchemy import String, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base


class ProspectRun(Base):
    """Persists the result of a prospect pipeline execution."""

    __tablename__ = "prospect_runs"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    prospect_name: Mapped[str] = mapped_column(String(256), nullable=False, index=True)
    company_name: Mapped[str] = mapped_column(String(256), nullable=False, index=True)

    # "pending" | "running" | "completed" | "failed"
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.datetime.utcnow
    )
    completed_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)

    # Pipeline output fields (populated when status == "completed")
    research_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    profile_raw: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    strategy_brief: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    emails_raw: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    raw_crew_output: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Error details (populated when status == "failed")
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return (
            f"<ProspectRun id={self.id!r} prospect={self.prospect_name!r} "
            f"status={self.status!r}>"
        )
