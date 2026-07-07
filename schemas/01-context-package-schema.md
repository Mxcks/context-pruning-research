# Context Package Schema

## Overview

This document defines the formal schema for context packages used in the context pruning system.

Status: draft schema aligned to the current Python package. Proposed fields and future extensions should be marked explicitly before adoption.

## JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://example.com/context-package.schema.json",
  "title": "Context Package",
  "description": "A unit of context with metadata and lifecycle state",
  "type": "object",
  "required": [
    "id",
    "name",
    "domain",
    "priority",
    "state",
    "content",
    "tags",
    "references",
    "created_at",
    "last_accessed"
  ],
  "properties": {
    "id": {
      "type": "string",
      "description": "Unique identifier for the package (32 hexadecimal characters)",
      "pattern": "^[a-f0-9]{32}$"
    },
    "name": {
      "type": "string",
      "description": "Human-readable name for the package"
    },
    "domain": {
      "type": "string",
      "description": "Primary domain tag",
      "enum": [
        "domain/software-development",
        "domain/research",
        "domain/business",
        "domain/creative",
        "domain/personal"
      ]
    },
    "priority": {
      "type": "string",
      "description": "Priority level",
      "enum": ["critical", "high", "medium", "low"]
    },
    "state": {
      "type": "string",
      "description": "Current lifecycle state",
      "enum": ["active", "compressed", "detached", "archived"]
    },
    "content": {
      "type": "object",
      "description": "Structured data content of the package",
      "additionalProperties": true
    },
    "tags": {
      "type": "array",
      "description": "Additional tags for categorization and rules",
      "items": {
        "type": "string"
      }
    },
    "references": {
      "type": "array",
      "description": "References to other packages or external resources",
      "items": {
        "type": "string"
      }
    },
    "created_at": {
      "type": "number",
      "description": "Timestamp when the package was created (Unix timestamp)"
    },
    "last_accessed": {
      "type": "number",
      "description": "Timestamp when the package was last accessed (Unix timestamp)"
    },
    "size": {
      "type": "integer",
      "description": "Approximate size in bytes",
      "minimum": 0
    }
  }
}
```

## Field Type Definitions

### id (string)
A unique identifier for the package. The current implementation generates a 32-character hexadecimal ID from package metadata and a timestamp.

### name (string)
A human-readable name for the package that describes its content. This should be descriptive but concise.

### domain (string)
The primary domain tag that categorizes the package. Must be one of the predefined domain values.

### priority (string)
The priority level that determines how the package should be handled during pruning operations.

### state (string)
The current lifecycle state of the package, which determines where it is stored and how it can be accessed.

### content (object)
The structured data content of the package. This can contain any JSON-serializable data structure.

### tags (array of strings)
Additional tags that provide more granular categorization and can be used for rule-based processing.

### references (array of strings)
References to other packages or external resources that this package depends on or relates to.

### created_at (number)
Unix timestamp indicating when the package was created.

### last_accessed (number)
Unix timestamp indicating when the package was last accessed.

### size (integer)
Approximate size of the package content in bytes. This is calculated automatically when the package is created.

## Example Package

```json
{
  "id": "2f8a3d94c8e6b2a1f5d7c3e9a8b4f6d1c2e5a9b3f8d6c4e1a7b2f9d3c8e5a1b6",
  "name": "User Authentication Module",
  "domain": "domain/software-development",
  "priority": "high",
  "state": "active",
  "content": {
    "code": "function authenticateUser(username, credential) { ... }",
    "tests": ["test1.js", "test2.js"],
    "documentation": "Implementation of user authentication"
  },
  "tags": [
    "priority/high",
    "lifecycle/active",
    "action/transform/compression-capable"
  ],
  "references": [
    "8a2b4c6d8e1f3a5c7b9d2e4f6a8c1b3d"
  ],
  "created_at": 1640995200,
  "last_accessed": 1640995200,
  "size": 1024
}
```

## Validation Rules

1. All required fields must be present
2. ID must be a valid 32-character hexadecimal identifier
3. Domain must be one of the predefined values
4. Priority must be one of: critical, high, medium, low
5. State must be one of: active, compressed, detached, archived
6. Created_at and last_accessed must be valid Unix timestamps
7. Size must be a non-negative integer
8. Tags and references must be arrays of strings

## Extensibility

The schema is designed to be extensible. Additional fields can be added to the content object without violating the schema. However, the core metadata fields should remain consistent to ensure compatibility with the context pruning engine.
