"""SQLite database for run history persistence."""
import sqlite3
import json
import os
from typing import Optional, List
from app.models.schemas import RunResult

# Database path: backend/data/run_history.db
DB_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "run_history.db"
)


def _ensure_db():
    """Create database and schema if they don't exist."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            id TEXT PRIMARY KEY,
            prospect_name TEXT NOT NULL,
            company_name TEXT NOT NULL,
            created_at TEXT NOT NULL,
            research_summary TEXT,
            profile_raw TEXT,
            strategy_brief TEXT,
            emails_raw TEXT,
            status TEXT DEFAULT 'success',
            full_result TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_run(run_result: RunResult) -> bool:
    """
    Save a run result to the database.
    Returns True on success, False on failure.
    """
    try:
        _ensure_db()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Store the full result as JSON for later retrieval
        full_result_json = json.dumps(run_result.model_dump())

        cursor.execute("""
            INSERT INTO runs (
                id, prospect_name, company_name, created_at,
                research_summary, profile_raw, strategy_brief, emails_raw,
                status, full_result
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            run_result.run_id,
            run_result.prospect_name,
            run_result.company_name,
            run_result.created_at,
            run_result.research_summary,
            run_result.profile_raw,
            run_result.strategy_brief,
            run_result.emails_raw,
            "success",
            full_result_json,
        ))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving run to database: {e}")
        return False


def list_runs(limit: int = 50) -> List[dict]:
    """
    List all runs with basic metadata.
    Returns a list of dicts with: id, prospect_name, company_name, created_at, status.
    Returns empty list if DB doesn't exist yet.
    """
    try:
        if not os.path.exists(DB_PATH):
            return []

        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, prospect_name, company_name, created_at, status
            FROM runs
            ORDER BY created_at DESC
            LIMIT ?
        """, (limit,))

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]
    except Exception as e:
        print(f"Error listing runs from database: {e}")
        return []


def get_run(run_id: str) -> Optional[RunResult]:
    """
    Retrieve a full run result by ID.
    Returns RunResult object or None if not found.
    """
    try:
        if not os.path.exists(DB_PATH):
            return None

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT full_result FROM runs WHERE id = ?
        """, (run_id,))

        row = cursor.fetchone()
        conn.close()

        if row and row[0]:
            result_dict = json.loads(row[0])
            return RunResult(**result_dict)
        return None
    except Exception as e:
        print(f"Error retrieving run from database: {e}")
        return None
