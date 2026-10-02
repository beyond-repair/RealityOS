# RealityOS claim status

**Classification:** RESEARCH (not promoted)  
**Claim cap:** ≤ 1 (local MVP heuristic)  
**Governing source:** beyond-repair/ADL-Governance

| Claim | State |
|-------|--------|
| In-memory SimulationEngine fidelity steps, price/hire/supplier heuristics | VERIFIED by local pytest in `backend/tests/test_simulation_engine.py` |
| FastAPI flow (create org, source, simulation, scenario, 404) | VERIFIED by the same pytest module via TestClient |
| `python demo.py` | VERIFIED locally; seed 0; printed figures are heuristics |
| SQLite / SQLAlchemy persistence | ABSENT. Those dependencies were declared and unused, then removed |
| `backend/app/services/connectors/` | ABSENT |
| Simulation Quality Agent | Stub `evaluate()` only; covered by a unit test; not scheduled |
| Calibrated confidence vs outcomes | NOT CLAIMED |
| Operating system / production autonomy | NOT CLAIMED |
| GitHub Actions `research-guard` | Present and not modified by the repair; a green local pytest is not an Actions result |

Do not treat older README architecture diagrams or `POLSIA_PROMPT.md` as evidence of connectors or a running company.
