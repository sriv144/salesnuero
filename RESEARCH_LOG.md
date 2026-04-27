# Research Log

This file tracks autonomous research and improvement runs against this
repository.

## 2026-04-27 — Auto-Researcher v4

**Resume score at start of run:** 60 / 100 — ranked 5 of 6 in the portfolio.

**Branch:** `claude/compassionate-keller-snPHW` (off `master`).

### Implemented this run

No code changes. This commit only seeds the research log so future runs have
memory of what was already evaluated.

### Why no implementation this run

SalesNeuro is feature-interesting (CrewAI multi-agent + Big Five / DISC
psychological profiling + Tavily OSINT) but the README is currently the
weakest part of the project relative to its capability. Token budget for this
run was prioritized for repos with clearer, higher-impact one-shot wins.

### Evaluated and parked for next run

- **README depth:** README is short and does not show example outputs. A
  walkthrough with one redacted prospect profile + the resulting cold email
  would dramatically raise the resume signal.
- **`.env.example` at repo root** (in addition to the `backend/` one): the
  current README references `backend/.env` only. A root-level
  `.env.example` would make the secret surface obvious.
- **CI:** TypeScript frontend + Python backend would benefit from a two-job
  GitHub Actions workflow (`npm run build`, `pytest`).
- **Architecture diagram of the CrewAI agent flow:** clear win for an outreach
  / sales tool because reviewers want to see what each agent does.
- **Add a LICENSE.**

### Next-run candidates (priority order)

1. README rewrite with example output (one full prospect profile + email).
2. CI: `npm run build` for frontend + `pytest` for backend.
3. CrewAI agent architecture diagram in README.
4. LICENSE.
