# Business Continuity Plan — Payments Processing (Tier 1)

| Field | Value |
|---|---|
| Process owner | Head of Payments |
| MTPD / RTO / RPO | 8h / 4h / 15 min (from BIA 2026-09-30) |
| Critical dependencies | payments-app, core-banking, HyperCloud EU, PaySwitch |
| Alternate site / mode | Secondary cloud region (warm standby); manual high-value payment procedure |
| Plan version / last test | 2.1 / 2026-06-14 |

## 1. Activation Criteria

Activate when **any** of the following applies:
- Payments outage > 30 minutes, or expected to last > 1 hour
- Suspected ransomware or destructive malware on payments infrastructure
- Loss of HyperCloud EU primary region or PaySwitch connectivity
- A DORA major-incident classification involving payments

## 2. Roles

| Role | Primary | Deputy | Responsibilities |
|---|---|---|---|
| Plan owner | Head of Payments | Payments Ops Manager | Activate the plan, prioritise payments, approve manual processing |
| IT recovery lead | Head of Infrastructure | Cloud Lead | Execute the DRP and failover |
| Security lead | CISO | SOC Manager | Containment, forensics, clean-environment validation |
| Comms lead | Head of Comms | Comms Manager | Customer, media and regulator messaging (with Compliance) |
| Compliance | Head of Compliance | Compliance Officer | DORA/PSD2 reporting, regulator liaison |

## 3. Recovery Procedure (Timeline)

| T+ | Action | Owner |
|---|---|---|
| 0–30 min | Detect, assess, convene the incident bridge, decide on activation | Plan owner |
| 30–60 min | Notify the CMT; start DORA classification; prioritise payments (salaries, high-value, CLS) | Plan owner / Compliance |
| 1–2 h | Fail over to the secondary region (if not a cyber event) **or** isolate and validate clean backups (if cyber) | IT recovery lead / CISO |
| 1–4 h | Manual processing of high-value and critical payments using the dual-control procedure | Payments Ops |
| ≤ 4 h | Restore the service (RTO); reconcile transactions to the last good point (RPO 15 min) | IT recovery lead |
| 4–8 h | Clear backlog; send customer communications; submit initial regulator notification | Payments Ops / Comms |
| Post | PIR within 10 working days; update BIA, BCP and the risk register | Plan owner |

## 4. Known Gaps (from BIA)

- core-banking demonstrated RTO is 6h against a required 4h. **Interim workaround:** manual payment release using the core-banking read-only replica, with a target architecture change in Q2.
