<div align="center">

```
╔═════════════════════════════════════════════════════════════╗
║   ATOMIC DREAM LABS  ·  BEYOND-REPAIR                        ║
╚═════════════════════════════════════════════════════════════╝
```

# RealityOS

### MVP decision-infrastructure simulation. Stubs are not live adapters.

[![Lifecycle](https://img.shields.io/badge/●_RESEARCH-a855f7?style=for-the-badge&labelColor=0f0f23)](https://github.com/beyond-repair/ADL-Governance)
[![Claim](https://img.shields.io/badge/Claim_%E2%89%A41-22c55e?style=for-the-badge&labelColor=0f0f23)](https://github.com/beyond-repair/ADL-Governance/blob/main/docs/CLAIM_VALIDATION.md)
[![Governance](https://img.shields.io/badge/ADL--Governance-7c3aed?style=for-the-badge&labelColor=0f0f23)](https://github.com/beyond-repair/ADL-Governance)

```
LIFECYCLE   RESEARCH
CLAIM       ≤ 1   local MVP heuristic
NOT CLAIMED production OS autonomy
```

</div>

---
## ▌ STATUS

Classification follows [ADL-Governance](https://github.com/beyond-repair/ADL-Governance). Sweep-187 reconfirmed RESEARCH. A README facelift does not raise claim level. CI green is not experimental validation.

Sweep-187 corrections against the preserved body below:

- `backend/app/services/connectors/` is **not** in the tree. Connector bullets and the architecture diagram are planned, not implemented.
- Confidence scores are heuristic (`model_version=mvp-heuristic-0.1`), not empirically calibrated.
- Tests now exist at `backend/tests/test_simulation_engine.py` (4 local cases). They do not prove a living twin.
- SQLite models are present; persistence was not integration-tested this sweep.
- Sibling map, not a successor: `os-family-constitution-map`. No SUPERSEDES label applied.

---

## ▌ PRESERVED BODY

# RealityOS

**Autonomous Decision Infrastructure**

RealityOS builds and maintains a living, confidence-scored simulation of an organization. It sits above existing systems of record and answers “What happens if…?” questions before decisions are made.

This repository contains the actual product codebase (MVP foundation).

## Current Status (MVP v0.1)

- Core domain models (Organization, DataSource, Simulation, Scenario, Prediction)
- Lightweight simulation engine with confidence scoring
- Progressive data source connectors (stubs ready for real integrations)
- Scenario query API
- FastAPI backend with automatic OpenAPI docs
- SQLite persistence for local development
- Agent scaffolding for future autonomous operation

## Quick Start

```bash
# Clone
git clone https://github.com/beyond-repair/RealityOS.git
cd RealityOS

# Backend
cd backend
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt pytest

# Run API
uvicorn app.main:app --reload

# Claim-capped tests
python -m pytest -q tests/test_simulation_engine.py
```

Open http://localhost:8000/docs for interactive API documentation.

## Architecture Overview

```
backend/
├── app/
│   ├── main.py                 # FastAPI entrypoint
│   ├── models/                 # Domain models (Pydantic)
│   ├── services/
│   │   ├── simulation.py       # Living simulation engine (in-memory heuristic)
│   │   └── scenario.py         # Scenario evaluation & prediction
│   ├── api/                    # Route handlers
│   └── agents/                 # Autonomous agent stubs
├── requirements.txt
└── tests/                     # Sweep-187 heuristic tests
```

`connectors/` is not present.

## Design Principles (Enforced in Code)

1. Progressive value – start with minimal connectors, deepen automatically
2. Confidence-first – every prediction carries explicit uncertainty (heuristic, not calibrated)
3. Auditability – provenance dict on scenario estimates
4. Autonomy-ready – services designed to be driven by agents with minimal human input
5. Network-effect oriented – models structured to accumulate cross-organization patterns

## Next Milestones

- [ ] Real OAuth connectors (Salesforce, HubSpot, QuickBooks, Slack)
- [ ] Outcome feedback loop (actual vs predicted)
- [ ] Multi-tenant isolation + basic auth
- [ ] Frontend dashboard for executives
- [ ] First autonomous agent (Simulation Quality Agent)

## License

Proprietary. All rights reserved.

---

<div align="center">

**REWRITE · BUILD · TRANSCEND**

**William (Brian) Ware** · [Atomic Dream Labs](https://github.com/beyond-repair)  
Governing source: [ADL-Governance](https://github.com/beyond-repair/ADL-Governance) · [Claim levels 0–5](https://github.com/beyond-repair/ADL-Governance/blob/main/docs/CLAIM_VALIDATION.md)

</div>
