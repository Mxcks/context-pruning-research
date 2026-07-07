# Performance Metrics

## Status

This document is being reset to a public-safe evidence standard. Earlier versions included broad quantitative claims and statistical tables that were not backed by reproducible data in this repository.

## Verified Locally

The current verified workflow is:

```bash
python -m pytest tests/ -q
python implementation/benchmark.py
```

The tests verify package and CLI behavior. The benchmark verifies a synthetic local workload using the current package API.

## What Can Be Claimed Today

- The package can create and persist context packages.
- The CLI can create, list, retrieve, prune, and restore packages across separate runs.
- The benchmark can reduce active context size by detaching lower-priority synthetic packages under a configured size limit.
- Detached packages remain tracked by the registry and can be retrieved.

## What Needs More Evidence

The following claim types require separate methodology, raw data, and reproducible scripts before they should be presented as measured results:

- response accuracy gains
- response consistency gains
- user productivity gains
- support resolution improvements
- creative output volume gains
- cost savings
- production reliability improvements

## Minimum Evidence Standard

Any future metric should include:

- exact command or script used to generate it
- package version or commit SHA
- Python version and operating system
- synthetic or real-data classification
- input parameters
- raw output or generated artifact path
- known limitations

## Next Step

Update `BENCHMARK_REPORT.md` and any generated benchmark files together whenever the benchmark workload changes.
