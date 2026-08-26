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
