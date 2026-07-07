#!/usr/bin/env python3
"""Compatibility demo for the public context_pruning package."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from context_pruning import ContextPruningEngine, Priority


def main() -> None:
    engine = ContextPruningEngine()

    packages = [
        (
            "Critical System Configuration",
            "system-admin",
            Priority.CRITICAL,
            {"instructions": "Synthetic critical configuration example."},
            ["critical", "configuration", "synthetic"],
        ),
        (
            "User Documentation",
            "documentation",
            Priority.MEDIUM,
            {"sections": ["Introduction", "Installation", "Usage"]},
            ["documentation", "synthetic"],
        ),
        (
            "Historical Logs",
            "logging",
            Priority.LOW,
            {"logs": ["Synthetic startup event", "Synthetic backup event"]},
            ["logs", "synthetic"],
        ),
    ]

    created_ids = [
        engine.create_package(name, domain, priority, content, tags)
        for name, domain, priority, content, tags in packages
    ]

    print("Created packages:")
    for package_id in created_ids:
        print(f"  {package_id}")

    print("\nInitial context stats:")
    for key, value in engine.get_stats().items():
        print(f"  {key}: {value}")

    print("\nPruning context with 100 byte limit...")
    for key, value in engine.prune_context(max_active_size=100).items():
        print(f"  {key}: {value}")

    print("\nFinal context stats:")
    for key, value in engine.get_stats().items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
