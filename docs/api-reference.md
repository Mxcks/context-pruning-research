# API Reference

This document is a proposed API reference. The current repository ships a Python package and CLI, not a production API server.

## Base URL

```
https://api.contextpruning.example.com/v1
```

For local development:
```
http://localhost:8000/v1
```

## Authentication

Most proposed API endpoints would require authentication.

### Headers
```
Authorization: Bearer EXAMPLE_AUTH_VALUE
Content-Type: application/json
```

### Auth Value Management
```bash
# Generate a new auth value
POST /api-keys/
{
  "name": "Development Key",
  "permissions": ["read", "write", "admin"]
}

# Response
{
  "id": "ak_1234567890",
  "key": "cpk_abcdefghijklmnopqrstuvwxyz1234567890",
  "name": "Development Key",
  "permissions": ["read", "write", "admin"],
  "created": "2024-06-15T10:30:00Z"
}
```

## Rate Limits

API requests are limited to:
- **1000 requests per hour** for basic accounts
- **10000 requests per hour** for premium accounts
- **100 requests per minute** burst limit

Exceeding rate limits will return a `429 Too Many Requests` response.

## Error Handling

All API errors follow this format:
```json
{
  "error": {
    "code": "error_code",
    "message": "Human-readable error message",
    "details": {
      "field": "value"
    }
  }
}
```

### Common Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `invalid_request` | 400 | Invalid request parameters |
| `unauthorized` | 401 | Missing or invalid authorization value |
| `forbidden` | 403 | Insufficient permissions |
| `not_found` | 404 | Resource not found |
| `conflict` | 409 | Resource conflict |
| `rate_limited` | 429 | Rate limit exceeded |
| `internal_error` | 500 | Internal server error |

## Context Packages

### Create Package

Create a new context package.

```
POST /packages/
```

#### Request Body
```json
{
  "name": "string (required)",
  "domain": "string (required)",
  "priority": "enum: critical|high|medium|low (required)",
  "content": "object (required)",
  "tags": ["string array (optional)"],
  "references": ["string array (optional)"],
  "metadata": "object (optional)"
}
```

#### Response
```json
{
  "id": "uuid",
  "created": "ISO 8601 timestamp"
}
```

#### Example
```bash
curl -X POST https://api.contextpruning.example.com/v1/packages/ \
  -H "Authorization: Bearer EXAMPLE_AUTH_VALUE" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "CLI Tools Development",
    "domain": "software-development",
    "priority": "high",
    "content": {
      "framework": "Click",
      "language": "Python 3.9",
      "requirements": ["argparse", "configparser"]
    },
    "tags": ["cli", "python", "development"],
    "references": []
  }'
```

### Retrieve Package

Get a context package by ID.

```
GET /packages/{package_id}
```

#### Response
```json
{
  "id": "uuid",
  "name": "string",
  "domain": "string",
  "priority": "enum: critical|high|medium|low",
  "state": "enum: active|compressed|detached|archived",
  "source": "enum: user-input|generated|imported|system",
  "created": "ISO 8601 timestamp",
  "last_accessed": "ISO 8601 timestamp",
  "last_modified": "ISO 8601 timestamp",
  "size": "integer (bytes)",
  "content": "object",
  "tags": ["string array"],
  "references": ["string array"],
  "metadata": "object"
}
```

#### Example
```bash
curl -X GET https://api.contextpruning.example.com/v1/packages/a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8 \
  -H "Authorization: Bearer EXAMPLE_AUTH_VALUE"
```

### Update Package

Update an existing context package.

```
PUT /packages/{package_id}
```

#### Request Body
```json
{
  "name": "string (optional)",
  "priority": "enum: critical|high|medium|low (optional)",
  "content": "object (optional)",
  "tags": ["string array (optional)"],
  "references": ["string array (optional)"],
  "metadata": "object (optional)"
}
```

#### Response
```json
{
  "status": "updated"
}
```

### Delete Package

Delete a context package.

```
DELETE /packages/{package_id}
```

#### Response
```json
{
  "status": "deleted"
}
```

### List Packages

