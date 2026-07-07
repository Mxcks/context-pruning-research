# Benchmark Report

This report describes the current local benchmark script for the importable `context_pruning` package.

## Status

The benchmark is a synthetic local benchmark, not a production LLM evaluation. It is useful for checking that package creation, pruning, retrieval, and persistence paths run without crashing and for comparing future code changes against the same workload.

## Reproduce

```bash
python implementation/benchmark.py
```

The script writes `benchmark_results.json`. That file is ignored by git because it contains machine-specific timing and timestamp data.

The script also raises an assertion failure if core benchmark invariants stop holding. Those invariants cover expected package counts, detachment after pruning, active-size limits, and positive size reduction.

## Current Benchmark Workload

`implementation/benchmark.py` currently:

- creates 100 medium-priority synthetic packages
- measures package creation time
- prunes to a 100 KB active-size limit
- retrieves active packages
- creates 5 larger low-priority synthetic packages
- prunes again with a 50 KB active-size limit
- compares a 200-package baseline against a pruned run
- validates portable benchmark invariants before exiting successfully

The benchmark uses temporary storage so repeated runs are not contaminated by prior registry state.

The default workload can be reduced for CI by setting:

- `CONTEXT_BENCHMARK_PERFORMANCE_PACKAGES`
- `CONTEXT_BENCHMARK_LARGE_PACKAGES`
- `CONTEXT_BENCHMARK_COMPARISON_PACKAGES`

GitHub Actions uses a smaller deterministic workload so CI remains fast while still checking the same invariant categories.

## Interpreting Results

The reported size reduction is a direct consequence of the configured active-size limits and synthetic package sizes. It should not be presented as a general LLM quality or productivity improvement.

Safe claims:

- The benchmark script runs against the current package API.
- The engine can detach lower-priority packages to local storage.
- Active context size can be reduced when a size limit is applied.
- Detached packages remain registered and retrievable by ID.

Claims that still need separate evidence:

- response quality improvements
- response consistency improvements
- support, research, creative, or development productivity gains
- production readiness
- real-world cost savings

## Next Benchmark Improvements

- Add raw benchmark output snapshots for release tags.
- Separate performance regression tests from research experiments.
- Update or retire older static benchmark result files that no longer match current code.
