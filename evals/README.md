# Trigger evals

Measures whether the GenPage skill's `description` field actually triggers on the
right queries — and *doesn't* trigger on near-miss negatives.

## Files

- `trigger-eval.json` — 20 realistic queries (10 should-trigger, 10 should-not), with rationale.
- `candidate-descriptions.json` — the descriptions to compare. Add more candidates as you iterate.
- `run-trigger-eval.py` — runs each query against an LLM CLI 3× and reports accuracy.
- `trigger-eval-results.json` — written by the runner.

## Run it

Default uses Claude Code's CLI:

```bash
python3 evals/run-trigger-eval.py
```

Override with any other CLI that takes a prompt as a positional arg:

```bash
python3 evals/run-trigger-eval.py --cmd 'gemini -p'
python3 evals/run-trigger-eval.py --runs 5
```

## How to interpret

Per candidate you get three numbers:

| Metric | What it measures | Goal |
|---|---|---|
| `overall_accuracy` | Mean of correct calls (1.0 = perfect) | maximize |
| `should_trigger_recall` | Of queries that *should* trigger, how often the LLM said YES | high (catch real cases) |
| `should_not_trigger_specificity` | Of queries that *shouldn't* trigger, how often the LLM said NO | high (avoid false triggers) |

A description that scores `1.0 / 0.4` (high specificity, low recall) is **undertriggering** — the failure mode skill-creator warns about most. Bias the rewrite toward more user-verb examples and pushier "use this whenever…" framing.

A description that scores `0.6 / 1.0` (low specificity, high recall) is **overtriggering** — it'll fire on simple questions. Tighten with negative cues or remove overly broad terms.

## Iterating

After the first run, look at `trigger-eval-results.json` for queries where `correct_rate < 0.67` — those are the ones the description doesn't handle. Either:
1. Adjust the description to better cover (or exclude) that pattern, OR
2. If the query is borderline, fix the eval label.

Add the revised description as a new entry in `candidate-descriptions.json` (e.g. `v3-tightened`) and re-run. The runner reports a winner by `overall_accuracy`.

## Notes

- This is a lightweight version of skill-creator's `run_loop.py` — same idea (3× sampling, accuracy on a held-out set), simpler shell-out CLI integration, no automatic rewriting loop.
- If you want the full optimization loop (auto-proposing new descriptions and iterating), use skill-creator's `scripts/run_loop.py` from <https://github.com/anthropics/skills/tree/main/skills/skill-creator>.