Get a list of context packages with optional filtering.

```
GET /packages/
```

#### Query Parameters
| Parameter | Type | Description |
|-----------|------|-------------|
| `domain` | string | Filter by domain |
| `state` | enum | Filter by state |
| `priority` | enum | Filter by priority |
| `tag` | string | Filter by tag |
| `limit` | integer | Number of results (default: 50, max: 1000) |
| `offset` | integer | Offset for pagination |

#### Response
```json
{
  "packages": [
    {
      "id": "uuid",
      "name": "string",
      "domain": "string",
      "priority": "enum",
      "state": "enum",
      "created": "ISO 8601 timestamp",
      "last_accessed": "ISO 8601 timestamp"
    }
  ],
  "total": "integer",
  "limit": "integer",
  "offset": "integer"
}
```

## Tag Management

### Add Tags to Package

Add tags to an existing context package.

```
POST /packages/{package_id}/tags
```

#### Request Body
```json
{
  "tags": ["string array (required)"]
}
```

#### Response
```json
{
  "status": "tags_added"
}
```

### Remove Tags from Package

Remove tags from an existing context package.

```
DELETE /packages/{package_id}/tags
```

#### Request Body
```json
{
  "tags": ["string array (required)"]
}
```

#### Response
```json
{
  "status": "tags_removed"
}
```

### Get Packages by Tag

Retrieve all packages with a specific tag.

```
GET /tags/{tag}/packages
```

#### Response
```json
{
  "packages": [
    {
      "id": "uuid",
      "name": "string",
      "domain": "string",
      "priority": "enum",
      "state": "enum",
      "created": "ISO 8601 timestamp"
    }
  ]
}
```

## Rule Management

### Create Rule

Create a new pruning rule.

```
POST /rules/
```

#### Request Body
```json
{
  "name": "string (required)",
  "description": "string (optional)",
  "conditions": [
    {
      "field": "string (required)",
      "operator": "enum: equals|not_equals|contains|greater_than|less_than (required)",
      "value": "any (required)",
      "weight": "number (0.0-1.0, optional)"
    }
  ],
  "actions": [
    {
      "type": "enum: retain|compress|detach|archive|delete (required)",
      "target": "enum: package|domain|tag (required)",
      "parameters": "object (optional)"
    }
  ],
  "priority": "integer (optional, default: 0)",
  "enabled": "boolean (optional, default: true)"
}
```

#### Response
```json
{
  "id": "uuid",
  "created": "ISO 8601 timestamp"
}
```

### Retrieve Rule

Get a rule by ID.

```
GET /rules/{rule_id}
```

#### Response
```json
{
  "id": "uuid",
  "name": "string",
  "description": "string",
  "conditions": [
    {
      "field": "string",
      "operator": "enum",
      "value": "any",
      "weight": "number"
    }
  ],
  "actions": [
    {
      "type": "enum",
      "target": "enum",
      "parameters": "object"
    }
  ],
  "priority": "integer",
  "enabled": "boolean",
  "created": "ISO 8601 timestamp",
  "modified": "ISO 8601 timestamp"
}
```

### Update Rule

Update an existing rule.

```
PUT /rules/{rule_id}
```

#### Request Body
```json
{
  "name": "string (optional)",
  "description": "string (optional)",
  "conditions": [
    {
      "field": "string",
      "operator": "enum",
      "value": "any",
      "weight": "number"
    }
  ],
  "actions": [
    {
      "type": "enum",
      "target": "enum",
      "parameters": "object"
    }
  ],
  "priority": "integer (optional)",
  "enabled": "boolean (optional)"
}
```

#### Response
```json
{
  "status": "updated"
}
```

### Delete Rule

Delete a rule.

```
DELETE /rules/{rule_id}
```

#### Response
```json
{
  "status": "deleted"
}
```

### List Rules

Get a list of all rules.

```
GET /rules/
```

#### Query Parameters
| Parameter | Type | Description |
|-----------|------|-------------|
| `enabled` | boolean | Filter by enabled status |
| `limit` | integer | Number of results (default: 50) |
| `offset` | integer | Offset for pagination |

