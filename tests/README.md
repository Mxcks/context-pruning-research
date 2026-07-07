# Context Pruning Tests

This directory contains tests for the context pruning system.

## Test Structure

1. **unit/** - Unit tests for individual components
2. **integration/** - Integration tests for combined components
3. **examples/** - Example implementations showing usage patterns

## Current Tests

- `test_context_isolation.py` - Verifies context isolation between projects
- `test_pruning_lifecycle.py` - Tests the pruning lifecycle (active → compressed → detached)
- `test_tagging_system.py` - Validates the tagging-based selection mechanism

## Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test
python -m pytest tests/test_context_isolation.py
```