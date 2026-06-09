# Research Log

This file tracks autonomous improvements made by the Auto-Researcher agent.
Each entry records what was implemented, what was evaluated and skipped,
and candidates queued for the next run, so we never repeat work.

## 2026-06-09 — Auto-Researcher v4

**Resume-worthiness score at start of run:** 65/100

**Branch:** `claude/compassionate-keller-rj6hm9`

### Implemented this run
- `backend/.env.example` — the README tells contributors to `cp .env.example` inside `backend/`, but no such file existed. Added a template with both env vars the README documents (`TAVILY_API_KEY`, `NVIDIA_API_KEY`) plus two commented-out optional overrides. Zero-risk: it is a template, never read by code.
- `RESEARCH_LOG.md` — seeded so future agent runs have memory of what's been tried.

### Why these were prioritized
- The missing `.env.example` is a documented-but-broken contract in the README — exactly the kind of small fix that prevents a recruiter / first-time contributor from bouncing on "file not found."
- Risk is bounded: the file is a template, not loaded at runtime.

### Evaluated and skipped
- CI — no visible tests directory; running compileall alone is cheap polish but doesn't unlock anything meaningful. Better to add it together with a real smoke test.
- README rewrite — current README already has features, prerequisites, backend/frontend split run order, and API docs reference. Hard to improve without churn.
- Adding Docker / docker-compose — high resume value but Next.js + FastAPI + ChromaDB + LiteLLM is non-trivial to glue cleanly; needs a deliberate pass.

### Next-run candidates (priority order)
1. **Add a `Makefile` or `docker-compose.yml`** that brings up backend + frontend + Chroma in one command — the README currently requires two terminals plus a manual `ingest_rag.py`.
2. **Add a smoke test + CI**: one pytest that imports `app.main` and one that imports `ingest_rag` would gate accidental import breakage.
3. **Showcase enhancement**: embed a short demo GIF (CrewAI agent finishing one prospect) in the README to convert browsers into stars.
4. **Claude integration**: SalesNeuro routes through NVIDIA NIM today; offering an Anthropic Claude provider through LiteLLM is a small change with strong resume signal.
5. **`/api/run` response schema**: document the response shape so the Swagger UI link in the README has more to demo.
