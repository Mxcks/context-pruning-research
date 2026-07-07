# Core Concepts

## 1. Context Packages

Context Packages are the fundamental building blocks of the Context Pruning system. Rather than treating individual messages or tokens as context units, we group related information into named packages with explicit metadata.

### Package Structure
```json
{
  "id": "project-cli-tools-2024-06",
  "name": "CLI Tools Development",
  "domain": "software-development",
  "priority": "high",
  "state": "active",
  "source": "user-interaction",
  "created": "2024-06-15T10:30:00Z",
  "last_accessed": "2024-06-15T14:22:00Z",
  "content": {
    "framework": "Click",
    "language": "Python 3.9",
    "requirements": ["argparse", "configparser"],
    "architecture": "modular command structure"
  },
  "tags": ["cli", "python", "development", "tools"],
  "references": ["project-web-api-2024-06"]
}
```

### Package Lifecycle
Context Packages transition through explicit states:
1. **Active**: Currently in the model's working context
2. **Compressed**: Reduced in size but still accessible
3. **Detached**: Moved to persistent storage but addressable
4. **Garbage**: Marked for eventual deletion

## 2. Tagging System

The tagging system is the heart of Context Pruning. Instead of numerical scores, we use structured metadata to drive context management decisions.

### Tag Categories
- **Domain**: The area of work (e.g., software-development, research, creative-writing)
- **Priority**: Importance level (e.g., critical, high, medium, low)
- **State**: Current lifecycle state (e.g., active, compressed, detached)
- **Source**: Origin of the context (e.g., user-input, research, generated-content)
- **Content-Type**: Type of information (e.g., requirements, code, documentation)

### Tag-Based Rules
Rules are defined as:
```
IF domain = "software-development" AND priority = "critical"
THEN retain_in_active_context = true

IF domain = "research" AND last_accessed > 24 hours ago
THEN compress_package = true

IF state = "detached" AND last_referenced > 30 days ago
THEN mark_for_garbage_collection = true
```

## 3. Pruning Algorithm

The pruning algorithm operates in phases, applying rules deterministically:

### Phase 1: Assessment
1. Inventory all active context packages
2. Apply domain-based filtering rules
3. Calculate resource usage metrics

### Phase 2: Selection
1. Apply priority-based retention rules
2. Identify packages for compression
3. Determine packages for detachment

### Phase 3: Execution
1. Compress selected packages
2. Detach packages to persistent storage
3. Update package metadata and references

### Phase 4: Verification
1. Validate that critical context remains accessible
2. Ensure no cross-domain contamination
3. Confirm resource usage within limits

## 4. Memory Integration

Context Pruning integrates with existing memory systems through well-defined interfaces:

### Active Memory
- Contains currently relevant context packages
- Directly accessible by the model
- Managed by the pruning algorithm

### Compressed Memory
- Reduced-size representations of less-frequently-used packages
- Accessible with minimal decompression overhead
- Maintains key metadata for quick retrieval

### Persistent Storage
- Detached packages stored in long-term memory
- Addressable by unique identifiers
- Accessible on-demand without model context limits

## 5. Reference-Based Access

One of the key innovations of Context Pruning is that detached context remains addressable:

### Direct References
```
User: "Can you remind me about the CLI architecture we discussed?"
Model: "Referencing package 'project-cli-tools-2024-06'..."
[Package content is restored to active context]
```

### Indirect References
```
User: "How does this relate to the web API project?"
Model: "Based on reference 'project-web-api-2024-06' in your CLI tools context..."
[Related package is retrieved and compared]
```

## 6. Composable Boundaries

Context Pruning enables clean separation between different work domains:

### Domain Isolation
- Packages from different domains don't interfere
- Domain-specific rules can be applied independently
- Cross-domain references are explicit and controlled

### Boundary Management
- Domains can be toggled on/off as atomic units
- Context switching between domains is deterministic
- No information bleeding between unrelated projects

Continue to [Technical Specification](technical-spec.md) for detailed implementation details.