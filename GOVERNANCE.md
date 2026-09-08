# RealityOS — Governance Lock (Sweep-119)

**Classification:** RESEARCH  
**Head (pre-lock):** `a70f5924b65a4f4977ac41e45b0d4cdae414d54a`  
**Governing source:** `beyond-repair/ADL-Governance`  
**Lock date:** 2026-09-08

## Claim contract

This repository is an **MVP scaffold** for an organizational simulation API. It is **not** an operating system, not a verified digital twin of any real organization, and not a production decision engine.

| Claim | State |
|-------|--------|
| FastAPI entrypoint + domain Pydantic/SQLAlchemy models | VERIFIED (tree) |
| Simulation / scenario service modules present | VERIFIED (tree) |
| Simulation Quality Agent | STUB only (`backend/app/agents/simulation_quality.py`) |
| Unit / integration tests | ABSENT (README lists `backend/tests/`; tree has no tests) |
| Product CI (pytest / lint) | ABSENT (only Dependabot graph workflow) |
| GitHub Releases / tags | none |
| Real OAuth connectors (Salesforce, HubSpot, QuickBooks, Slack) | PLANNED (README) |
| Calibrated confidence scoring vs empirical outcomes | UNVERIFIED |
| Multi-tenant isolation / auth | PLANNED |
| Living simulation of a real organization | UNVERIFIED |

## Features

| Feature | State |
|---------|--------|
| FastAPI OpenAPI surface | VERIFIED (code present; runtime not executed this cycle) |
| SQLite local persistence | PARTIAL (models present; not integration-tested this cycle) |
| Demo script `backend/demo.py` | VERIFIED (file present; not executed this cycle) |
| Data source connectors | ABSENT in tree (README architecture lists `connectors/`; no such directory) |
| Frontend dashboard | PLANNED |

## Code-review readiness

**FAIL** for ACTIVE promotion: no product tests, no product CI, README/tree drift, no releases.

## Do not claim

- RealityOS is a shipped OS or production autonomy layer.
- Predictions are empirically calibrated.
- Agent autonomy is implemented beyond stubs.
- Connectors exist because the README diagram names them.
