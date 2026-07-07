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

- [x] Fix divide-by-zero paths in `implementation/benchmark.py`.
- [x] Add benchmark assertions so failures are explicit instead of producing misleading reports.
- [x] Generate benchmark output from the current code during a local verification script.
- [x] Store raw benchmark input parameters alongside results.
- [x] Separate measured claims from projected or theoretical claims.
- [ ] Re-run benchmark after packaging changes and update `simple_benchmark_results.json`.

## Phase 4: Test Quality

- [ ] Replace dict-copy isolation tests with tests that exercise `ContextPruningEngine`.
- [ ] Test package creation, priority retention, detachment, restoration, and state transitions.
- [ ] Test serialization and deserialization of enum fields after detachment.
- [ ] Test behavior when compressed packages are zero so benchmark/report code cannot crash.
- [ ] Test documented examples on Windows and Git Bash.
- [ ] Add coverage thresholds for the real package, not only the test files.

## Phase 5: Documentation Accuracy

- [x] Update README file tree to match the actual repository.
- [x] Either add missing `spec/01-*` files and `schemas/` files or remove those references.
- [x] Replace `<repository-url>` placeholders with the real clone URL.
- [x] Update setup instructions after the clean install path works.
- [x] Make the API reference identify proposed API/server behavior instead of current package behavior.
- [x] Mark any future API server examples as proposed, not currently available.
- [x] Add a short "What is verified today" section and a separate "Research hypotheses" section.

## Phase 6: Claims and Research Integrity

- [x] Downgrade unsupported claims such as response consistency, case-study gains, and 100% elimination until source data exists.
- [x] Add methodology for every retained quantitative claim.
- [ ] Add raw data or reproducible scripts for every benchmark table.
- [x] Label illustrative examples clearly.
- [x] Add limitations and failure modes.
- [x] Add a reproducibility note explaining machine, Python version, command sequence, and expected output.

## Phase 7: Cross-Platform Hygiene

- [ ] Normalize existing shell scripts to LF line endings.
- [x] Add `.gitattributes` to enforce line endings for `.sh`, `.ps1`, `.py`, and `.md`.
- [ ] Test shell scripts under Git Bash.
- [ ] Test PowerShell scripts under Windows PowerShell or PowerShell 7.
- [x] Remove hardcoded absolute paths from touched examples and tests.
- [x] Use temporary directories for new tests by default.

## Phase 8: Public Safety Gate

- [x] Confirm all example data is synthetic, generic, and safe to publish.
- [x] Remove real secrets, tokens, credentials, private URLs, and secret-shaped placeholder values.
- [x] Remove local absolute paths such as `E:\Research\...`, `E:\dev\...`, and `C:\Users\...`.
- [ ] Remove private Base41, client, project, calendar, finance, agent, or workspace details unless intentionally public.
- [x] Remove generated logs, scratchpads, caches, build folders, virtual environments, and temporary output files.
- [x] Ensure benchmark data is reproducible from checked-in code and safe synthetic inputs.
- [ ] Ensure claims do not reveal private operations, client outcomes, or unapproved business process details.
- [x] Add or update `.gitignore` so private runtime files cannot be committed accidentally.
- [x] Add or update `.gitattributes` so line endings and text normalization are predictable.
- [x] Run a final secret/path scan before release.

## Phase 8A: Continuous Verification

- [x] Add GitHub Actions CI for tests, package build, and benchmark invariants.
- [x] Add a repository evidence standard for public claims.
- [x] Add CI badge after the workflow is visible on GitHub.
- [ ] Add release artifact upload for benchmark output if release tags are created.

Suggested scan patterns:

```bash
rg -n "C:\\\\Users|E:\\\\Research|E:\\\\dev|api[_-]?key|token|secret|password|client|Base41|calendar|finance|payroll|telegram|linear|n8n" .
```

## Phase 9: Public Release Gate

- [x] Fresh clone succeeds.
- [x] `pip install -r requirements.txt` succeeds or README no longer recommends that path.
- [x] `pip install .` succeeds.
- [x] `python -m pytest` passes with meaningful package coverage.
- [x] `python examples/basic_pruning.py` succeeds.
- [x] `python implementation/benchmark.py` succeeds or is replaced by a supported benchmark command.
- [x] `context-pruning --version` succeeds after install.
- [x] README claims match the verified evidence.
- [x] No local-only paths, placeholder URLs, or secret-shaped example values remain.

## Suggested First PR

Scope the first PR to install/package/API correctness only:

- Clean dependency files.
- Move the engine into the package.
- Export the public API.
- Fix console script installation.
- Add clean install and import smoke tests.

This creates a stable base before changing research claims, benchmarks, or larger documentation.
