# Evidence Standard

This repository separates implemented behavior, benchmark evidence, hypotheses, and roadmap ideas. Public docs should make that distinction explicit.

## Claim Categories

Use these labels when writing docs, summaries, examples, or release notes.

| Category | Meaning | Required Evidence |
| --- | --- | --- |
| Implemented | Behavior exists in the importable package or CLI. | Source code reference and passing test or command. |
| Locally verified | Behavior was reproduced on a local machine. | Exact command, date, environment, and result summary. |
| Benchmark-supported | A repeatable benchmark demonstrates the claim for a synthetic workload. | Benchmark command, benchmark input shape, raw output or committed report, and benchmark invariants. |
| Production-verified | Behavior was observed in a real deployment or real user workflow. | Deployment context, dataset/workload description, reproduction notes, and limitations. |
| Hypothesis | A plausible expected benefit that has not been proven. | Clear "hypothesis" label and proposed measurement plan. |
| Roadmap | Planned or desired capability that is not implemented. | Clear "roadmap" label and no present-tense implementation claims. |

## Required Claim Format

Every measurable claim should answer:

- What was measured?
- What command, test, benchmark, or workflow produced the evidence?
- What code version or commit was used?
- What environment was used?
- What limitation changes how the result should be interpreted?

Example:

```text
Locally verified on 2026-07-07 with Python 3.13.11:
python implementation/benchmark.py completed successfully and detached lower-priority packages under a 50 KB active-size limit.
This is synthetic benchmark evidence, not production LLM quality evidence.
```

## Safe Public Claims Today

The current repository can safely claim:

- The Python package imports successfully.
- The CLI exposes local package management commands.
- The engine can create, retrieve, prune, detach, restore, and persist packages.
- Tests cover core engine, CLI, and context isolation behavior.
- The benchmark script exercises synthetic package creation, pruning, retrieval, and size comparison.
- Benchmark invariants are asserted by `implementation/benchmark.py`.

## Claims That Need More Evidence

Do not make these claims unless new evidence is added:

- Production readiness.
- General LLM quality improvement.
- General cost reduction.
- General productivity improvement.
- Real-world support, coding, research, or creative workflow impact.
- Statistical significance.
- Security guarantees beyond what the current code implements.

## Benchmark Rules

Benchmark reports must include:

- the exact command used
- the input size and workload shape
- whether storage is temporary or persistent
- which values are assertions versus observations
- why the result should not be generalized beyond the workload

Timing values should be treated as observational unless the benchmark includes a stable threshold and explains why that threshold is portable across machines.

## Pull Request Checklist

Before merging docs or summaries:

- [ ] Present-tense implementation claims are backed by source code.
- [ ] Measurable claims cite a test, benchmark, or workflow.
- [ ] Hypotheses are labeled as hypotheses.
- [ ] Roadmap features are labeled as roadmap items.
- [ ] Examples use safe placeholder values, not credential-shaped secrets.
- [ ] Production claims include production evidence.
