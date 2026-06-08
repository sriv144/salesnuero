# Research Log

Maintained by the Auto-Researcher passes. Each entry records what was looked
at, what was implemented, and what was deferred so future runs do not redo
the same work.

Note: the default branch on this repo is `master`, not `main`. Any CI
workflow added in a future pass must wire `branches: [master]` triggers.

## 2026-06-08 — Auto-Researcher v4

**Resume-worthiness score (start of run):** ~62 / 100
- Tech stack prestige (25): 19 — FastAPI + CrewAI + React is a credible
  multi-agent + product-grade stack.
- Commit recency (25): 22 — last push 2026-05-11.
- Feature completeness (20): unknown this pass; not opened in depth.
- Stars + visibility (15): 3 — 1 star.
- README quality (15): unknown this pass.

**Implemented on branch `claude/compassionate-keller-fX5uP`:**
- `RESEARCH_LOG.md` — this file. Recorded so the next pass starts with
  context instead of re-deriving the priority call.

**Why this pass did not ship code here:**
The top three repos absorbed this run's safe-change budget. salesnuero is a
TypeScript + Python project with a React frontend, which makes safe additive
changes (Mermaid diagrams, CI) a bit more involved than the Python-only
repos — the CI workflow needs both Node and Python jobs. Worth doing
properly in a focused pass rather than rushed in this one.

**Next-run candidates (in priority order):**
1. Add `.github/workflows/ci.yml` with **two** jobs:
   - Python: ruff + py_compile against the FastAPI / CrewAI backend.
   - Node: `npm ci && npm run build` against the React frontend.
   Triggers must use `branches: [master]`.
2. Audit CrewAI agent definitions and ensure the LLM calls target Claude
   (`claude-opus-4-8` for orchestration, `claude-sonnet-4-6` for fan-out
   tasks) with prompt caching where appropriate.
3. Add `SECURITY.md` covering `.env` hygiene, customer-data handling, and
   outbound-rate-limit etiquette for any prospecting / scraping flows.
4. Add a Mermaid sequence diagram of the buyer-psychology flow (lead in →
   CrewAI agents → personalized outreach generation) to the README so the
   multi-agent story renders visually.
5. If the README does not already, add a screenshot of the React frontend.
