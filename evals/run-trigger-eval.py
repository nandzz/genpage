#!/usr/bin/env python3
"""
Trigger eval runner for GenPage skill descriptions.

Asks an LLM (Claude via `claude -p`, by default) whether each query in
trigger-eval.json should trigger the skill, given a candidate description.
Runs each query 3 times to get a stable rate. Outputs per-candidate scores.

Usage:
    python3 evals/run-trigger-eval.py
    python3 evals/run-trigger-eval.py --runs 5
    python3 evals/run-trigger-eval.py --cmd 'gemini -p'   # any LLM CLI that takes a prompt as last arg

Requires either:
    - `claude` CLI on PATH (default), OR
    - any other CLI that accepts a prompt as a positional arg

This script does NOT call paid APIs directly — it shells out to a CLI you
already have configured. Free of API key handling.
"""
import argparse
import json
import os
import statistics
import subprocess
import sys
from pathlib import Path

EVAL_DIR = Path(__file__).parent
EVAL_FILE = EVAL_DIR / "trigger-eval.json"
CANDIDATES_FILE = EVAL_DIR / "candidate-descriptions.json"

PROMPT_TEMPLATE = """You are deciding whether a user query should trigger a particular agent skill.

The skill's description is:
\"\"\"
{description}
\"\"\"

The user's query is:
\"\"\"
{query}
\"\"\"

Should this query trigger the skill? Reply with EXACTLY one word: YES or NO. No explanation, no punctuation."""


def ask(cmd: list[str], prompt: str) -> str:
    """Run the LLM CLI with the prompt and return stdout, lowercased+trimmed."""
    result = subprocess.run(
        cmd + [prompt], capture_output=True, text=True, timeout=60
    )
    return result.stdout.strip().lower()


def evaluate(cmd: list[str], description: str, queries: list[dict], runs: int) -> dict:
    """Return per-query results and aggregate scores for a candidate description."""
    per_query = []
    for i, q in enumerate(queries, 1):
        prompt = PROMPT_TEMPLATE.format(description=description, query=q["query"])
        triggers = []
        for _ in range(runs):
            answer = ask(cmd, prompt)
            triggers.append(answer.startswith("yes"))
        rate = sum(triggers) / len(triggers)
        correct_rate = rate if q["should_trigger"] else 1 - rate
        mark = "✓" if correct_rate >= 0.67 else "✗"
        exp = "T" if q["should_trigger"] else "F"
        print(f"  [{i:>2}/{len(queries)}] {mark} expect={exp} rate={rate:.2f} :: {q['query'][:70]}", flush=True)
        per_query.append({
            "query": q["query"][:80],
            "expected": q["should_trigger"],
            "trigger_rate": round(rate, 2),
            "correct_rate": round(correct_rate, 2),
        })
    overall = statistics.mean(p["correct_rate"] for p in per_query)
    pos = [p for p in per_query if p["expected"]]
    neg = [p for p in per_query if not p["expected"]]
    return {
        "overall_accuracy": round(overall, 3),
        "should_trigger_recall": round(statistics.mean(p["trigger_rate"] for p in pos), 3),
        "should_not_trigger_specificity": round(
            statistics.mean(1 - p["trigger_rate"] for p in neg), 3
        ),
        "per_query": per_query,
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--runs", type=int, default=3, help="Times to run each query (default 3)")
    p.add_argument("--cmd", default="claude -p", help="LLM CLI command (default: 'claude -p')")
    args = p.parse_args()

    cmd = args.cmd.split()
    queries = json.loads(EVAL_FILE.read_text())
    candidates = json.loads(CANDIDATES_FILE.read_text())["candidates"]

    print(f"Running {len(queries)} queries × {args.runs} runs × {len(candidates)} candidates")
    print(f"CLI: {' '.join(cmd)}\n")

    results = {}
    for cand in candidates:
        print(f"=== Candidate: {cand['id']} ===")
        result = evaluate(cmd, cand["description"], queries, args.runs)
        results[cand["id"]] = result
        print(f"  overall accuracy:           {result['overall_accuracy']}")
        print(f"  should-trigger recall:      {result['should_trigger_recall']}")
        print(f"  should-not-trigger spec.:   {result['should_not_trigger_specificity']}\n")

    out = EVAL_DIR / "trigger-eval-results.json"
    out.write_text(json.dumps(results, indent=2))
    print(f"Detailed results written to {out}")

    # Pick winner
    winner = max(results.items(), key=lambda kv: kv[1]["overall_accuracy"])
    print(f"\nWinner: {winner[0]} (accuracy {winner[1]['overall_accuracy']})")


if __name__ == "__main__":
    main()
