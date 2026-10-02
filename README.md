<div align="center">

```
╔═════════════════════════════════════════════════════════════╗
║   ATOMIC DREAM LABS  ·  BEYOND-REPAIR                        ║
╚═════════════════════════════════════════════════════════════╝
```

# RealityOS

### In-memory what-if API. Heuristic confidence. Not an operating system.

[![Lifecycle](https://img.shields.io/badge/●_RESEARCH-a855f7?style=for-the-badge&labelColor=0f0f23)](https://github.com/beyond-repair/ADL-Governance)
[![Claim](https://img.shields.io/badge/Claim_%E2%89%A41-22c55e?style=for-the-badge&labelColor=0f0f23)](https://github.com/beyond-repair/ADL-Governance/blob/main/docs/CLAIM_VALIDATION.md)
[![Governance](https://img.shields.io/badge/ADL--Governance-7c3aed?style=for-the-badge&labelColor=0f0f23)](https://github.com/beyond-repair/ADL-Governance)

```
LIFECYCLE   RESEARCH
CLAIM       ≤ 1   local MVP heuristic / RUNNABLE SKETCH
NOT CLAIMED production OS · living twin · calibrated forecasts · live connectors · SQLite
```

</div>

---

## What this repository is

RealityOS is a small local API that keeps an **in-memory** sketch of one organization and answers keyword what-if questions (price, hiring, supplier, or a generic fallback). Every prediction is tagged `model_version=mvp-heuristic-0.1`.

It does **not** talk to Salesforce, QuickBooks, or any other system of record. There is no database, no login, and no autonomous company. Restarting the process drops all organizations. `POLSIA_PROMPT.md` is a design prompt, not a running product.

Sibling map, not a successor: `os-family-constitution-map`. No SUPERSEDES label.

## Configure

No environment variables and no database URL. Configuration is the process defaults in code:

| Knob | Value |
| --- | --- |
| Persistence | Process memory only |
| Starting fidelity | `0.05`, status `initializing` |
| Fidelity step | `+0.12` if source `health_score > 0.7`, else `+0.06`, rounded to 2 decimals, cap `0.95` |
| Status `live` | Fidelity **greater than** `0.25` (two healthy sources: `0.29`) |
| Price heuristic | `demand = -0.6 * (percent_change / 10)`; revenue change percent is `percent_change + 100 * demand` |
| Model tag | `mvp-heuristic-0.1` |

Python **3.11+**. Commands below were checked on Python 3.13.

## Install, run, test

```bash
git clone https://github.com/beyond-repair/RealityOS.git
cd RealityOS/backend
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Tests (heuristic engine, scenario service, quality-agent stub, HTTP flow, demo)
python -m pytest -q tests/test_simulation_engine.py

# Same flow as a script (seed 0). Printed dollars and entity counts are not measurements.
python demo.py

# API. Interactive docs at http://127.0.0.1:8000/docs
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Use the API (another shell, with the server running):

```bash
ORG=$(curl -s -X POST http://127.0.0.1:8000/v1/organizations \
  -H 'content-type: application/json' \
  -d '{"name":"Acme Industrial","industry":"Manufacturing"}' | python3 -c 'import json,sys; print(json.load(sys.stdin)["id"])')

curl -s -X POST "http://127.0.0.1:8000/v1/organizations/$ORG/data-sources" \
  -H 'content-type: application/json' \
  -d '{"type":"crm","name":"Salesforce Production","health_score":0.88}'

curl -s "http://127.0.0.1:8000/v1/organizations/$ORG/simulation"

curl -s -X POST "http://127.0.0.1:8000/v1/organizations/$ORG/scenarios" \
  -H 'content-type: application/json' \
  -d '{"question":"What happens if we raise prices 7%?","parameters":{"percent_change":7}}'
```

A 7% price question returns `revenue_change_pct` of **-35.0** and `customer_churn_delta_pct` of **16.8**. That is the elasticity sketch above, not a measured market outcome. One healthy source leaves fidelity at **0.17** and status **initializing**.

## HTTP surface

| Method | Path | Behavior |
| --- | --- | --- |
| GET | `/` | Name, version, `persistence=in-memory`, model tag |
| GET | `/health` | `{"status":"ok"}` |
| GET | `/docs` | OpenAPI UI |
| POST | `/v1/organizations` | Create org and an empty simulation |
| GET | `/v1/organizations/{id}` | 404 if missing |
| POST | `/v1/organizations/{id}/data-sources` | Record a labeled source and raise fidelity. `connector_config` is stored and ignored |
| GET | `/v1/organizations/{id}/data-sources` | List sources |
| GET | `/v1/organizations/{id}/simulation` | Current sketch |
| POST | `/v1/organizations/{id}/simulation/advance` | Multiply existing metrics by a random drift in `[-3%, +4%]` |
| POST | `/v1/organizations/{id}/scenarios` | Keyword heuristic prediction |
| GET | `/v1/organizations/{id}/predictions` | Predictions stored in this process |

`backend/app/agents/simulation_quality.py` only recommends connecting a source when fidelity is low. It does not run on a schedule.

## Layout

```
backend/
├── app/
│   ├── main.py            # FastAPI entry
│   ├── models/domain.py   # Pydantic records
│   ├── services/
│   │   ├── simulation.py  # In-memory engine
│   │   └── scenario.py    # Stores Prediction objects
│   ├── api/routes.py
│   └── agents/simulation_quality.py
├── demo.py
├── requirements.txt
└── tests/test_simulation_engine.py
```

There is no `connectors/` package. Declared-but-unused SQLAlchemy, Alembic, python-jose, and passlib dependencies were removed so install matches the code.

## Not claimed

- An operating system, a living organization, or production autonomy
- Calibrated confidence or outcome feedback
- OAuth or any real connector
- Multi-tenant auth
- SQLite or any other persistence
- A passed GitHub Actions run (the existing `research-guard` workflow is unchanged and was not treated as evidence)

## License

Proprietary. All rights reserved.

---

<div align="center">

**REWRITE · BUILD · TRANSCEND**

**William (Brian) Ware** · [Atomic Dream Labs](https://github.com/beyond-repair)  
Governing source: [ADL-Governance](https://github.com/beyond-repair/ADL-Governance) · [Claim levels 0–5](https://github.com/beyond-repair/ADL-Governance/blob/main/docs/CLAIM_VALIDATION.md)

</div>
