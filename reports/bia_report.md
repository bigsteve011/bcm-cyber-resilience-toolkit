# Business Impact Analysis & Recovery Gap Report — 2026-09-30

## 1. Recovery Requirements

| Process | Owner | Peak impact | MTPD | RTO | RPO | Tier | Achievable recovery | Gap? |
|---|---|---|---|---|---|---|---|---|
| Online & mobile banking | Head of Digital | 5/5 | 8h | 4h | 60min | Tier 1 | 8h | 🔴 YES |
| Payments processing | Head of Payments | 5/5 | 8h | 4h | 15min | Tier 1 | 6h | 🔴 YES |
| Treasury & liquidity reporting | Treasurer | 5/5 | 24h | 8h | 60min | Tier 2 | 10h | 🔴 YES |
| Customer onboarding (KYC) | Head of Operations | 3/5 | 336h | 168h | 240min | Tier 3 | 12h | 🟢 No |
| Payroll | HR Director | 3/5 | 336h | 168h | 1440min | Tier 3 | 48h | 🔴 YES |

## 2. Recovery Gaps

### Online & mobile banking (Tier 1, RTO 4h)
- mobile-backend: no immutable/isolated backup for Tier 1 process
- core-banking: RTO 6h exceeds required 4h
- crm: RTO 8h exceeds required 4h

### Payments processing (Tier 1, RTO 4h)
- core-banking: RTO 6h exceeds required 4h

### Treasury & liquidity reporting (Tier 2, RTO 8h)
- treasury-system: RTO 10h exceeds required 8h
- treasury-system: RPO 240min exceeds tolerance 60min
- treasury-system: DR test older than 12 months
- treasury-system: last DR test FAILED

### Payroll (Tier 3, RTO 168h)
- hr-cloud: never DR tested

## 3. Single Points of Failure (dependencies shared by ≥ 2 processes)

| Dependency | Processes | Strictest RTO needed |
|---|---|---|
| core-banking | Payments processing, Online & mobile banking, Treasury & liquidity reporting | 4h |
| hypercloud-eu | Payments processing, Online & mobile banking | 4h |
| crm | Online & mobile banking, Customer onboarding (KYC) | 4h |

