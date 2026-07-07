# Pruning Algorithm: Phased Pruning Flow

## Overview

Status: draft algorithm. The current implementation provides priority-based active/compressed/detached transitions; emergency and maintenance pruning are proposed extensions.

The context pruning algorithm uses a phased approach to manage context size while preserving critical information. The algorithm operates in three distinct phases:

1. **Full Pruning Phase**: Comprehensive evaluation and optimization
2. **Emergency Pruning Phase**: Rapid reduction under high pressure
3. **Maintenance Pruning Phase**: Regular cleanup and optimization

## Full Pruning Phase

### Trigger Conditions
- Active context size exceeds configured limit
- Scheduled periodic pruning
- Manual initiation

### Algorithm Steps

1. **Inventory Collection**
   - Enumerate all active context packages
   - Calculate total active context size
   - Gather package metadata (priority, last accessed, tags)

2. **Priority-Based Sorting**
   - Sort packages by priority level (critical -> high -> medium -> low)
   - Within each priority level, sort by last accessed time (oldest first)

3. **Size-Based Allocation**
   - Calculate target size for each priority level
   - Critical: 40% of total allowed size
   - High: 30% of total allowed size
   - Medium: 20% of total allowed size
   - Low: 10% of total allowed size

4. **Package Transition**
   - Retain packages within allocated size limits
   - Compress packages that exceed their priority level's size limit but are high priority
   - Detach packages that exceed their priority level's size limit and are low priority

5. **Verification**
   - Confirm active context size is within limits
   - Validate all transitions were successful
   - Update statistics and metrics

## Emergency Pruning Phase

### Trigger Conditions
- Active context size exceeds 150% of configured limit
- System memory pressure detected
- Critical performance degradation

### Algorithm Steps

1. **Rapid Assessment**
   - Quick scan of active packages
   - Identify packages with `priority/low` tag

2. **Immediate Detachment**
   - Detach all low-priority packages immediately
   - Detach medium-priority packages older than 1 hour
   - Compress high-priority packages if size still exceeds limit

3. **Emergency Verification**
   - Check if size is now within emergency limits (200% of configured limit)
   - If not, detach additional packages as needed

## Maintenance Pruning Phase

### Trigger Conditions
- Scheduled daily/weekly maintenance
- System idle time detected
- Manual initiation for optimization

### Algorithm Steps

1. **Deep Analysis**
   - Comprehensive review of all context packages
   - Analysis of access patterns and usage frequency
   - Identification of optimization opportunities

2. **Optimization Actions**
   - Compress packages that haven't been accessed in 24 hours
   - Archive packages older than 7 days
   - Clean up expired references and metadata
   - Optimize storage layout for frequently accessed packages

3. **Performance Tuning**
   - Update access statistics
   - Adjust priority levels based on usage patterns
   - Optimize compression algorithms for different content types

## Configuration Parameters

### Size Limits
- `max_active_size`: Maximum allowed active context size (bytes)
- `emergency_threshold`: Size that triggers emergency pruning (percentage of max_active_size)
- `priority_allocation`: Percentage allocation for each priority level

### Timing Parameters
- `full_prune_interval`: Interval for full pruning (seconds)
- `maintenance_prune_interval`: Interval for maintenance pruning (seconds)
- `emergency_check_interval`: Interval for emergency checks (seconds)

### Transition Rules
- `compress_threshold`: Age threshold for compression (seconds)
- `detach_threshold`: Age threshold for detachment (seconds)
- `archive_threshold`: Age threshold for archiving (seconds)

## Performance Considerations

### Memory Efficiency
- Minimize memory overhead during pruning operations
- Use streaming algorithms for large packages
- Cache frequently accessed metadata

### Time Complexity
- Full pruning: O(n log n) due to sorting
- Emergency pruning: O(n) for linear scan
- Maintenance pruning: O(n) for analysis

### I/O Optimization
- Batch I/O operations to reduce disk access
- Use asynchronous I/O where possible
- Optimize storage layout for sequential access
