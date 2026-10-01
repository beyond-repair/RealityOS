<div align="center">

```
╔══════════════════════════════════════════════════════════════╗
║   ATOMIC DREAM LABS  ·  BEYOND-REPAIR                        ║
╚══════════════════════════════════════════════════════════════╝
```

# RealityOS

### MVP decision-infrastructure simulation. Stubs are not live adapters.

[![Lifecycle](https://img.shields.io/badge/●_RESEARCH-a855f7?style=for-the-badge&labelColor=0f0f23)](https://github.com/beyond-repair/ADL-Governance)
[![Claim](https://img.shields.io/badge/Claim_≤1-22c55e?style=for-the-badge&labelColor=0f0f23)](https://github.com/beyond-repair/ADL-Governance/blob/main/docs/CLAIM_VALIDATION.md)
[![Governance](https://img.shields.io/badge/ADL--Governance-7c3aed?style=for-the-badge&labelColor=0f0f23)](https://github.com/beyond-repair/ADL-Governance)

```
LIFECYCLE   RESEARCH
CLAIM       ≤ 1   local MVP
NOT CLAIMED production OS autonomy
```

</div>

---
## ▌ STATUS

Classification follows [ADL-Governance](https://github.com/beyond-repair/ADL-Governance). A README facelift does not raise claim level. Physics and pharmacology stay at the evidenced cap. CI green is not experimental validation.

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
pip install -r requirements.txt

# Run
uvicorn app.main:app --reload
```

Open http://localhost:8000/docs for interactive API documentation.

## Architecture Overview

```
backend/
├── app/
│   ├── main.py                 # FastAPI entrypoint
│   ├── models/                 # Domain models (Pydantic + SQLAlchemy)
│   ├── services/
│   │   ├── simulation.py       # Living simulation engine
│   │   ├── connectors/         # Progressive data source connectors
│   │   └── scenario.py         # Scenario evaluation & prediction
│   ├── api/                    # Route handlers
│   └── agents/                 # Autonomous agent stubs
├── requirements.txt
└── tests/
```

## Design Principles (Enforced in Code)

1. Progressive value – start with minimal connectors, deepen automatically
2. Confidence-first – every prediction carries calibrated uncertainty
3. Auditability – full provenance on every recommendation
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
