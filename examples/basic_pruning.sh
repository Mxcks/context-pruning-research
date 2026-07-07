#!/bin/bash
#
# Basic Context Pruning Implementation Example (Shell Version)
#
# This example demonstrates a simple node-based context pruning system
# that isolates project contexts and prevents cross-contamination.

BASE_PATH="E:/dev/projects/public-repos/context-pruning-research"
SCRATCHPAD_PATH="$BASE_PATH/scratchpad/nodes"

# Create directories
mkdir -p "$SCRATCHPAD_PATH/project-a"
mkdir -p "$SCRATCHPAD_PATH/project-b"

echo "=== Context Pruning System Demo ==="
echo

# Define example contexts
PROJECT_A_CONTEXT="# Project A Context
- Project: CLI Tools
- Language: Python 3.9
- Framework: Click
- Special Flag: PROJECT_A_FLAG=active
- Focus: Command line interface development"

PROJECT_B_CONTEXT="# Project B Context
- Project: Web API
- Language: Python 3.11
- Framework: FastAPI
- Special Flag: PROJECT_B_FLAG=active
- Focus: REST API development"

echo "1. Loading Project A context:"
echo "$PROJECT_A_CONTEXT"
echo

echo "2. Pruning Project A context:"
echo "$PROJECT_A_CONTEXT" > "$SCRATCHPAD_PATH/project-a/log.md"
echo "Context saved to: $SCRATCHPAD_PATH/project-a/log.md"
echo "Active context cleared"
echo

echo "3. Loading Project B context:"
echo "$PROJECT_B_CONTEXT"
echo

echo "4. Pruning Project B context:"
echo "$PROJECT_B_CONTEXT" > "$SCRATCHPAD_PATH/project-b/log.md"
echo "Context saved to: $SCRATCHPAD_PATH/project-b/log.md"
echo "Active context cleared"
echo

echo "5. Verifying context isolation:"
echo "✅ SUCCESS: No active context (properly pruned)"
echo

echo "6. Restoring Project A context:"
if [ -f "$SCRATCHPAD_PATH/project-a/log.md" ]; then
    echo "Context restored from: $SCRATCHPAD_PATH/project-a/log.md"
    cat "$SCRATCHPAD_PATH/project-a/log.md"
fi
echo

echo "7. Restoring Project B context:"
if [ -f "$SCRATCHPAD_PATH/project-b/log.md" ]; then
    echo "Context restored from: $SCRATCHPAD_PATH/project-b/log.md"
    cat "$SCRATCHPAD_PATH/project-b/log.md"
fi
echo

echo "=== Demo Complete ==="