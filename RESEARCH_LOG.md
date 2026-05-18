# Research Log

A running log of autonomous research-and-development cycles on salesnuero.

> Note: this repo's default branch is `master`, not `main`. All `claude/*`
> branches in this repo are cut from `master`.

---

## 2026-05-18 — Auto-Researcher v4

**Resume score at start of run:** 49/100
**Branch:** `claude/compassionate-keller-9dHiZ` (cut from `master`)
**Status:** Evaluated, no code change shipped this cycle.

### Why skipped this cycle
- `master` has only a handful of commits dated 2026-04-01, all in the project's
  initial release window. No recent contributor signal to anchor a change to.
- Stack (CrewAI + FastAPI + React) is interesting for resume optics but the
  CrewAI agent definitions are LLM-coupled in non-trivial ways; a clean migration
  to Claude needs a careful read of the agents/ and crew configurations first.
- Budget went to the top three (AegisQuant polish, SRE → Claude migration,
  embodied-skill-composer CI + LICENSE + CITATION).

### Candidates evaluated
- **CrewAI → Claude backend** — highest resume return on this repo; deferred
  until the agent definitions are read and a per-agent migration plan exists.
- **Frontend polish + screenshots** — worth doing for a sales-tech showcase;
  deferred.
- **CI workflow (pytest + ruff + frontend build)** — the safest single ship;
  deferred only because budget went to the top three.

### Next-run candidates
1. Read `backend/` (FastAPI) + `crew/` (CrewAI definitions), then ship a Claude
   migration with the agent prompts kept verbatim.
2. Add `LICENSE` (MIT), `CITATION.cff`, GitHub issue / PR templates.
3. Add screenshots / a 30-second demo GIF of the React frontend.
4. Add a `docker-compose.yaml` covering backend + frontend + a sample Postgres.
5. Add a CI workflow that runs `pytest` for the backend and `npm run build` for
   the frontend on every push and PR to `master`.