#### Response
```json
{
  "rules": [
    {
      "id": "uuid",
      "name": "string",
      "description": "string",
      "priority": "integer",
      "enabled": "boolean",
      "created": "ISO 8601 timestamp"
    }
  ],
  "total": "integer",
  "limit": "integer",
  "offset": "integer"
}
```

### Evaluate Rules

Evaluate rules against a specific package.

```
POST /rules/evaluate
```

#### Request Body
```json
{
  "package_id": "uuid (required)",
  "rule_ids": ["uuid array (optional)"]
}
```

#### Response
```json
{
  "actions": [
    {
      "type": "enum",
      "target": "enum",
      "parameters": "object",
      "rule_id": "uuid",
      "reason": "string"
    }
  ]
}
```

## Pruning Operations

### Manual Pruning

Trigger a manual pruning operation.

```
POST /prune/
```

#### Request Body
```json
{
  "strategy": "enum: aggressive|balanced|conservative (optional, default: balanced)",
  "domains": ["string array (optional)"],
  "dry_run": "boolean (optional, default: false)"
}
```

#### Response
```json
{
  "packages_processed": "integer",
  "packages_retained": "integer",
  "packages_compressed": "integer",
  "packages_detached": "integer",
  "packages_archived": "integer",
  "packages_deleted": "integer",
  "execution_time_ms": "integer",
  "dry_run": "boolean"
}
```

### Pruning Status

Get the current pruning system status.

```
GET /prune/status
```

#### Response
```json
{
  "last_run": "ISO 8601 timestamp",
  "next_scheduled_run": "ISO 8601 timestamp",
  "packages_active": "integer",
  "packages_compressed": "integer",
  "packages_detached": "integer",
  "packages_archived": "integer",
  "storage_usage_bytes": "integer",
  "storage_compression_ratio": "number"
}
```

### Pruning History

Get history of pruning operations.

```
GET /prune/history
```

#### Query Parameters
| Parameter | Type | Description |
|-----------|------|-------------|
| `limit` | integer | Number of results (default: 50) |
| `offset` | integer | Offset for pagination |

#### Response
```json
{
  "operations": [
    {
      "id": "uuid",
      "started": "ISO 8601 timestamp",
      "completed": "ISO 8601 timestamp",
      "strategy": "enum",
      "packages_processed": "integer",
      "packages_retained": "integer",
      "packages_compressed": "integer",
      "packages_detached": "integer",
      "execution_time_ms": "integer"
    }
  ],
  "total": "integer",
  "limit": "integer",
  "offset": "integer"
}
```

## Reference Management

### Create Reference

Create a reference between two packages.

```
POST /references/
```

#### Request Body
```json
{
  "from_package_id": "uuid (required)",
  "to_package_id": "uuid (required)",
  "type": "enum: related|dependent|synthesized (optional, default: related)",
  "metadata": "object (optional)"
}
```

#### Response
```json
{
  "id": "uuid",
  "created": "ISO 8601 timestamp"
}
```

### Get Package References

Get all references for a package.

```
GET /packages/{package_id}/references
```

#### Response
```json
{
  "references": [
    {
      "id": "uuid",
      "from_package_id": "uuid",
      "to_package_id": "uuid",
      "type": "enum",
      "created": "ISO 8601 timestamp",
      "metadata": "object"
    }
  ]
}
```

### Delete Reference

Delete a reference.

```
DELETE /references/{reference_id}
```

#### Response
```json
{
  "status": "deleted"
}
```

## Storage Management

### Storage Status

Get storage system status and metrics.

```
GET /storage/status
```

#### Response
```json
{
  "total_space_bytes": "integer",
  "used_space_bytes": "integer",
  "free_space_bytes": "integer",
  "compression_enabled": "boolean",
  "average_compression_ratio": "number",
  "active_packages": "integer",
  "compressed_packages": "integer",
  "detached_packages": "integer"
}
```

### Storage Cleanup

Trigger storage cleanup operations.

```
POST /storage/cleanup
```

