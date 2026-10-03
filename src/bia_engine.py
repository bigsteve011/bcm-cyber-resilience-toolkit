"""
Business Impact Analysis (BIA) & Recovery Gap Engine
====================================================

ISO 22301:2019 cl. 8.2.2 / ISO 22317 aligned BIA:

1. Impact-over-time scoring (1 = negligible ... 5 = severe) per process across
   financial, regulatory, reputational and customer dimensions.
2. MTPD (Maximum Tolerable Period of Disruption) = first time window at which
   ANY dimension reaches the "unacceptable" level (score >= 4).
3. RTO = the time window before MTPD, which leaves a safety margin to resume
   before impact becomes unacceptable. RPO = the process's data loss tolerance.
4. Recovery gap analysis: the slowest dependency (application, SaaS, third
   party) sets the achievable recovery time. A dependency fails if its
   demonstrated RTO/RPO exceeds the process requirement, if its last DR test is
   older than 12 months or failed, or if it has no ransomware-isolated backup
   for a Tier 1 process.

Usage:
    python src/bia_engine.py
"""

from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WINDOWS = [1, 4, 8, 24, 72, 168]  # hours
UNACCEPTABLE = 4
AS_OF = date(2026, 9, 30)
DR_TEST_MAX_AGE_DAYS = 365


@dataclass
class Process:
    name: str
    owner: str
    impacts: dict[str, list[int]] = field(default_factory=dict)
    rpo_minutes: int = 0
    dependencies: list[str] = field(default_factory=list)

    @property
    def mtpd_hours(self) -> int:
        for i, window in enumerate(WINDOWS):
            if any(scores[i] >= UNACCEPTABLE for scores in self.impacts.values()):
                return window
        return WINDOWS[-1] * 2  # tolerable beyond one week

    @property
    def rto_hours(self) -> float:
        mtpd = self.mtpd_hours
        earlier = [w for w in WINDOWS if w < mtpd]
        return earlier[-1] if earlier else mtpd / 2

    @property
    def tier(self) -> str:
        rto = self.rto_hours
        return "Tier 1" if rto <= 4 else "Tier 2" if rto <= 24 else "Tier 3"

    @property
    def peak_impact(self) -> int:
        return max(max(s) for s in self.impacts.values())


def load_bia(path: Path = ROOT / "data" / "bia_input.csv") -> list[Process]:
    procs: dict[str, Process] = {}
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            p = procs.setdefault(row["process"], Process(row["process"], row["owner"]))
            p.impacts[row["dimension"]] = [int(row[f"{w}h"]) for w in WINDOWS]
            p.rpo_minutes = int(row["data_loss_tolerance_min"])
            if row["dependencies"]:
                p.dependencies = row["dependencies"].split(";")
    return list(procs.values())


def load_capabilities(path: Path = ROOT / "data" / "recovery_capabilities.csv") -> dict[str, dict]:
    with open(path, newline="", encoding="utf-8") as fh:
        return {r["dependency"]: r for r in csv.DictReader(fh)}


def gaps(process: Process, caps: dict[str, dict]) -> list[str]:
    issues = []
    for dep in process.dependencies:
        cap = caps.get(dep)
        if cap is None:
            issues.append(f"{dep}: no recovery capability documented")
            continue
        if float(cap["demonstrated_rto_hours"]) > process.rto_hours:
            issues.append(f"{dep}: RTO {cap['demonstrated_rto_hours']}h exceeds required {process.rto_hours}h")
        if int(cap["demonstrated_rpo_minutes"]) > process.rpo_minutes:
            issues.append(f"{dep}: RPO {cap['demonstrated_rpo_minutes']}min exceeds tolerance {process.rpo_minutes}min")
        if not cap["last_dr_test"]:
            issues.append(f"{dep}: never DR tested")
        else:
            if (AS_OF - date.fromisoformat(cap["last_dr_test"])).days > DR_TEST_MAX_AGE_DAYS:
                issues.append(f"{dep}: DR test older than 12 months")
            if cap["dr_test_result"] == "fail":
                issues.append(f"{dep}: last DR test FAILED")
        if process.tier == "Tier 1" and cap["ransomware_isolated_backup"] != "yes":
            issues.append(f"{dep}: no immutable/isolated backup for Tier 1 process")
    return issues


def achievable_recovery(process: Process, caps: dict[str, dict]) -> float | None:
    values = [float(caps[d]["demonstrated_rto_hours"]) for d in process.dependencies if d in caps]
    return max(values) if values else None


def render(processes: list[Process], caps: dict[str, dict]) -> str:
    lines = [f"# Business Impact Analysis & Recovery Gap Report — {AS_OF}", "",
             "## 1. Recovery Requirements", "",
             "| Process | Owner | Peak impact | MTPD | RTO | RPO | Tier | Achievable recovery | Gap? |",
             "|---|---|---|---|---|---|---|---|---|"]
    ordered = sorted(processes, key=lambda p: (p.rto_hours, p.name))
    for p in ordered:
        ach = achievable_recovery(p, caps)
        gap = "🔴 YES" if gaps(p, caps) else "🟢 No"
        lines.append(f"| {p.name} | {p.owner} | {p.peak_impact}/5 | {p.mtpd_hours}h | {p.rto_hours:g}h | "
                     f"{p.rpo_minutes}min | {p.tier} | {f'{ach:g}h' if ach is not None else 'n/a'} | {gap} |")
    lines += ["", "## 2. Recovery Gaps", ""]
    for p in ordered:
        issues = gaps(p, caps)
        if issues:
            lines.append(f"### {p.name} ({p.tier}, RTO {p.rto_hours:g}h)")
            lines += [f"- {i}" for i in issues] + [""]
    shared = defaultdict(list)
    for p in processes:
        for d in p.dependencies:
            shared[d].append(p.name)
    lines += ["## 3. Single Points of Failure (dependencies shared by ≥ 2 processes)", "",
              "| Dependency | Processes | Strictest RTO needed |", "|---|---|---|"]
    by_name = {p.name: p for p in processes}
    for dep, names in sorted(shared.items(), key=lambda kv: -len(kv[1])):
        if len(names) >= 2:
            lines.append(f"| {dep} | {', '.join(names)} | {min(by_name[n].rto_hours for n in names):g}h |")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    print(render(load_bia(), load_capabilities()))
