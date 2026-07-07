#!/usr/bin/env python3
"""Command-line interface for context pruning research."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import List, Optional

from . import __version__
from .engine import ContextPackage, ContextPruningEngine, Priority


def _add_common_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--storage-path",
        default=".context-pruning/storage",
        help="Directory used for detached context package storage.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable JSON output.",
    )


def _print_result(data: dict, as_json: bool) -> None:
    if as_json:
        print(json.dumps(data, indent=2, sort_keys=True))
        return
    for key, value in data.items():
        print(f"{key}: {value}")


def _package_summary(package: ContextPackage) -> dict:
    return {
        "id": package.id,
        "name": package.name,
        "domain": package.domain,
        "priority": package.priority.value,
        "state": package.state.value,
        "size": package.size,
        "tags": package.tags,
        "references": package.references,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Context Pruning Research CLI")
    parser.add_argument(
        "--version",
        action="version",
        version=f"Context Pruning Research {__version__}",
    )

    subparsers = parser.add_subparsers(dest="command")

    init_parser = subparsers.add_parser("init", help="Initialize storage.")
    _add_common_options(init_parser)

    status_parser = subparsers.add_parser("status", help="Show engine status.")
    _add_common_options(status_parser)

    create_parser = subparsers.add_parser(
        "create-package",
        help="Create and persist a context package.",
    )
    _add_common_options(create_parser)
    create_parser.add_argument("--name", required=True)
    create_parser.add_argument("--domain", required=True)
    create_parser.add_argument(
        "--priority",
        choices=[priority.value for priority in Priority],
        default=Priority.MEDIUM.value,
    )
    create_parser.add_argument(
        "--content",
        default="{}",
        help="JSON object containing synthetic package content.",
    )
    create_parser.add_argument("--tag", action="append", default=[])
    create_parser.add_argument("--reference", action="append", default=[])

    list_parser = subparsers.add_parser("list-packages", help="List known packages.")
    _add_common_options(list_parser)

    get_parser = subparsers.add_parser("get-package", help="Show one package.")
    _add_common_options(get_parser)
    get_parser.add_argument("package_id")

    prune_parser = subparsers.add_parser("prune", help="Prune persisted packages.")
    _add_common_options(prune_parser)
    prune_parser.add_argument("--max-active-size", type=int, required=True)

    restore_parser = subparsers.add_parser(
        "restore",
        help="Restore a compressed or detached package to active state.",
    )
    _add_common_options(restore_parser)
    restore_parser.add_argument("package_id")

    prune_parser = subparsers.add_parser(
        "prune-demo",
        help="Run a deterministic synthetic pruning demo.",
    )
    _add_common_options(prune_parser)
    prune_parser.add_argument("--max-active-size", type=int, default=250)

    return parser


def main(args: Optional[List[str]] = None) -> int:
    parser = build_parser()
    parsed_args = parser.parse_args(args)

    if not parsed_args.command:
        parser.print_help()
        return 0

    engine = ContextPruningEngine(storage_path=parsed_args.storage_path)

    if parsed_args.command == "init":
        storage_path = Path(parsed_args.storage_path)
        (storage_path / "detached").mkdir(parents=True, exist_ok=True)
        engine.save()
        _print_result({"storage_path": str(storage_path), "initialized": True}, parsed_args.json)
        return 0

    if parsed_args.command == "status":
        _print_result(engine.get_stats(), parsed_args.json)
        return 0

    if parsed_args.command == "create-package":
        try:
            content = json.loads(parsed_args.content)
        except json.JSONDecodeError as exc:
            print(f"Invalid JSON for --content: {exc}", file=sys.stderr)
            return 2
        if not isinstance(content, dict):
            print("--content must decode to a JSON object.", file=sys.stderr)
            return 2
        package_id = engine.create_package(
            name=parsed_args.name,
            domain=parsed_args.domain,
            priority=parsed_args.priority,
            content=content,
            tags=parsed_args.tag,
            references=parsed_args.reference,
        )
        package = engine.get_package(package_id)
        result = {"package": _package_summary(package), **engine.get_stats()}
        _print_result(result, parsed_args.json)
        return 0

    if parsed_args.command == "list-packages":
        packages = [_package_summary(package) for package in engine.list_packages()]
        if parsed_args.json:
            _print_result({"packages": packages, **engine.get_stats()}, parsed_args.json)
        else:
            if not packages:
                print("No packages found.")
            for package in packages:
                print(
                    f"{package['id']} {package['state']} "
                    f"{package['priority']} {package['domain']} {package['name']}"
                )
        return 0

    if parsed_args.command == "get-package":
        package = engine.get_package(parsed_args.package_id)
        if package is None:
            print(f"Package not found: {parsed_args.package_id}", file=sys.stderr)
            return 1
        result = {"package": {**_package_summary(package), "content": package.content}}
        _print_result(result, parsed_args.json)
        return 0

    if parsed_args.command == "prune":
        prune_stats = engine.prune_context(max_active_size=parsed_args.max_active_size)
        _print_result({**prune_stats, **engine.get_stats()}, parsed_args.json)
        return 0

    if parsed_args.command == "restore":
        package = engine.restore_package(parsed_args.package_id)
        if package is None:
            print(f"Package not found: {parsed_args.package_id}", file=sys.stderr)
            return 1
        _print_result({"package": _package_summary(package), **engine.get_stats()}, parsed_args.json)
        return 0

    if parsed_args.command == "prune-demo":
        engine.create_package(
            name="Current Task",
            domain="demo",
            priority=Priority.CRITICAL,
            content={"summary": "Synthetic active work package."},
            tags=["synthetic", "demo"],
        )
        engine.create_package(
            name="Reference Notes",
            domain="demo",
            priority=Priority.MEDIUM,
            content={"notes": ["Synthetic note one", "Synthetic note two"]},
            tags=["synthetic", "reference"],
        )
        engine.create_package(
            name="Historical Scratch",
            domain="demo",
            priority=Priority.LOW,
            content={"history": "Synthetic historical context " * 20},
            tags=["synthetic", "history"],
        )
        prune_stats = engine.prune_context(max_active_size=parsed_args.max_active_size)
        _print_result({**prune_stats, **engine.get_stats()}, parsed_args.json)
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
