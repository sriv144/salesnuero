# Research Log — Salesnuero

Durable memory for the auto-researcher agent. Each run appends an entry
documenting what was implemented, what was deliberately skipped, and the
next viable improvement. Do not delete prior entries.

Note: this repository's default branch is `master`, not `main`. All
auto-researcher branches MUST be created from `master`.

---

## 2026-05-23 — Auto-Researcher v4

**Resume score at start of run:** 65 / 100

**Implemented on branch `claude/compassionate-keller-dmZJS`:** none this
run (this seed entry only).

**Why this repo was deprioritized:** Salesnuero is the FastAPI + React +
CrewAI B2B outreach platform. It's a legitimate full-stack AI project,
but its tech-stack prestige is lower than the RL/robotics/SRE
portfolio repos and there is no `tests/` directory at the repo root nor
a visible `.env.example`. With a bounded token budget, the top three
repos were the higher-leverage targets this run.

**Evaluated and skipped this run:**
- *Adding a CI workflow.* Skipped because the repo lacks a `tests/`
  directory, so a pytest-only CI would have nothing to run. A useful
  CI would also need to compile the React frontend.
- *Seeding `.env.example`.* Tractable but requires reading
  `backend/` to enumerate the real env vars (OpenAI / Anthropic key,
  database URL, JWT secret, etc.) without leaking secrets.
- *Switching LLM provider to Anthropic Claude.* Real feature work.
  CrewAI supports multiple model backends — worth doing in a
  scoped PR.

**Next-run candidates (in priority order):**
1. Audit `backend/` for env-var usage and seed a clean `.env.example`.
2. Add a `tests/` directory with smoke tests against the FastAPI app.
3. Add a GitHub Actions workflow that lints the backend with ruff,
   runs pytest, and builds the React frontend (`npm ci && npm run build`).
4. Add Anthropic Claude as the primary LLM behind a feature flag.
