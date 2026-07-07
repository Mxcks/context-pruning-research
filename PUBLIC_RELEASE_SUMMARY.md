# Public Release Summary

## Status

This repository is public, but the documentation is still moving toward a stricter evidence standard.

The package currently provides a local context pruning engine, persistent CLI registry, tests, and a synthetic benchmark script. Broader API, production, and real-world outcome claims should be treated as roadmap or illustrative material until supported by reproducible evidence.

## Current Public-Safe Assets

- importable `context_pruning` package
- `context-pruning` CLI
- local filesystem persistence
- pytest coverage for package and CLI behavior
- synthetic benchmark script
- draft specs and schemas
- public readiness checklist

## Current Verification Commands

```bash
python -m pytest tests/ -q
python -m build --sdist --wheel
python implementation/benchmark.py
```

## Remaining Public-Readiness Work

- finish replacing older placeholder URLs
- mark proposed API/server docs clearly
- remove or rewrite unsupported historical benchmark claims
- add benchmark assertions and reproducibility metadata
- decide whether older generated result files should stay, be regenerated, or be archived as historical
