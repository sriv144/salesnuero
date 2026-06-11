# Research Log

Living record of automated improvements made by the Auto-Researcher agent.

## 2026-06-11 — Auto-Researcher v4

**Resume score at start of run:** 65 / 100
- Tech prestige (Multi-agent CrewAI + FastAPI + React + TypeScript): 17/25
- Recency (updated 2026-05-11): 18/25
- Feature completeness (B2B buyer psychology + outreach platform): 13/20
- Stars (1): 4/15
- README quality: 13/15

### Implemented on `claude/compassionate-keller-07c8b9`
- **docs: seed RESEARCH_LOG** — establishes the auto-researcher's running memory for this repo. No code changes shipped this run.

### Why not implemented this run
- Token budget went to the higher-scoring repos (AegisQuant, embodied-skill-composer, Autonomous-SRE-Agent).
- salesnuero has a frontend + backend split which complicates atomic improvements; safer to wait until a focused session that can verify both halves still build.

### Evaluated and skipped
- **Add CI workflow** — needs separate jobs for the React frontend and the FastAPI backend; not safely atomicizable without reading the build configs more carefully.
- **Migrating CrewAI agents to use Anthropic Claude** — multi-agent rewrites are high blast radius without integration tests.

### Next-run candidates
- CI workflow with a TypeScript build matrix (frontend) and a Python pytest job (backend), each isolated so the FE/BE breakage is clearly attributable.
- README screenshot/GIF of the React frontend driving a sample outreach flow.
- Anthropic Claude as the default LLM for the CrewAI agents with an A/B harness.
- A small "buyer psychology" eval set (10 prospects, expected angles) reported in the README to make the AI claim concrete.
- Rate limiting on the FastAPI endpoints called by the React frontend.
