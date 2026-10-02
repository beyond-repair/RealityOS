# RealityOS — Governance Lock (Sweep-187)

**Classification:** RESEARCH  
**Head (pre-sweep-187):** `c06f94f6d96b01fe3cd69224ece7447f7944a28b`  
**Governing source:** `beyond-repair/ADL-Governance`  
**Prior lock:** Sweep-119 (2026-09-08)  
**This lock:** 2026-10-01

## Claim contract

This repository is an **MVP scaffold** for an organizational simulation API. It is **not** an operating system, not a verified digital twin of any real organization, and not a production decision engine.

| Claim | State |
|-------|--------|
| FastAPI entrypoint + domain Pydantic models | VERIFIED (tree) |
| Simulation / scenario service modules present | VERIFIED (tree) |
| SimulationEngine create, fidelity cap, price heuristic | VERIFIED (local pytest, Sweep-187; 4 passed) |
| Simulation Quality Agent | STUB only (`backend/app/agents/simulation_quality.py`) |
| Unit tests | PRESENT (`backend/tests/test_simulation_engine.py`) |
| Product CI | ADDED (`.github/workflows/research-guard.yml`); remote conclusion not yet recorded in this file |
| GitHub Releases / tags | none (not created this sweep) |
| Real OAuth connectors | ABSENT (`connectors/` not in tree) |
| Calibrated confidence scoring vs empirical outcomes | UNVERIFIED |
| Multi-tenant isolation / auth | PLANNED |
| Living simulation of a real organization | UNVERIFIED |

## Code-review readiness

**FAIL** for ACTIVE promotion: CI remote result not yet a release gate, no auth, no connectors, heuristic confidence only.

## Do not claim

- RealityOS is a shipped OS or production autonomy layer.
- Predictions are empirically calibrated.
- Agent autonomy is implemented beyond stubs.
- Connectors exist because the README diagram names them.

## Repair note (2026-10-02)

The Sweep-187 lock above still describes the tree as it was. A later repair corrected three facts without promoting the lifecycle:

- Persistence is in-memory. SQLAlchemy and Alembic were requirements only and were removed.
- Confidence strings no longer say the scores are calibrated.
- Local pytest covers the engine, the scenario service, the quality-agent stub, the HTTP routes, and `demo.py`. That is not a remote CI result and not a claim-level promotion.
