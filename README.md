# Context Pruning Research Repository

A research project on **context pruning** — an LLM architecture pattern that manages long-term memory through **tagging-based rules** instead of opaque numerical scoring for selective retention and compression.

## Purpose

This repository contains research, implementations, and examples of the context pruning technique, which aims to solve common problems with LLM context management:

1. **Buffer overflow**: Keeping all tokens exceeds context window limits
2. **Summarization loss**: Compressing everything destroys precision and addressability
3. **Blind retention**: Heuristic scoring is opaque, unadjustable, and leaks across domains

## Key Innovation

Instead of asking *"how relevant is this information?"* (scoring → ambiguous decision), we ask:
*"Which domain does this belong to, and which package governs its retention?"*

This makes pruning **deterministic**, **auditable**, and **reversible**.

## Repository Structure

```
├── README.md            # This file
├── examples/            # Implementation examples
│   ├── basic_pruning.py    # Simple node-based pruning example
│   └── README.md           # Examples documentation
├── spec/                # Technical specifications
│   ├── 00-overview.md      # Core theory: why tagging beats scoring
│   ├── 01-tagging-system.md  # Tag taxonomy and lifecycle engine
│   ├── 02-context-packages.md  # Package schema and lifecycle states
│   ├── 03-pruning-algorithm.md # Phased pruning flow (full → emergency)
│   ├── 04-memory-integration.md  # Integration points in memory stacks
│   └── 05-implementation-notes.md  # Concrete next steps, open questions
├── schemas/             # Tag bundle examples and package schema definitions
│   ├── 01-context-package-schema.md     # Type-safe field spec for packages
│   └── 02-tag-bundle-examples.md        # Six worked lifecycle examples
├── tests/               # Test suite
│   ├── test_context_isolation.py    # Context isolation tests
│   └── README.md                    # Test documentation
├── requirements.txt     # Python dependencies
└── .gitignore           # Personal data exclusion rules
```

## Getting Started

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd context-pruning-research
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run examples:
   ```bash
   python examples/basic_pruning.py
   ```

4. Run tests:
   ```bash
   python -m pytest tests/
   ```

## Examples

- `examples/basic_pruning.py` - Demonstrates basic node-based context isolation
- `examples/tagging_system.py` - Shows the tagging-based selection mechanism
- `examples/lifecycle_demo.py` - Illustrates the context lifecycle

## Tests

The test suite validates the core concepts:
- Context isolation between projects
- Context persistence to scratchpad
- Context restoration from storage

Run tests with:
```bash
python -m pytest tests/
```

## Status

- [x] Concept formulation (drafted)
- [x] Draft review / personalization (in progress)
- [ ] Public readiness audit
- [ ] Release to public repository (when ready)

## Contributing

This repository is being prepared for public release. Contributions will be welcome once it's publicly available.

## License

This research is released under the MIT License.