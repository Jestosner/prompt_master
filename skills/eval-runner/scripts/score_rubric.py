#!/usr/bin/env python3
"""Deterministic rubric scorer, regression detector, and stop-condition verifier.

Usage:
    python score_rubric.py --rubric rubric.json --results v2_results.json [--prev v1_results.json]

rubric.json format:
{
  "weights": {"accuracy": 0.4, "format": 0.3, "conciseness": 0.3},
  "threshold": 4.3
}

results JSON format:
[
  {"case_id": "T1", "hard_fails": [], "scores": {"accuracy": 5, "format": 5, "conciseness": 4}}
]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def score_case(case: dict[str, Any], weights: dict[str, float], threshold: float) -> dict[str, Any]:
    scores = case.get("scores", {})
    hard_fails = case.get("hard_fails", [])
    total = 0.0
    for crit, w in weights.items():
        if crit not in scores:
            raise ValueError(f"Case {case['case_id']} missing criterion score: {crit}")
        total += float(scores[crit]) * float(w)
    total = round(total, 2)
    if hard_fails:
        verdict = "fail"
    elif total >= threshold:
        verdict = "pass"
    elif total >= max(1.0, threshold - 0.5):
        verdict = "revise"
    else:
        verdict = "fail"
    return {
        "case_id": case["case_id"],
        "scores": scores,
        "weighted_total": total,
        "hard_fails": hard_fails,
        "verdict": verdict,
    }


def render_markdown_table(scored: list[dict[str, Any]], criteria: list[str]) -> str:
    header = "| Case | " + " | ".join(criteria) + " | Weighted | Hard Fails | Verdict |"
    sep = "| :--- | " + " | ".join([":---:"] * len(criteria)) + " | :---: | :--- | :---: |"
    rows = [header, sep]
    for row in scored:
        crit_vals = " | ".join(str(row["scores"][c]) for c in criteria)
        hf_str = ", ".join(row["hard_fails"]) if row["hard_fails"] else "none"
        rows.append(
            f"| {row['case_id']} | {crit_vals} | {row['weighted_total']:.2f} | {hf_str} | {row['verdict']} |"
        )
    return "\n".join(rows)


def evaluate(
    rubric: dict[str, Any],
    current_raw: list[dict[str, Any]],
    prev_raw: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    weights: dict[str, float] = rubric["weights"]
    weight_sum = round(sum(weights.values()), 6)
    if abs(weight_sum - 1.0) > 1e-4:
        raise ValueError(f"Rubric weights must sum to 1.00, got {weight_sum}")
    threshold = float(rubric["threshold"])
    criteria = list(weights.keys())

    scored = [score_case(c, weights, threshold) for c in current_raw]
    mean_score = round(sum(r["weighted_total"] for r in scored) / len(scored), 2) if scored else 0.0
    total_hard_fails = sum(len(r["hard_fails"]) for r in scored)

    regressions: list[dict[str, Any]] = []
    prev_zero_hf = False
    if prev_raw is not None:
        prev_scored = {r["case_id"]: r for r in (score_case(c, weights, threshold) for c in prev_raw)}
        prev_zero_hf = sum(len(r["hard_fails"]) for r in prev_scored.values()) == 0
        for cur in scored:
            cid = cur["case_id"]
            if cid not in prev_scored:
                continue
            prv = prev_scored[cid]
            if prv["verdict"] == "pass" and cur["verdict"] != "pass":
                regressions.append(
                    {
                        "case_id": cid,
                        "reason": f"verdict regressed {prv['verdict']} -> {cur['verdict']}",
                        "prev_score": prv["weighted_total"],
                        "curr_score": cur["weighted_total"],
                    }
                )
            elif not prv["hard_fails"] and cur["hard_fails"]:
                regressions.append(
                    {
                        "case_id": cid,
                        "reason": f"new hard_fails: {cur['hard_fails']}",
                        "prev_score": prv["weighted_total"],
                        "curr_score": cur["weighted_total"],
                    }
                )

    two_consecutive_zero_hf = (total_hard_fails == 0) and prev_zero_hf
    stop_condition_met = (
        mean_score >= threshold
        and two_consecutive_zero_hf
        and len(regressions) == 0
    )

    return {
        "threshold": threshold,
        "mean_weighted_score": mean_score,
        "total_hard_fails": total_hard_fails,
        "two_consecutive_zero_hard_fails": two_consecutive_zero_hf,
        "regressions": regressions,
        "stop_condition_met": stop_condition_met,
        "markdown_table": render_markdown_table(scored, criteria),
        "cases": scored,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Score rubric results and check stop condition.")
    parser.add_argument("--rubric", required=True, help="Path to rubric JSON.")
    parser.add_argument("--results", required=True, help="Path to current version results JSON.")
    parser.add_argument("--prev", help="Optional path to previous version results JSON.")
    parser.add_argument("--markdown", action="store_true", help="Print markdown table before JSON.")
    args = parser.parse_args()

    rubric = json.loads(Path(args.rubric).read_text(encoding="utf-8"))
    current = json.loads(Path(args.results).read_text(encoding="utf-8"))
    prev = json.loads(Path(args.prev).read_text(encoding="utf-8")) if args.prev else None

    report = evaluate(rubric, current, prev)
    if args.markdown:
        print(report["markdown_table"])
        print()
    summary = {k: v for k, v in report.items() if k != "markdown_table"}
    print(json.dumps(summary, indent=2))
    return 0 if report["stop_condition_met"] else 1


if __name__ == "__main__":
    sys.exit(main())
