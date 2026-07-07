# Context Pruning Documentation

This directory contains a mix of current package documentation and draft research notes.

## Current Implementation References

- [README](../README.md)
- [API Reference](api-reference.md)
- [Implementation Guide](implementation-guide.md)
- [Performance Metrics](performance-metrics.md)
- [Case Studies](case-studies.md)
- [Evidence Standard](evidence-standard.md)

## Quick Start

```bash
git clone https://github.com/Mxcks/context-pruning-research.git
cd context-pruning-research
python -m pip install .
python -m pytest tests/
context-pruning status --json
```

## Evidence Standard

Docs should clearly separate:

- implemented package behavior
- local synthetic benchmark results
- proposed API/server features
- illustrative scenarios
- future research hypotheses

When in doubt, describe the feature as proposed until code and tests exist. Use [Evidence Standard](evidence-standard.md) before adding measurable public claims.
