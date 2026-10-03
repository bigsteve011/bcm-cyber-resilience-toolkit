# Tabletop Exercise: "Operation Frozen Ledger" — Ransomware on Core Banking

| Item | Detail |
|---|---|
| Format | Facilitated discussion-based tabletop, 3 hours |
| Audience | Crisis Management Team (CEO, CRO, CIO, CISO, CFO, Head of Payments, Comms, Legal, Compliance, DPO) |
| Standards exercised | ISO 22301 cl. 8.5, DORA Art. 11(6) & 13, NIST CSF 2.0 RS/RC, GDPR Art. 33–34 |
| Facilitator | Stephen Omowumi (GRC) · Scribe: BCM Analyst · Observer: Internal Audit |

## 1. Objectives

1. Test whether the CMT can make timely decisions with incomplete information.
2. Validate the DORA major-incident classification and the 4h/24h reporting path.
3. Test the decision on whether to pay a ransom, along with cyber insurer and law enforcement engagement.
4. Validate GDPR breach notification decision-making (72h).
5. Check whether the Payments BCP works when **failover is not possible** (the replica is encrypted too).

## 2. Ground Rules

No-fault environment · Decisions over perfect answers · Use real plans and contact lists · Parking lot for side issues · "Exercise, exercise, exercise" on all communications.

## 3. Scenario & Injects

| # | Time (scenario) | Inject | Key questions | Expected response / plan reference |
|---|---|---|---|---|
| 1 | Sat 02:10 | SOC sees mass file renames on core-banking servers. EDR flags encryption on 40 hosts. | Who is woken up? Who decides on isolation? | SOC runbook → CISO → isolate segment; incident bridge opened |
| 2 | Sat 03:00 | Ransom note: 30 BTC, 72h deadline, claims 2 TB of customer data exfiltrated. | Is this a DORA major incident? GDPR breach? Who decides? | Classify with RTS criteria (critical services + malicious access) → **major**; initial notification due ≤ 4h after classification |
| 3 | Sat 05:30 | Secondary region replica is also encrypted, so failover is impossible. | What now? What is the manual workaround for payments? | Payments BCP §3, manual high-value procedure; restore from immutable backups |
| 4 | Sat 08:00 | Journalist calls: "Customers say they can't pay. Are you hacked?" | Holding statement? Who approves it? | Comms plan; pre-approved holding statement; Legal review |
| 5 | Sat 11:00 | Cyber insurer asks you to engage their panel IR firm. Threat actor is on a sanctions list. | Can we pay? Who decides? | Board-level decision; sanctions screening makes payment unlawful; law enforcement notified |
| 6 | Sat 18:00 | Immutable backups validated clean, but restore takes 22h. Payday is Monday. | Prioritisation? Customer communication? DORA intermediate report? | Restore priority by BIA tier; salary payments via manual process; intermediate report ≤ 72h |
| 7 | Mon 09:00 | Leak site publishes a 1,000-record sample of customer data. | Notify data subjects? Regulator follow-up? | GDPR Art. 34 high-risk test → notify; DPO leads; update DORA report |

## 4. Evaluation Criteria (scored 1–5 by observers)

| Capability | Criteria |
|---|---|
| Detection & escalation | CMT convened within 60 min; clear incident commander |
| Decision-making | Decisions recorded with rationale; escalation thresholds respected |
| Regulatory | DORA classification correct; reporting timelines met; GDPR 72h assessed |
| Recovery | BIA tiers used for restore priority; manual workarounds understood |
| Communication | Consistent, timely, approved internal and external messages |
| Third parties | Cloud provider, insurer, IR retainer and law enforcement engaged correctly |

## 5. After-Action Report (Template)

| # | Observation | Type | Root cause | Recommendation | Owner | Due | Risk register ref |
|---|---|---|---|---|---|---|---|
| 1 | Replica encrypted along with primary; failover assumption invalid | Gap | Replication of encrypted data; no logical air gap | Cyber recovery vault with delayed, immutable copies | CIO | Q2 | R-0412 |
| 2 | 55 minutes to agree who classifies the DORA incident | Gap | RACI not known by CMT | Add classification RACI to the CMT quick card; train | CISO | Q1 | R-0413 |
| 3 | No pre-approved holding statement for cyber incidents | Gap | Comms plan generic | Pre-approve 3 cyber holding statements | Head of Comms | Q1 | — |
| 4 | Sanctions check on ransom payment handled well | Strength | — | Keep | — | — | — |
| 5 | Restore time 22h vs required 4h for Tier 1 | Gap | Restore throughput not tested at scale | Full-scale restore test; parallel restore streams | Head of Infra | Q2 | R-0414 |

**Overall rating:** 🟠 *Partially prepared.* Strong decision-making, but recovery capability doesn't meet Tier 1 RTO in a destructive cyber scenario.
