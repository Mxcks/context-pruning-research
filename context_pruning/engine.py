"""Core context pruning engine.

The engine keeps context in named packages, retains higher-priority packages in
active memory, and detaches lower-priority packages to JSON files when the
active context exceeds a configured size limit.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class Priority(Enum):
    """Retention priority for a context package."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class State(Enum):
    """Lifecycle state for a context package."""

    ACTIVE = "active"
    COMPRESSED = "compressed"
    DETACHED = "detached"
    ARCHIVED = "archived"


@dataclass
class ContextPackage:
    """A unit of context with metadata and lifecycle state."""

    id: str
    name: str
    domain: str
    priority: Priority
    state: State
    content: Dict[str, Any]
    tags: List[str]
    references: List[str]
    created_at: float
    last_accessed: float
    size: int = 0

    def __post_init__(self) -> None:
        if isinstance(self.priority, str):
            self.priority = Priority(self.priority)
        if isinstance(self.state, str):
            self.state = State(self.state)
        self.size = len(json.dumps(self.content, default=str, sort_keys=True))

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["priority"] = self.priority.value
        data["state"] = self.state.value
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ContextPackage":
        return cls(**data)


class ContextPruningEngine:
    """Manage active, compressed, and detached context packages."""

    def __init__(self, storage_path: str | Path = ".context-pruning/storage"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.active_context: Dict[str, ContextPackage] = {}
        self.compressed_context: Dict[str, ContextPackage] = {}
        self.detached_context: Dict[str, str] = {}

    def create_package(
        self,
        name: str,
        domain: str,
        priority: Priority | str,
        content: Dict[str, Any],
        tags: Optional[List[str]] = None,
        references: Optional[List[str]] = None,
    ) -> str:
        """Create a new active context package and return its ID."""

        priority_value = priority if isinstance(priority, Priority) else Priority(priority)
        package_id = self._generate_id(name, domain)
        package = ContextPackage(
            id=package_id,
            name=name,
            domain=domain,
            priority=priority_value,
            state=State.ACTIVE,
            content=content,
            tags=tags or [],
            references=references or [],
            created_at=time.time(),
            last_accessed=time.time(),
        )
        self.active_context[package_id] = package
        return package_id

    def get_package(self, package_id: str) -> Optional[ContextPackage]:
        """Retrieve a package from active, compressed, or detached storage."""

        if package_id in self.active_context:
            package = self.active_context[package_id]
            package.last_accessed = time.time()
            return package

        if package_id in self.compressed_context:
            package = self.compressed_context[package_id]
            package.last_accessed = time.time()
            return package

        storage_file = self.detached_context.get(package_id)
        if storage_file:
            path = Path(storage_file)
            if path.exists():
                package = ContextPackage.from_dict(json.loads(path.read_text()))
                package.last_accessed = time.time()
                return package

        return None

    def prune_context(self, max_active_size: int = 1_000_000) -> Dict[str, int]:
        """Prune active context based on size limits and priority."""

        stats = {
            "packages_processed": len(self.active_context),
            "packages_retained": 0,
            "packages_compressed": 0,
            "packages_detached": 0,
        }

        current_size = sum(pkg.size for pkg in self.active_context.values())
        if current_size <= max_active_size:
            stats["packages_retained"] = len(self.active_context)
            return stats

        sorted_packages = sorted(
            self.active_context.items(),
            key=lambda item: (
                self._priority_value(item[1].priority),
                item[1].last_accessed,
            ),
            reverse=True,
        )

        retained_size = 0
        new_active_context: Dict[str, ContextPackage] = {}

        for package_id, package in sorted_packages:
            if retained_size + package.size <= max_active_size:
                new_active_context[package_id] = package
                retained_size += package.size
                stats["packages_retained"] += 1
            elif package.priority in {Priority.CRITICAL, Priority.HIGH}:
                package.state = State.COMPRESSED
                self.compressed_context[package_id] = package
                stats["packages_compressed"] += 1
            else:
                self._detach_package(package_id, package)
                stats["packages_detached"] += 1

        self.active_context = new_active_context
        return stats

    def get_stats(self) -> Dict[str, Any]:
        """Return current package counts and sizes."""

        active_size = sum(pkg.size for pkg in self.active_context.values())
        compressed_size = sum(pkg.size for pkg in self.compressed_context.values())

        return {
            "active_packages": len(self.active_context),
            "compressed_packages": len(self.compressed_context),
            "detached_packages": len(self.detached_context),
            "active_context_size": active_size,
            "compressed_context_size": compressed_size,
            "total_packages": (
                len(self.active_context)
                + len(self.compressed_context)
                + len(self.detached_context)
            ),
        }

    def _priority_value(self, priority: Priority) -> int:
        return {
            Priority.CRITICAL: 4,
            Priority.HIGH: 3,
            Priority.MEDIUM: 2,
            Priority.LOW: 1,
        }.get(priority, 0)

    def _detach_package(self, package_id: str, package: ContextPackage) -> None:
        detached_dir = self.storage_path / "detached"
        detached_dir.mkdir(parents=True, exist_ok=True)

        package.state = State.DETACHED
        storage_path = detached_dir / f"{package_id}.json"
        storage_path.write_text(json.dumps(package.to_dict(), indent=2, sort_keys=True))
        self.detached_context[package_id] = str(storage_path)

    def _generate_id(self, name: str, domain: str) -> str:
        timestamp = str(time.time_ns())
        unique_string = f"{name}-{domain}-{timestamp}"
        return hashlib.sha256(unique_string.encode()).hexdigest()[:32]
