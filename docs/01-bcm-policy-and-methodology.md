# Business Continuity Management Policy & BIA Methodology

**Standards:** ISO 22301:2019 · ISO/TS 22317 (BIA) · ISO/IEC 27001:2022 A.5.29–A.5.30 · DORA Art. 11–12 · NIST CSF 2.0 RC
**Owner:** Head of Business Continuity · **Approved by:** Executive Committee · **Review:** Annually

## 1. Policy Statements

1. Every business process gets a BIA at least annually and after any significant change.
2. Recovery objectives (MTPD, RTO, RPO) are set by **business owners** based on impact. IT capability does not set them.
3. Every Tier 1 and Tier 2 process has a documented, tested Business Continuity Plan (BCP) and IT Disaster Recovery Plan (DRP).
4. A dependency's demonstrated recovery capability must meet the strictest RTO/RPO of every process that depends on it.
5. Tier 1 processes need immutable or isolated backups that can be restored after a destructive cyberattack.
6. The crisis management team (CMT) runs at least two exercises a year, and one of them must be a cyber scenario.

## 2. BIA Impact Scale

| Score | Financial | Regulatory | Reputational | Customer |
|---|---|---|---|---|
| 1 Negligible | < €10k | None | No external visibility | No noticeable impact |
| 2 Minor | €10k–€100k | Internal breach of policy | Local complaints | < 1% customers affected |
| 3 Moderate | €100k–€1M | Reportable, no sanction likely | Regional media | 1–10% customers |
| 4 Major *(unacceptable)* | €1M–€10M | Regulatory reporting (e.g. DORA major incident), likely findings | National media | 10–30% customers |
| 5 Severe | > €10M | Sanctions, licence risk | International media, sustained | > 30% customers |

## 3. Deriving Recovery Objectives

```
 Impact over time (1h, 4h, 8h, 24h, 72h, 1w) per dimension
             │
             ▼
 MTPD = first window where ANY dimension ≥ 4 (unacceptable)
             │
             ▼
 RTO  = preceding window (safety margin before MTPD)
 RPO  = maximum tolerable data loss stated by the process owner
             │
             ▼
 Tier 1 (RTO ≤ 4h) · Tier 2 (≤ 24h) · Tier 3 (> 24h)
             │
             ▼
 Gap analysis: demonstrated RTO/RPO of each dependency vs requirement
```

This logic is implemented in [`bia_engine.py`](../src/bia_engine.py). Output: [BIA & Recovery Gap Report](../reports/bia_report.md).

## 4. Recovery Strategy Options

| Gap type | Strategy options | Indicative cost |
|---|---|---|
| Application RTO too long | Warm standby, active-active, automated failover runbooks | €€€ |
| RPO too long | Synchronous replication, log shipping, CDC | €€ |
| No isolated backup | Immutable object-lock backup, offline vault, cyber recovery vault | €€ |
| Third-party dependency | Secondary provider, contractual RTO with penalties, tested exit plan | €€ |
| Manual workaround | Documented manual procedures for degraded-mode operation | € |

## 5. Programme Metrics

| Metric | Target |
|---|---|
| Processes with BIA < 12 months old | 100% |
| Tier 1/2 processes with tested BCP | 100% |
| Dependencies meeting required RTO/RPO | ≥ 95% |
| Exercises completed vs plan | 100% |
| Exercise actions closed within due date | ≥ 90% |
