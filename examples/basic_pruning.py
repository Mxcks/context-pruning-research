#!/usr/bin/env python3
"""
Basic Context Pruning Implementation Example

This example demonstrates a simple node-based context pruning system
that isolates project contexts and prevents cross-contamination.
"""

import os
import json
from pathlib import Path

class ContextPruningSystem:
    """A simple context pruning system with node-based isolation."""
    
    def __init__(self, base_path):
        """Initialize the context pruning system."""
        self.base_path = Path(base_path)
        self.scratchpad_path = self.base_path / "scratchpad" / "nodes"
        self.scratchpad_path.mkdir(parents=True, exist_ok=True)
        self.active_context = {}
    
    def create_node(self, node_name):
        """Create a new node for context isolation."""
        node_path = self.scratchpad_path / node_name
        node_path.mkdir(exist_ok=True)
        return node_path
    
    def load_context(self, node_name, context_data):
        """Load context data into active memory."""
        print(f"Loading context for node: {node_name}")
        self.active_context = context_data.copy()
        print(f"Active context: {self.active_context}")
    
    def prune_context(self, node_name):
        """Prune active context and save to scratchpad."""
        print(f"Pruning context for node: {node_name}")
        
        # Save context to scratchpad
        node_path = self.scratchpad_path / node_name
        log_file = node_path / "log.json"
        
        with open(log_file, 'w') as f:
            json.dump(self.active_context, f, indent=2)
        
        print(f"Context saved to: {log_file}")
        
        # Clear active context
        self.active_context.clear()
        print("Active context cleared")
        
        return log_file
    
    def restore_context(self, node_name):
        """Restore context from scratchpad."""
        print(f"Restoring context for node: {node_name}")
        
        # Load context from scratchpad
        node_path = self.scratchpad_path / node_name
        log_file = node_path / "log.json"
        
        if log_file.exists():
            with open(log_file, 'r') as f:
                self.active_context = json.load(f)
            print(f"Context restored from: {log_file}")
            print(f"Active context: {self.active_context}")
        else:
            print(f"No saved context found for node: {node_name}")
            self.active_context = {}

def main():
    """Demonstrate the context pruning system."""
    print("=== Context Pruning System Demo ===\n")
    
    # Initialize system
    system = ContextPruningSystem("E:/dev/projects/public-repos/context-pruning-research")
    
    # Create nodes
    system.create_node("project-a")
    system.create_node("project-b")
    
    # Define example contexts
    project_a_context = {
        "project": "CLI Tools",
        "language": "Python 3.9",
        "framework": "Click",
        "special_flag": "PROJECT_A_FLAG=active",
        "focus": "Command line interface development"
    }
    
    project_b_context = {
        "project": "Web API",
        "language": "Python 3.11",
        "framework": "FastAPI",
        "special_flag": "PROJECT_B_FLAG=active",
        "focus": "REST API development"
    }
    
    # Demo 1: Load and prune Project A context
    print("1. Loading Project A context:")
    system.load_context("project-a", project_a_context)
    print()
    
    print("2. Pruning Project A context:")
    system.prune_context("project-a")
    print()
    
    # Demo 2: Load and prune Project B context
    print("3. Loading Project B context:")
    system.load_context("project-b", project_b_context)
    print()
    
    print("4. Pruning Project B context:")
    system.prune_context("project-b")
    print()
    
    # Demo 3: Verify isolation
    print("5. Verifying context isolation:")
    if not system.active_context:
        print("✅ SUCCESS: No active context (properly pruned)")
    else:
        print("❌ FAILURE: Context still active")
    print()
    
    # Demo 4: Restore context
    print("6. Restoring Project A context:")
    system.restore_context("project-a")
    print()
    
    print("7. Restoring Project B context:")
    system.restore_context("project-b")
    print()
    
    print("=== Demo Complete ===")

if __name__ == "__main__":
    main()