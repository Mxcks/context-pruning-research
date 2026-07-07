# Context Pruning Research

[![CI](https://github.com/Mxcks/context-pruning-research/actions/workflows/ci.yml/badge.svg)](https://github.com/Mxcks/context-pruning-research/actions/workflows/ci.yml)

Context pruning is a research and prototype implementation for managing long-running LLM context with explicit packages, priorities, lifecycle states, and auditable retention rules.

The core idea is simple: instead of asking only "how relevant is this text?", organize context into named packages and decide what remains active, compressed, detached, or archived by rule.

## Current Implementation

The current Python package provides:

- `ContextPackage`: a structured context unit with metadata.
- `ContextPruningEngine`: local package creation, retrieval, pruning, restore, and persistence.
- `Priority`: `critical`, `high`, `medium`, and `low`.
- `State`: `active`, `compressed`, `detached`, and `archived`.
- `context-pruning` CLI with `init`, `status`, `create-package`, `list-packages`, `get-package`, `prune`, `restore`, and `prune-demo`.

The current implementation uses local filesystem storage. Cloud storage, database-backed metadata, API servers, dashboards, encryption, RBAC, advanced compression, and automatic rule learning are research roadmap items unless explicitly implemented in code.

## Quick Start

```bash
git clone https://github.com/Mxcks/context-pruning-research.git
cd context-pruning-research
python -m pip install .
context-pruning --version
context-pruning init
context-pruning create-package --name "Example Package" --domain demo --priority medium --content-file examples/package_content.json
context-pruning status
```

Run tests:

```bash
python -m pytest tests/
```

Run the local benchmark:

```bash
python implementation/benchmark.py
```

Benchmark output is generated as `benchmark_results.json` and is intentionally ignored by git because timings and timestamps vary by machine.

The benchmark also asserts portable invariants for package counts, detachment behavior, active-size limits, and positive size reduction. Timing values remain observational.

## Repository Structure

```text
context_pruning/              Importable Python package
  __init__.py                  Public API exports
  cli.py                       CLI entrypoint
  engine.py                    Core pruning engine
implementation/               Compatibility demos and benchmark scripts
examples/                     Early examples
spec/                         Draft design specifications
schemas/                      Draft schema and tag examples
tests/                        Pytest coverage for package and CLI behavior
docs/                         Broader research documentation
docs/evidence-standard.md     Evidence rules for public claims
BENCHMARK_REPORT.md           Current benchmark summary
PUBLIC_READINESS_CHECKLIST.md Public-release cleanup checklist
```

## Locally Verified Today

Current verification is local and synthetic. It demonstrates that the package API, CLI persistence, pruning transitions, build, and benchmark script run successfully on the test machine.

Verified commands:

```bash
python -m pytest tests/ -q
python -m build --sdist --wheel
python implementation/benchmark.py
```

Current test coverage is focused on the importable package and CLI. The broader research claims in `docs/` are being reviewed and should be treated as draft research material unless they meet the [evidence standard](docs/evidence-standard.md).

## Benchmark Scope

`implementation/benchmark.py` creates synthetic packages, prunes them with size limits, and reports local timing and active-context size changes.

These benchmark results are useful for regression checks, but they are not yet evidence of production LLM quality improvements. Any claims about response quality, productivity, support outcomes, or business impact should be treated as hypotheses until backed by reproducible studies.

## Research Roadmap

Planned research and implementation areas:

- richer lifecycle rules and scheduled pruning
- compression backends
- storage backend abstraction
- stronger benchmark methodology
- API/server layer if needed
- dashboard or visualization tools
- documented limitations and failure modes

## Safety and Public Data

Public examples should use synthetic data only. Do not commit real secrets, private project details, local machine paths, generated benchmark output, caches, or runtime storage.

See [PUBLIC_READINESS_CHECKLIST.md](PUBLIC_READINESS_CHECKLIST.md) and [docs/evidence-standard.md](docs/evidence-standard.md) for the release gate.

## License

MIT License.
