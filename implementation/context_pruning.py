#!/usr/bin/env python3
"""
Context Pruning Implementation for Base41
"""

import os
import json
import time
import hashlib
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path

class Priority(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class State(Enum):
    ACTIVE = "active"
    COMPRESSED = "compressed"
    DETACHED = "detached"
    ARCHIVED = "archived"

@dataclass
class ContextPackage:
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
    
    def __post_init__(self):
        # Calculate approximate size
        self.size = len(json.dumps(self.content, default=str))

class ContextPruningEngine:
    def __init__(self, storage_path: str = "E:/Research/Projects/base41/context-pruning-dev/storage"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True)
        self.active_context: Dict[str, ContextPackage] = {}
        self.compressed_context: Dict[str, ContextPackage] = {}
        self.detached_context: Dict[str, str] = {}  # id -> storage_path
        
    def create_package(self, name: str, domain: str, priority: Priority, 
                      content: Dict[str, Any], tags: List[str] = None, 
                      references: List[str] = None) -> str:
        """Create a new context package"""
        package_id = self._generate_id(name, domain)
        package = ContextPackage(
            id=package_id,
            name=name,
            domain=domain,
            priority=priority,
            state=State.ACTIVE,
            content=content,
            tags=tags or [],
            references=references or [],
            created_at=time.time(),
            last_accessed=time.time()
        )
        
        self.active_context[package_id] = package
        return package_id
    
    def get_package(self, package_id: str) -> Optional[ContextPackage]:
        """Retrieve a context package by ID"""
        # Check active context first
        if package_id in self.active_context:
            package = self.active_context[package_id]
            package.last_accessed = time.time()
            return package
        
        # Check compressed context
        if package_id in self.compressed_context:
            package = self.compressed_context[package_id]
            package.last_accessed = time.time()
            return package
        
        # Check detached context
        if package_id in self.detached_context:
            # Load from storage
            storage_file = self.detached_context[package_id]
            if os.path.exists(storage_file):
                with open(storage_file, 'r') as f:
                    data = json.load(f)
                package = ContextPackage(**data)
                package.last_accessed = time.time()
                return package
        
        return None
    
    def prune_context(self, max_active_size: int = 1000000) -> Dict[str, int]:
        """Prune context based on size limits and priority"""
        stats = {
            'packages_processed': len(self.active_context),
            'packages_retained': 0,
            'packages_compressed': 0,
            'packages_detached': 0
        }
        
        # Calculate current active context size
        current_size = sum(pkg.size for pkg in self.active_context.values())
        
        if current_size <= max_active_size:
            stats['packages_retained'] = len(self.active_context)
            return stats
        
        # Sort packages by priority and last accessed time
        sorted_packages = sorted(
            self.active_context.items(),
            key=lambda x: (self._priority_value(x[1].priority), x[1].last_accessed),
            reverse=True
        )
        
        # Move packages to compressed or detached storage
        retained_size = 0
        new_active_context = {}
        
        for package_id, package in sorted_packages:
            if retained_size + package.size <= max_active_size:
                # Keep in active context
                new_active_context[package_id] = package
                retained_size += package.size
                stats['packages_retained'] += 1
            elif package.priority in [Priority.CRITICAL, Priority.HIGH]:
                # Compress but keep accessible
                self.compressed_context[package_id] = package
                stats['packages_compressed'] += 1
            else:
                # Detach to storage
                self._detach_package(package_id, package)
                stats['packages_detached'] += 1
        
        self.active_context = new_active_context
        return stats
    
    def _priority_value(self, priority: Priority) -> int:
        """Convert priority to numeric value for sorting"""
        priority_map = {
            Priority.CRITICAL: 4,
            Priority.HIGH: 3,
            Priority.MEDIUM: 2,
            Priority.LOW: 1
        }
        return priority_map.get(priority, 0)
    
    def _detach_package(self, package_id: str, package: ContextPackage):
        """Move a package to detached storage"""
        # Save to file
        detached_dir = self.storage_path / "detached"
        detached_dir.mkdir(exist_ok=True)
        
        filename = f"{package_id}.json"
        storage_path = detached_dir / filename
        
        # Convert enum values to strings for JSON serialization
        package_dict = asdict(package)
        package_dict['priority'] = package.priority.value
        package_dict['state'] = State.DETACHED.value
        
        with open(storage_path, 'w') as f:
            json.dump(package_dict, f)
        
        # Update state and store reference
        package.state = State.DETACHED
        self.detached_context[package_id] = str(storage_path)
        
        # Remove from active context
        if package_id in self.active_context:
            del self.active_context[package_id]
    
    def _generate_id(self, name: str, domain: str) -> str:
        """Generate a unique ID for a package"""
        timestamp = str(time.time())
        unique_string = f"{name}-{domain}-{timestamp}"
        return hashlib.md5(unique_string.encode()).hexdigest()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current context statistics"""
        active_size = sum(pkg.size for pkg in self.active_context.values())
        compressed_size = sum(pkg.size for pkg in self.compressed_context.values())
        
        return {
            'active_packages': len(self.active_context),
            'compressed_packages': len(self.compressed_context),
            'detached_packages': len(self.detached_context),
            'active_context_size': active_size,
            'compressed_context_size': compressed_size,
            'total_packages': len(self.active_context) + len(self.compressed_context) + len(self.detached_context)
        }

# Example usage and testing
if __name__ == "__main__":
    # Create engine
    engine = ContextPruningEngine()
    
    # Create some test packages
    print("Creating test context packages...")
    
    # High priority package (should be retained)
    pkg1_id = engine.create_package(
        name="Critical System Configuration",
        domain="system-admin",
        priority=Priority.CRITICAL,
        content={
            "config": {"database_url": "postgresql://localhost/mydb", "api_key": "secret123"},
            "instructions": "This is critical system configuration that must always be available"
        },
        tags=["critical", "configuration", "system"]
    )
    
    # Medium priority package (might be compressed)
    pkg2_id = engine.create_package(
        name="User Documentation",
        domain="documentation",
        priority=Priority.MEDIUM,
        content={
            "sections": ["Introduction", "Installation", "Usage", "Troubleshooting"],
            "content": "Detailed user documentation for the system..."
        },
        tags=["documentation", "user-guide"]
    )
    
    # Low priority package (likely to be detached)
    pkg3_id = engine.create_package(
        name="Historical Logs",
        domain="logging",
        priority=Priority.LOW,
        content={
            "logs": ["2024-01-01: System started", "2024-01-02: User login", "2024-01-03: Data backup"],
            "metadata": {"total_entries": 1000, "oldest_entry": "2024-01-01"}
        },
        tags=["logs", "history", "audit"]
    )
    
    print(f"Created packages: {pkg1_id}, {pkg2_id}, {pkg3_id}")
    
    # Show initial stats
    print("\nInitial context stats:")
    stats = engine.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Prune context with small limit to force some pruning
    print("\nPruning context with 500 byte limit...")
    prune_stats = engine.prune_context(max_active_size=500)
    print("Pruning results:")
    for key, value in prune_stats.items():
        print(f"  {key}: {value}")
    
    # Show final stats
    print("\nFinal context stats:")
    final_stats = engine.get_stats()
    for key, value in final_stats.items():
        print(f"  {key}: {value}")
    
    # Test package retrieval
    print("\nTesting package retrieval:")
    for pkg_id in [pkg1_id, pkg2_id, pkg3_id]:
        pkg = engine.get_package(pkg_id)
        if pkg:
            print(f"  Package {pkg_id[:8]}...: {pkg.name} (state: {pkg.state.value})")
        else:
            print(f"  Package {pkg_id[:8]}...: Not found in active context")