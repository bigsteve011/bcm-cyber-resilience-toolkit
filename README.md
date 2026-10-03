# 🧯 Business Continuity & Cyber Resilience Toolkit

An **ISO 22301 / DORA aligned** business continuity programme that connects **business impact** to **proven recovery capability**.
It includes a Python BIA engine that derives MTPD/RTO/RPO from impact-over-time scoring and flags where IT, SaaS and
third-party recovery capability falls short. It also includes a ransomware tabletop exercise pack ready to run with a crisis management team.

## Why this project

Most BCM programmes set RTOs that IT has never proven it can meet, and they assume failover will work during a
destructive cyberattack. This toolkit makes those assumptions testable: **required vs demonstrated recovery**,
**shared single points of failure**, and a **cyber-specific exercise** that challenges the failover assumption.

## Deliverables

| # | Deliverable | Purpose |
|---|---|---|
| 1 | [BCM Policy & BIA Methodology](docs/01-bcm-policy-and-methodology.md) | Policy statements, 5-point impact scale, MTPD→RTO logic, recovery strategies |
| 2 | [`bia_engine.py`](src/bia_engine.py) | Derives recovery objectives and tiers, finds RTO/RPO, DR-test and immutability gaps, and identifies SPOFs |
| 3 | [BIA input](data/bia_input.csv) · [Recovery capabilities](data/recovery_capabilities.csv) | Sample data for 5 processes and 9 dependencies |
| 4 | [BIA & Recovery Gap Report](reports/bia_report.md) | Generated output |
| 5 | [BCP — Payments Processing](docs/02-bcp-template-payments.md) | Tier 1 plan: activation, roles, timeline, known gaps |
| 6 | [Ransomware Tabletop Exercise](exercises/ransomware-tabletop-exercise.md) | 7 injects, evaluation criteria, after-action report |
| 7 | [Annual Exercise Programme](exercises/exercise-programme.md) | Mix of tabletop, technical DR, exit and live tests |

## Sample output

```
| Process                 | MTPD | RTO | Tier   | Achievable recovery | Gap?   |
| Online & mobile banking | 8h   | 4h  | Tier 1 | 8h                  | 🔴 YES |
| Payments processing     | 8h   | 4h  | Tier 1 | 6h                  | 🔴 YES |

### Treasury & liquidity reporting (Tier 2, RTO 8h)
- treasury-system: RPO 240min exceeds tolerance 60min
- treasury-system: last DR test FAILED

| core-banking | Payments, Online banking, Treasury | Strictest RTO needed: 4h |   ← single point of failure
```

## Quick start

```bash
python3 src/bia_engine.py
python3 -m unittest discover -s tests -v
```

Python 3.10+, standard library only.

## How it connects to my portfolio

- **DORA programme:** feeds Art. 11 BCP/DR testing evidence and the CIF dependency mapping
- **FAIR engine:** the BIA financial impact bands become loss magnitude inputs
- **Enterprise risk tracker:** recovery gaps and exercise actions are tracked to closure

> ⚠️ All organisations, systems and figures are fictitious.
