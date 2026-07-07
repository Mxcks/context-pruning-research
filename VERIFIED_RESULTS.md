# Verified Results

## Status

The verified results in this repository are local and synthetic. They validate current package behavior, CLI persistence, and benchmark execution.

## Verified Commands

```bash
python -m pytest tests/ -q
python -m build --sdist --wheel
python implementation/benchmark.py
```

## Verified Behaviors

- `ContextPruningEngine` can create packages.
- Packages persist through `registry.json`.
- CLI commands can create, list, retrieve, prune, and restore packages.
- Pruning can detach lower-priority packages under size pressure.
- Detached packages remain retrievable by ID.
- The benchmark script runs with isolated temporary storage.

## Limitations

- Benchmarks use synthetic generated package content.
- Timing varies by machine.
- Benchmark output is not committed by default.
- Results do not measure LLM response quality.
- Results do not prove production readiness.

## Reproducibility Notes

Use the commands above from a fresh checkout after installing the package. If benchmark numbers are reported publicly, include the commit SHA, Python version, operating system, command, and generated `benchmark_results.json` content.
