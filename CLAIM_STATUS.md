# RealityOS claim status

**Classification:** RESEARCH (not promoted)
**Claim cap:** ≤ 1 (local MVP heuristic) / **RUNNABLE SKETCH**
**Governing source:** beyond-repair/ADL-Governance
**Sweep-274:** 2026-10-07. Selection seed `random.Random(20261007*1000+273).choice` on the sorted 83-name search payload. Index 31. Subject `RealityOS`. Sweep id is 274 because Sweep-273 was already a census commit.

| Claim | State |
|-------|--------|
| In-memory SimulationEngine fidelity steps, price/hire/supplier heuristics | VERIFIED by local pytest in `backend/tests/test_simulation_engine.py` |
| FastAPI flow (create org, source, simulation, scenario, 404) | VERIFIED by the same pytest module via TestClient |
| `python demo.py` | VERIFIED by the demo test; seed 0; printed figures are heuristics |
| Health-score boundary `0.7` uses the smaller fidelity step | VERIFIED by `test_health_score_at_threshold_uses_smaller_step` (Sweep-274) |
| Local pytest on Sweep-274 working tree | 18 passed (Python host this sweep) |
| GitHub Actions `research-guard` on pre-Sweep-274 main `e36664a403c428838ffdeca6d3e5b714ff5dbc9b` | Run 37515961844 conclusion success (2026-10-06). This supersedes the Sweep-250 note that the permissions edit was unobserved. |
| SQLite / SQLAlchemy persistence | ABSENT |
| `backend/app/services/connectors/` | ABSENT |
| Simulation Quality Agent | Stub `evaluate()` only; covered by a unit test; not scheduled |
| Calibrated confidence vs outcomes | NOT CLAIMED |
| Operating system / production autonomy | NOT CLAIMED |

Do not treat older README architecture diagrams or `POLSIA_PROMPT.md` as evidence of connectors or a running company. Do not promote to ACTIVE: no auth, no persistence, heuristic confidence only. A green `research-guard` run is a sketch gate, not a security audit.