#### Request Body
```json
{
  "operation": "enum: garbage_collect|optimize|reindex (required)",
  "dry_run": "boolean (optional, default: false)"
}
```

#### Response
```json
{
  "operation": "enum",
  "packages_affected": "integer",
  "space_reclaimed_bytes": "integer",
  "execution_time_ms": "integer",
  "dry_run": "boolean"
}
```

## Monitoring and Metrics

### System Metrics

Get system performance metrics.

```
GET /metrics/system
```

#### Response
```json
{
  "timestamp": "ISO 8601 timestamp",
  "cpu_percent": "number",
  "memory_percent": "number",
  "disk_percent": "number",
  "network_in_bytes": "integer",
  "network_out_bytes": "integer",
  "requests_per_second": "number"
}
```

### Pruning Metrics

Get context pruning specific metrics.

```
GET /metrics/pruning
```

#### Response
```json
{
  "timestamp": "ISO 8601 timestamp",
  "packages_created_per_minute": "number",
  "packages_pruned_per_minute": "number",
  "average_pruning_latency_ms": "number",
  "context_window_utilization_percent": "number",
  "rule_evaluation_success_rate": "number"
}
```

### Health Check

Get system health status.

```
GET /health
```

#### Response
```json
{
  "status": "enum: healthy|degraded|unhealthy",
  "timestamp": "ISO 8601 timestamp",
  "components": {
    "database": "enum: healthy|degraded|unhealthy",
    "storage": "enum: healthy|degraded|unhealthy",
    "cache": "enum: healthy|degraded|unhealthy",
    "pruning_engine": "enum: healthy|degraded|unhealthy"
  }
}
```

## Webhooks

### Configure Webhooks

Set up webhook endpoints for real-time notifications.

```
POST /webhooks/
```

#### Request Body
```json
{
  "url": "string (required)",
  "events": ["string array (required)"],
  "secret": "string (optional, for signature verification)",
  "active": "boolean (optional, default: true)"
}
```

#### Supported Events
- `package.created`
- `package.updated`
- `package.deleted`
- `package.pruned`
- `rule.triggered`
- `storage.warning`
- `system.alert`

#### Response
```json
{
  "id": "uuid",
  "created": "ISO 8601 timestamp"
}
```

## SDKs and Libraries

### Official SDKs
- **Python**: `context-pruning-sdk-python`
- **JavaScript**: `context-pruning-sdk-js`
- **Java**: `context-pruning-sdk-java`
- **Go**: `context-pruning-sdk-go`

### Python SDK Example
```python
from context_pruning import Client

client = Client(auth_value="EXAMPLE_AUTH_VALUE")

# Create a package
package = client.packages.create(
    name="CLI Tools Development",
    domain="software-development",
    priority="high",
    content={"framework": "Click"}
)

# Add tags
client.packages.add_tags(package.id, ["cli", "python"])

# Evaluate rules
actions = client.rules.evaluate(package.id)
```

## Best Practices

### Error Handling
Always check HTTP status codes and handle errors appropriately:
```python
import requests

response = requests.get("https://api.contextpruning.example.com/v1/packages/123")

if response.status_code == 200:
    package = response.json()
elif response.status_code == 404:
    print("Package not found")
elif response.status_code == 429:
    print("Rate limit exceeded")
else:
    print(f"Error: {response.status_code}")
```

### Rate Limiting
Implement exponential backoff for rate-limited requests:
```python
import time
import requests

def make_request_with_backoff(url, max_retries=5):
    for attempt in range(max_retries):
        response = requests.get(url)
        if response.status_code == 429:
            wait_time = 2 ** attempt
            time.sleep(wait_time)
        else:
            return response
    return None
```

### Pagination
Handle paginated responses properly:
```python
def get_all_packages(client):
    all_packages = []
    offset = 0
    limit = 100
    
    while True:
        response = client.packages.list(limit=limit, offset=offset)
        packages = response["packages"]
        all_packages.extend(packages)
        
        if len(packages) < limit:
            break
            
        offset += limit
    
    return all_packages
```

Continue to [Contributing](contributing.md) to learn how to contribute to this project.
