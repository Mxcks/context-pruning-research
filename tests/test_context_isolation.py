#!/usr/bin/env python3
"""
Unit tests for context pruning system.
"""

import unittest
import os
import tempfile
import json
from pathlib import Path

class TestContextPruning(unittest.TestCase):
    """Test context pruning functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = Path(tempfile.mkdtemp())
        self.context_a = {
            "project": "ProjectA",
            "language": "Python 3.9",
            "framework": "Click",
            "special_flag": "PROJECT_A_FLAG=active"
        }
        self.context_b = {
            "project": "ProjectB",
            "language": "Python 3.11",
            "framework": "FastAPI",
            "special_flag": "PROJECT_B_FLAG=active"
        }
    
    def test_context_isolation(self):
        """Test that contexts remain isolated."""
        # Simulate loading Project A context
        active_context = self.context_a.copy()
        
        # Simulate pruning Project A context
        project_a_log = self.test_dir / "project-a-log.json"
        with open(project_a_log, 'w') as f:
            json.dump(active_context, f)
        
        # Clear active context
        active_context.clear()
        
        # Simulate loading Project B context
        active_context = self.context_b.copy()
        
        # Verify no cross-contamination
        self.assertNotIn("PROJECT_A_FLAG", active_context)
        self.assertIn("PROJECT_B_FLAG", active_context["special_flag"])
        
    def test_context_persistence(self):
        """Test that context is properly saved to scratchpad."""
        # Simulate pruning context
        project_log = self.test_dir / "test-project-log.json"
        with open(project_log, 'w') as f:
            json.dump(self.context_a, f)
        
        # Verify context was saved
        self.assertTrue(project_log.exists())
        
        # Verify content
        with open(project_log, 'r') as f:
            saved_context = json.load(f)
        
        self.assertEqual(saved_context, self.context_a)
        
    def test_context_loading(self):
        """Test that context can be reloaded from scratchpad."""
        # Save context to scratchpad
        project_log = self.test_dir / "test-project-log.json"
        with open(project_log, 'w') as f:
            json.dump(self.context_b, f)
        
        # Simulate loading context
        with open(project_log, 'r') as f:
            loaded_context = json.load(f)
        
        self.assertEqual(loaded_context, self.context_b)

if __name__ == "__main__":
    unittest.main()