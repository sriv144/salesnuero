# Research Log

This log tracks automated research and improvement runs by the
auto-researcher agent.

---

## 2026-05-13 — Auto-Researcher v4

**Resume score at start of run:** 70 / 100
- Tech stack prestige: 17/25 (FastAPI + CrewAI + React/TypeScript)
- Commit recency: 25/25 (active within the last 48 hours)
- Feature completeness: 14/20
- Stars + visibility: 4/15
- README quality: 10/15

**Note:** This repo's default branch is `master`, not `main`.

**Implemented (branch: `claude/compassionate-keller-HHSYf`):**
- `RESEARCH_LOG.md` (this file) so future runs can avoid duplicate work.

**Why no code changes this run:**
- Token budget was spent on the top 3 by resume score
  (embodied-skill-composer, AegisQuant, Autonomous-SRE-Agent).
- A safe one-commit win on salesnuero would touch both the FastAPI
  backend and the React frontend, which is too broad to land cleanly
  in a single atomic commit; deferred to a focused next run.

**Next-run candidates (ranked):**
1. Add `.github/workflows/ci.yml` with a backend pytest job and a
   frontend `npm ci && npm run build` job.
2. Replace any OpenAI-only CrewAI agent path with an Anthropic Claude
   option, gated on `ANTHROPIC_API_KEY`.
3. README overhaul: hero screenshot of the React UI + a sample
   buyer-psychology output.
4. Add a Dockerfile + docker-compose for one-command local boot.
5. Wire a rate-limit middleware on the FastAPI outreach endpoint to
   prevent accidental burst sends in dev.
