# Tag Bundle Examples

## Overview

This document provides six worked examples of tag bundles and their lifecycle behavior in the context pruning system.

Status: illustrative examples. These bundles describe intended lifecycle behavior and may require additional rule-engine features beyond the current minimal package API.

## Example 1: Software Development Task

### Tags
```
domain/software-development
priority/high
lifecycle/active
action/transform/compression-capable
action/retain/temporal-boundary:2024-12-31
```

### Behavior
- Package is kept in active memory due to high priority
- Can be compressed if memory pressure occurs
- Will be retained until December 31, 2024
- Part of the software development domain

### Lifecycle Path
Active -> Compressed (if needed) -> Detached (after deadline) -> Archived (for historical reference)

## Example 2: Research Paper Analysis

### Tags
```
domain/research
priority/critical
lifecycle/active
action/retain/temporal-boundary:indefinite
action/archive/long-term
```

### Behavior
- Package is critical and always kept in active memory
- Retained indefinitely due to research value
- Will be archived for long-term preservation
- Part of the research domain

### Lifecycle Path
Active -> Compressed (only under extreme pressure) -> Never detached -> Archived (for long-term storage)

## Example 3: Meeting Notes

### Tags
```
domain/business
priority/medium
lifecycle/active
action/detach/reference-only
action/delete/ttl-expired:7_days
```

### Behavior
- Package has medium priority
- Detached after initial use but remains referenceable
- Automatically deleted after 7 days
- Part of the business domain

### Lifecycle Path
Active -> Detached (after 1 day) -> Deleted (after 7 days total)

## Example 4: Creative Writing Draft

### Tags
```
domain/creative
priority/low
lifecycle/active
action/detach/reference-only
action/archive/long-term
```

### Behavior
- Package has low priority
- Detached quickly to free up active memory
- Archived for potential future use
- Part of the creative domain

### Lifecycle Path
Active -> Detached (within hours) -> Archived (for long-term storage)

## Example 5: System Logs

### Tags
```
domain/software-development
priority/low
lifecycle/active
action/detach/reference-only
action/delete/ttl-expired:1_day
```

### Behavior
- Package has low priority
- Detached quickly as logs are not frequently accessed
- Automatically deleted after 1 day
- Part of the software development domain

### Lifecycle Path
Active -> Detached (within minutes) -> Deleted (after 1 day total)

## Example 6: User Documentation

### Tags
```
domain/software-development
priority/high
lifecycle/active
action/transform/compression-capable
action/archive/long-term
```

### Behavior
- Package has high priority as it's frequently referenced
- Can be compressed to save space
- Archived for long-term preservation
- Part of the software development domain

### Lifecycle Path
Active -> Compressed (if needed) -> Detached (under extreme pressure) -> Archived (for long-term storage)

## Tag Bundle Design Patterns

### Pattern 1: Time-Bounded Critical Information
```
priority/critical
action/retain/temporal-boundary:<date>
action/archive/long-term
```
Used for information that is critical now but will become historical after a specific date.

### Pattern 2: Frequently Accessed Reference Material
```
priority/high
action/transform/compression-capable
action/archive/long-term
```
Used for information that is accessed regularly but can be compressed to save space.

### Pattern 3: Ephemeral Working Data
```
priority/low
action/detach/reference-only
action/delete/ttl-expired:<duration>
```
Used for temporary data that is only needed for a short period.

### Pattern 4: Archival-Only Content
```
priority/medium
action/detach/reference-only
action/archive/long-term
```
Used for content that is rarely accessed but should be preserved indefinitely.

## Best Practices

### 1. Consistent Domain Tagging
Always include a domain tag to ensure proper categorization and prevent cross-domain contamination.

### 2. Appropriate Priority Assignment
Assign priority based on actual usage patterns and business requirements, not perceived importance.

### 3. Realistic TTL Settings
Set time-to-live values based on actual retention requirements, not arbitrary defaults.

### 4. Action Tag Completeness
Include all relevant action tags to ensure the pruning engine can make optimal decisions.

### 5. Regular Review
Periodically review tag bundles to ensure they still reflect current usage patterns and requirements.
