#!/usr/bin/env python3
"""Zero-dependency deterministic hard-fail check runner for Prompt Systems Architect.

Usage:
    python run_deterministic_checks.py --config checks.json --output candidate.txt
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


def run_checks(text: str, config: dict[str, Any]) -> dict[str, Any]:
    hard_fails: list[str] = []
    details: dict[str, str] = {}
    parsed_json: Any = None

    # 1. Template variable leak check
    if config.get("forbid_template_leaks", True):
        leaks = re.findall(r"\{\{[^}]+\}\}", text)
        if leaks:
            hard_fails.append("HF_TEMPLATE_LEAK")
            details["HF_TEMPLATE_LEAK"] = f"Unresolved variables found: {leaks}"

    # 2. Length checks
    max_chars = config.get("max_chars")
    if isinstance(max_chars, int) and len(text) > max_chars:
        hard_fails.append("HF_MAX_CHARS_EXCEEDED")
        details["HF_MAX_CHARS_EXCEEDED"] = f"{len(text)} chars > limit {max_chars}"

    min_chars = config.get("min_chars")
    if isinstance(min_chars, int) and len(text.strip()) < min_chars:
        hard_fails.append("HF_MIN_CHARS_NOT_MET")
        details["HF_MIN_CHARS_NOT_MET"] = f"{len(text.strip())} chars < min {min_chars}"

    words = text.split()
    max_words = config.get("max_words")
    if isinstance(max_words, int) and len(words) > max_words:
        hard_fails.append("HF_MAX_WORDS_EXCEEDED")
        details["HF_MAX_WORDS_EXCEEDED"] = f"{len(words)} words > limit {max_words}"

    # 3. JSON validity & required keys / enums
    if config.get("require_json", False):
        try:
            parsed_json = json.loads(text)
        except json.JSONDecodeError as exc:
            hard_fails.append("HF_INVALID_JSON")
            details["HF_INVALID_JSON"] = f"JSON parse error: {exc}"

    if isinstance(parsed_json, dict):
        required_keys = config.get("required_keys", [])
        missing = [k for k in required_keys if k not in parsed_json]
        if missing:
            hard_fails.append("HF_MISSING_REQUIRED_KEYS")
            details["HF_MISSING_REQUIRED_KEYS"] = f"Missing keys: {missing}"

        allowed_enums = config.get("allowed_enums", {})
        for key, allowed in allowed_enums.items():
            if key in parsed_json and parsed_json[key] not in allowed:
                hf_id = f"HF_INVALID_ENUM_{key.upper()}"
                hard_fails.append(hf_id)
                details[hf_id] = f"{key}={parsed_json[key]!r} not in {allowed}"

    # 4. Forbidden regex patterns
    for rule in config.get("forbidden_regex", []):
        flags = re.IGNORECASE if rule.get("ignore_case", True) else 0
        if re.search(rule["pattern"], text, flags):
            hf_id = rule.get("id", "HF_FORBIDDEN_REGEX")
            hard_fails.append(hf_id)
            details[hf_id] = f"Matched forbidden pattern: {rule['pattern']}"

    # 5. Required regex patterns
    for rule in config.get("required_regex", []):
        flags = re.IGNORECASE if rule.get("ignore_case", True) else 0
        if not re.search(rule["pattern"], text, flags):
            hf_id = rule.get("id", "HF_MISSING_REQUIRED_PATTERN")
            hard_fails.append(hf_id)
            details[hf_id] = f"Missing required pattern: {rule['pattern']}"

    return {
        "passed": len(hard_fails) == 0,
        "hard_fails": hard_fails,
        "details": details,
        "metrics": {"chars": len(text), "words": len(words)},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run deterministic hard-fail checks.")
    parser.add_argument("--config", required=True, help="Path to JSON check config file.")
    parser.add_argument("--output", required=True, help="Path to candidate model output text.")
    args = parser.parse_args()

    config = json.loads(Path(args.config).read_text(encoding="utf-8"))
    text = Path(args.output).read_text(encoding="utf-8")
    result = run_checks(text, config)
    print(json.dumps(result, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
