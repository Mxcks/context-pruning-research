# Context Packages: Schema and Lifecycle States

## Package Schema

Status: draft design aligned to the current `ContextPackage` model.

Each context package follows a standardized schema:

```json
{
  "id": "unique_identifier",
  "name": "human_readable_name",
  "domain": "domain_tag",
  "priority": "priority_level",
  "state": "lifecycle_state",
  "content": {
    "data": "structured_content"
  },
  "tags": ["tag1", "tag2", "tag3"],
  "references": ["ref1", "ref2"],
  "created_at": "timestamp",
  "last_accessed": "timestamp",
  "size": "byte_count"
}
```

### Field Descriptions

- **id**: Unique 32-character hexadecimal identifier for the package
- **name**: Human-readable name for the package
- **domain**: Primary domain tag (e.g., `domain/software-development`)
- **priority**: Priority level (`critical`, `high`, `medium`, `low`)
- **state**: Current lifecycle state (`active`, `compressed`, `detached`, `archived`)
- **content**: Structured data content of the package
- **tags**: Additional tags for categorization and rules
- **references**: References to other packages or external resources
- **created_at**: Timestamp when the package was created
- **last_accessed**: Timestamp when the package was last accessed
- **size**: Approximate size in bytes

## Lifecycle States

### Active State
- **Description**: Package is currently in active memory
- **Characteristics**: 
  - Fully accessible without additional I/O
  - Ready for immediate use
  - Counted toward active context size limits
- **Transitions**: Can transition to compressed or detached

### Compressed State
- **Description**: Package is stored in compressed format
- **Characteristics**:
  - Reduced memory footprint
  - Requires decompression for access
  - Still in memory but not immediately accessible
- **Transitions**: Can transition to active or detached

### Detached State
- **Description**: Package is stored in external storage
- **Characteristics**:
  - Minimal memory footprint (only metadata)
  - Requires I/O to access
  - Accessible by reference
- **Transitions**: Can transition to active or archived

### Archived State
- **Description**: Package is stored in long-term archival storage
- **Characteristics**:
  - Very minimal memory footprint
  - Requires significant I/O to access
  - Preserved for historical reference
- **Transitions**: Can transition to active or deleted

## State Transition Diagram

```
[Active] <-> [Compressed] -> [Detached] -> [Archived] -> [Deleted]
   ^                                            |
   +--------------------------------------------+
```

## Package Creation and Management

Packages are created through the ContextPruningEngine API and automatically assigned appropriate lifecycle states based on their tags and the current context pressure.
