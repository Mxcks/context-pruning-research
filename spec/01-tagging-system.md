# Tagging System and Lifecycle Engine

## Tag Taxonomy

Status: draft design. The current package supports free-form tags, priorities, and lifecycle states; the rule expressions below describe intended behavior for future rule-engine work.

The tagging system uses a hierarchical structure to categorize context information:

### Domain Tags
- `domain/software-development` - Code, documentation, and technical tasks
- `domain/research` - Academic papers, literature reviews, and analysis
- `domain/business` - Strategic planning, financial data, and market analysis
- `domain/creative` - Writing, design, and artistic projects
- `domain/personal` - Notes, reminders, and personal information

### Priority Tags
- `priority/critical` - Must be retained at all costs
- `priority/high` - Important but can be compressed if needed
- `priority/medium` - Standard retention, compressed under pressure
- `priority/low` - Can be detached when space is needed

### Lifecycle Tags
- `lifecycle/active` - Currently in use
- `lifecycle/compressed` - Stored in compressed format
- `lifecycle/detached` - Moved to external storage
- `lifecycle/archived` - Preserved for historical reference
- `lifecycle/expired` - Scheduled for deletion

### Action Tags
- `action/transform/compression-capable` - Can be compressed without loss
- `action/retain/temporal-boundary` - Retain until specific time/event
- `action/detach/reference-only` - Move to detached storage, keep reference
- `action/archive/long-term` - Move to archive storage
- `action/delete/ttl-expired` - Delete after time-to-live expires

## Lifecycle Engine

The lifecycle engine processes tags according to predefined rules:

1. **Evaluation Phase**: Check all packages against retention rules
2. **Transition Phase**: Move packages between lifecycle states
3. **Cleanup Phase**: Remove expired or unnecessary packages

### Transition Rules

```
IF priority/critical AND lifecycle/active THEN retain
IF priority/high AND context_size > threshold THEN compress
IF priority/medium AND last_accessed > 7_days THEN detach
IF priority/low AND last_accessed > 1_day THEN detach
IF action/delete/ttl-expired THEN garbage_collect
```

## Implementation Details

The engine uses a rule-based approach where each tag has associated actions that determine how context packages are handled during pruning operations.
