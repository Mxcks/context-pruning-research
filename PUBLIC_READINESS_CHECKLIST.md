# Public Readiness Checklist

This checklist turns the review findings into a staged path from promising research draft to reproducible public artifact.

## Phase 1: Install, Package, and API Correctness

- [x] Remove non-pip entries from `requirements.txt`: `python>=3.8`, `sqlite3`, and `zlib`.
- [x] Keep Python version constraints only in `pyproject.toml` / `setup.py`.
- [x] Replace placeholder repository URLs with `https://github.com/Mxcks/context-pruning-research`.
- [x] Move the real engine from `implementation/context_pruning.py` into the importable `context_pruning/` package.
- [x] Export public classes from `context_pruning/__init__.py`.
- [x] Ensure the built wheel includes the engine, examples or package data needed by docs, and any benchmark entrypoints meant for users.
- [x] Fix console script metadata so `context-pruning` installs and runs from a clean environment.
- [x] Add a clean-install smoke test that runs `pip install .` and imports the public API.

## Phase 2: CLI and User-Facing Workflow

- [x] Replace stub CLI commands with real engine-backed behavior.
- [x] Define the first supported CLI surface clearly: `init`, `create-package`, `prune`, `status`, and `restore`.
- [x] Keep new CLI output ASCII-safe.
- [x] Add `--storage-path` so the engine does not default to a machine-specific Base41 path.
- [x] Add `--json` output for automation-friendly command results.
- [x] Add CLI tests that verify every documented command works.

## Phase 3: Benchmark Reproducibility

- [ ] Fix divide-by-zero paths in `implementation/benchmark.py`.
- [ ] Add benchmark assertions so failures are explicit instead of producing misleading reports.
- [ ] Generate benchmark output from the current code during CI or a local verification script.
- [ ] Store raw benchmark input parameters alongside results.
- [ ] Separate measured claims from projected or theoretical claims.
- [ ] Re-run benchmark after packaging changes and update `simple_benchmark_results.json`.

## Phase 4: Test Quality

- [ ] Replace dict-copy isolation tests with tests that exercise `ContextPruningEngine`.
- [ ] Test package creation, priority retention, detachment, restoration, and state transitions.
- [ ] Test serialization and deserialization of enum fields after detachment.
- [ ] Test behavior when compressed packages are zero so benchmark/report code cannot crash.
- [ ] Test documented examples on Windows and Git Bash.
- [ ] Add coverage thresholds for the real package, not only the test files.

## Phase 5: Documentation Accuracy

- [ ] Update README file tree to match the actual repository.
- [ ] Either add missing `spec/01-*` files and `schemas/` files or remove those references.
- [ ] Replace `<repository-url>` placeholders with the real clone URL.
- [ ] Update setup instructions after the clean install path works.
- [ ] Make the API reference match the implemented package and CLI.
- [ ] Mark any future API server examples as proposed, not currently available.
- [ ] Add a short "What is verified today" section and a separate "Research hypotheses" section.

## Phase 6: Claims and Research Integrity

- [ ] Downgrade unsupported claims such as response consistency, case-study gains, and 100% elimination until source data exists.
- [ ] Add methodology for every retained quantitative claim.
- [ ] Add raw data or reproducible scripts for every benchmark table.
- [ ] Label illustrative examples clearly.
- [ ] Add limitations and failure modes.
- [ ] Add a reproducibility note explaining machine, Python version, command sequence, and expected output.

## Phase 7: Cross-Platform Hygiene

- [ ] Normalize existing shell scripts to LF line endings.
- [x] Add `.gitattributes` to enforce line endings for `.sh`, `.ps1`, `.py`, and `.md`.
- [ ] Test shell scripts under Git Bash.
- [ ] Test PowerShell scripts under Windows PowerShell or PowerShell 7.
- [x] Remove hardcoded absolute paths from touched examples and tests.
- [x] Use temporary directories for new tests by default.

## Phase 8: Public Safety Gate

- [ ] Confirm all example data is synthetic, generic, and safe to publish.
- [ ] Remove real secrets, tokens, credentials, private URLs, and secret-shaped placeholder values.
- [ ] Remove local absolute paths such as `E:\Research\...`, `E:\dev\...`, and `C:\Users\...`.
- [ ] Remove private Base41, client, project, calendar, finance, agent, or workspace details unless intentionally public.
- [ ] Remove generated logs, scratchpads, caches, build folders, virtual environments, and temporary output files.
- [ ] Ensure benchmark data is reproducible from checked-in code and safe synthetic inputs.
- [ ] Ensure claims do not reveal private operations, client outcomes, or unapproved business process details.
- [x] Add or update `.gitignore` so private runtime files cannot be committed accidentally.
- [x] Add or update `.gitattributes` so line endings and text normalization are predictable.
- [ ] Run a final secret/path scan before release.

Suggested scan patterns:

```bash
rg -n "C:\\\\Users|E:\\\\Research|E:\\\\dev|api[_-]?key|token|secret|password|client|Base41|calendar|finance|payroll|telegram|linear|n8n" .
```

## Phase 9: Public Release Gate

- [ ] Fresh clone succeeds.
- [ ] `pip install -r requirements.txt` succeeds or README no longer recommends that path.
- [ ] `pip install .` succeeds.
- [ ] `python -m pytest` passes with meaningful package coverage.
- [ ] `python examples/basic_pruning.py` succeeds.
- [ ] `python implementation/benchmark.py` succeeds or is replaced by a supported benchmark command.
- [ ] `context-pruning --version` succeeds after install.
- [ ] README claims match the verified evidence.
- [ ] No local-only paths, placeholder URLs, or secret-shaped example values remain.

## Suggested First PR

Scope the first PR to install/package/API correctness only:

- Clean dependency files.
- Move the engine into the package.
- Export the public API.
- Fix console script installation.
- Add clean install and import smoke tests.

This creates a stable base before changing research claims, benchmarks, or larger documentation.
