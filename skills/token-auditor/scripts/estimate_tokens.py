#!/usr/bin/env python3
"""Zero-dependency approximate token and cost-per-1,000-calls estimator.

NOTE: Heuristic approximation only — NOT an exact model tokenizer.

Usage:
    python estimate_tokens.py --prompt prompt.txt --dynamic-in 300 --avg-out 180 \
        --price-in 1.25 --price-cached 0.31 --price-out 5.00
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path
from typing import Any


def estimate_text_tokens(text: str) -> dict[str, Any]:
    chars = len(text)
    words = len(text.split())
    pieces = len(re.findall(r"\w+|[^\w\s]", text))
    by_chars = math.ceil(chars / 4.0) if chars else 0
    by_pieces = math.ceil(pieces * 1.15) if pieces else 0
    blended = math.ceil((by_chars + by_pieces) / 2.0) if chars else 0
    return {
        "chars": chars,
        "words": words,
        "approx_tokens": blended,
        "range": [min(by_chars, by_pieces), max(by_chars, by_pieces)],
    }


def cost_per_1k(
    static_tokens: int,
    dynamic_tokens: int,
    output_tokens: int,
    price_in: float,
    price_cached: float,
    price_out: float,
    cache_hit_rate: float = 0.85,
) -> dict[str, float]:
    uncached = ((static_tokens + dynamic_tokens) * price_in + output_tokens * price_out) / 1000.0
    eff_static_price = cache_hit_rate * price_cached + (1.0 - cache_hit_rate) * price_in
    cached = (static_tokens * eff_static_price + dynamic_tokens * price_in + output_tokens * price_out) / 1000.0
    savings_pct = ((uncached - cached) / uncached * 100.0) if uncached > 0 else 0.0
    return {
        "uncached_usd_per_1k": round(uncached, 4),
        "cached_usd_per_1k": round(cached, 4),
        "cache_hit_rate_assumed": cache_hit_rate,
        "cache_savings_pct": round(savings_pct, 1),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Approximate prompt token & cost/1k estimator.")
    parser.add_argument("--prompt", required=True, help="Path to prompt file.")
    parser.add_argument("--split-marker", default="--- DYNAMIC INPUT", help="Static/dynamic boundary marker.")
    parser.add_argument("--dynamic-in", type=int, default=0, help="Expected average dynamic input tokens.")
    parser.add_argument("--avg-out", type=int, default=150, help="Expected average output tokens.")
    parser.add_argument("--price-in", type=float, default=1.25, help="USD per 1M input tokens.")
    parser.add_argument("--price-cached", type=float, default=0.31, help="USD per 1M cached input tokens.")
    parser.add_argument("--price-out", type=float, default=5.00, help="USD per 1M output tokens.")
    parser.add_argument("--cache-hit-rate", type=float, default=0.85, help="Assumed cache hit rate (0-1).")
    args = parser.parse_args()

    text = Path(args.prompt).read_text(encoding="utf-8")
    if args.split_marker and args.split_marker in text:
        static_part, dynamic_part = text.split(args.split_marker, 1)
    else:
        static_part, dynamic_part = text, ""

    total_est = estimate_text_tokens(text)
    static_est = estimate_text_tokens(static_part)
    dynamic_template_est = estimate_text_tokens(dynamic_part)

    total_dynamic_in = dynamic_template_est["approx_tokens"] + args.dynamic_in
    costs = cost_per_1k(
        static_tokens=static_est["approx_tokens"],
        dynamic_tokens=total_dynamic_in,
        output_tokens=args.avg_out,
        price_in=args.price_in,
        price_cached=args.price_cached,
        price_out=args.price_out,
        cache_hit_rate=args.cache_hit_rate,
    )

    report = {
        "method": "APPROXIMATE heuristic (blend of ceil(chars/4) and ceil(regex_pieces*1.15)); NOT an exact model tokenizer.",
        "prompt_total": total_est,
        "static_cacheable_prefix": static_est,
        "dynamic_template_suffix": dynamic_template_est,
        "assumptions": {
            "expected_dynamic_payload_tokens": args.dynamic_in,
            "expected_avg_output_tokens": args.avg_out,
            "usd_per_1m_input": args.price_in,
            "usd_per_1m_cached_input": args.price_cached,
            "usd_per_1m_output": args.price_out,
        },
        "cost_per_1k_calls": costs,
    }
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
