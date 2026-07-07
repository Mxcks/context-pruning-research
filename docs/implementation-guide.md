# Implementation Guide

This guide provides step-by-step instructions for implementing the Context Pruning system in your environment.

## Prerequisites

### System Requirements
- Python 3.8 or higher
- 4GB RAM minimum (8GB recommended)
- 10GB free disk space for storage
- Modern web browser for management interface

### Dependencies
```bash
# Core dependencies
python>=3.8
jsonschema>=4.0.0
pyyaml>=6.0.0

# Storage dependencies
sqlalchemy>=2.0.0
sqlite3 (built-in) or PostgreSQL/MySQL adapter

# Web framework (if using web interface)
flask>=2.0.0 or fastapi>=0.68.0

# Testing dependencies
pytest>=6.0.0
pytest-cov>=2.10.0
```

### Installation

1. **Clone the Repository**
```bash
git clone https://github.com/your-username/context-pruning-research.git
cd context-pruning-research
```

2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

## Step 1: Basic Setup

### Configure Storage

Create a basic storage configuration:

```python
# config/storage.py
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./context_pruning.db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Define Core Models

```python
# models/package.py
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
from sqlalchemy.dialects.postgresql import JSONB
import enum
from datetime import datetime
from config.storage import Base

class PriorityEnum(enum.Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class StateEnum(enum.Enum):
    ACTIVE = "active"
    COMPRESSED = "compressed"
    DETACHED = "detached"
    ARCHIVED = "archived"

class ContextPackage(Base):
    __tablename__ = "context_packages"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    domain = Column(String, index=True)
    priority = Column(Enum(PriorityEnum))
    state = Column(Enum(StateEnum), default=StateEnum.ACTIVE)
    source = Column(String)
    created = Column(DateTime, default=datetime.utcnow)
    last_accessed = Column(DateTime, default=datetime.utcnow)
    last_modified = Column(DateTime, default=datetime.utcnow)
    size = Column(Integer, default=0)
    content = Column(JSONB)
    tags = Column(JSONB)
    references = Column(JSONB)
    metadata_ = Column("metadata", JSONB)
```

## Step 2: Implement Core Functionality

### Package Management

```python
# services/package_manager.py
import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from models.package import ContextPackage, StateEnum, PriorityEnum
import json

class PackageManager:
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def create_package(self, name: str, domain: str, priority: str, 
                      content: dict, tags: list = None, references: list = None):
        """Create a new context package"""
        package = ContextPackage(
            id=str(uuid.uuid4()),
            name=name,
            domain=domain,
            priority=PriorityEnum(priority),
            content=content,
            tags=tags or [],
            references=references or [],
            created=datetime.utcnow(),
            last_accessed=datetime.utcnow(),
            last_modified=datetime.utcnow()
        )
        
        self.db.add(package)
        self.db.commit()
        self.db.refresh(package)
        return package
    
    def get_package(self, package_id: str):
        """Retrieve a context package by ID"""
        return self.db.query(ContextPackage).filter(
            ContextPackage.id == package_id
        ).first()
    
    def update_package_state(self, package_id: str, new_state: str):
        """Update the state of a context package"""
        package = self.get_package(package_id)
        if package:
            package.state = StateEnum(new_state)
            package.last_modified = datetime.utcnow()
            self.db.commit()
            self.db.refresh(package)
        return package
    
    def delete_package(self, package_id: str):
        """Delete a context package"""
        package = self.get_package(package_id)
        if package:
            self.db.delete(package)
            self.db.commit()
            return True
        return False
```

### Tagging System

```python
# services/tag_manager.py
from sqlalchemy.orm import Session
from models.package import ContextPackage

class TagManager:
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def add_tags(self, package_id: str, tags: list):
        """Add tags to a context package"""
        package = self.db.query(ContextPackage).filter(
            ContextPackage.id == package_id
        ).first()
        
        if package:
            current_tags = package.tags or []
            for tag in tags:
                if tag not in current_tags:
                    current_tags.append(tag)
            package.tags = current_tags
            self.db.commit()
            return True
        return False
    
    def remove_tags(self, package_id: str, tags: list):
        """Remove tags from a context package"""
        package = self.db.query(ContextPackage).filter(
            ContextPackage.id == package_id
        ).first()
        
        if package:
            current_tags = package.tags or []
            for tag in tags:
                if tag in current_tags:
                    current_tags.remove(tag)
            package.tags = current_tags
            self.db.commit()
            return True
        return False
    
    def get_packages_by_tag(self, tag: str):
        """Retrieve all packages with a specific tag"""
        return self.db.query(ContextPackage).filter(
            ContextPackage.tags.contains([tag])
        ).all()
```

### Rule Engine

```python
# services/rule_engine.py
from sqlalchemy.orm import Session
from models.package import ContextPackage, StateEnum
import operator

class RuleEngine:
    def __init__(self, db_session: Session):
        self.db = db_session
        self.operators = {
            'equals': operator.eq,
            'not_equals': operator.ne,
            'contains': lambda x, y: y in x if isinstance(x, (list, str)) else False,
            'greater_than': operator.gt,
            'less_than': operator.lt
        }
    
    def evaluate_package(self, package_id: str, rules: list):
        """Evaluate a package against a set of rules"""
        package = self.db.query(ContextPackage).filter(
            ContextPackage.id == package_id
        ).first()
        
        if not package:
            return None
        
        actions = []
        
        for rule in rules:
            match_count = 0
            total_conditions = len(rule.get('conditions', []))
            
            for condition in rule.get('conditions', []):
                field_value = getattr(package, condition['field'], None)
                
                if field_value is not None:
                    op = self.operators.get(condition['operator'])
                    if op and op(field_value, condition['value']):
                        match_count += 1
            
            # If all conditions match, apply actions
            if match_count == total_conditions:
                actions.extend(rule.get('actions', []))
        
        return actions
    
    def execute_actions(self, package_id: str, actions: list):
        """Execute pruning actions on a package"""
        package = self.db.query(ContextPackage).filter(
            ContextPackage.id == package_id
        ).first()
        
        if not package:
            return False
        
        for action in actions:
            if action['type'] == 'retain':
                package.state = StateEnum.ACTIVE
            elif action['type'] == 'compress':
                package.state = StateEnum.COMPRESSED
            elif action['type'] == 'detach':
                package.state = StateEnum.DETACHED
            elif action['type'] == 'archive':
                package.state = StateEnum.ARCHIVED
            elif action['type'] == 'delete':
                self.db.delete(package)
                self.db.commit()
                return True
        
        package.last_modified = datetime.utcnow()
        self.db.commit()
        return True
```

## Step 3: Storage Optimization

### Active Context Cache

```python
# services/cache_manager.py
import threading
from collections import OrderedDict
from datetime import datetime, timedelta

class ActiveContextCache:
    def __init__(self, max_size=1000):
        self.cache = OrderedDict()
        self.max_size = max_size
        self.lock = threading.Lock()
    
    def get(self, package_id):
        """Retrieve package from cache"""
        with self.lock:
            if package_id in self.cache:
                # Move to end (most recently used)
                package = self.cache.pop(package_id)
                self.cache[package_id] = package
                return package
            return None
    
    def put(self, package_id, package):
        """Add package to cache"""
        with self.lock:
            if package_id in self.cache:
                self.cache.pop(package_id)
            elif len(self.cache) >= self.max_size:
                # Remove least recently used
                self.cache.popitem(last=False)
            
            self.cache[package_id] = {
                'data': package,
                'accessed': datetime.utcnow()
            }
    
    def cleanup_expired(self, ttl_minutes=60):
        """Remove expired entries from cache"""
        with self.lock:
            cutoff_time = datetime.utcnow() - timedelta(minutes=ttl_minutes)
            expired_keys = [
                k for k, v in self.cache.items() 
                if v['accessed'] < cutoff_time
            ]
            for key in expired_keys:
                self.cache.pop(key)
```

### Compression Strategy

```python
# services/compression_manager.py
import json
import zlib
from typing import Any

class CompressionManager:
    @staticmethod
    def compress_content(content: Any) -> bytes:
        """Compress content using zlib"""
        content_str = json.dumps(content, ensure_ascii=False)
        return zlib.compress(content_str.encode('utf-8'))
    
    @staticmethod
    def decompress_content(compressed_data: bytes) -> Any:
        """Decompress content using zlib"""
        decompressed_str = zlib.decompress(compressed_data).decode('utf-8')
        return json.loads(decompressed_str)
    
    @staticmethod
    def estimate_compression_ratio(content: Any) -> float:
        """Estimate compression ratio for content"""
        original_size = len(json.dumps(content, ensure_ascii=False).encode('utf-8'))
        compressed_size = len(CompressionManager.compress_content(content))
        return compressed_size / original_size if original_size > 0 else 0
```

## Step 4: API Implementation

### REST API Endpoints

```python
# api/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid

from config.storage import get_db
from services.package_manager import PackageManager
from services.tag_manager import TagManager
from services.rule_engine import RuleEngine
from models.package import ContextPackage

app = FastAPI(title="Context Pruning API")

def get_package_manager(db: Session = Depends(get_db)):
    return PackageManager(db)

def get_tag_manager(db: Session = Depends(get_db)):
    return TagManager(db)

def get_rule_engine(db: Session = Depends(get_db)):
    return RuleEngine(db)

@app.post("/packages/")
async def create_package(
    name: str,
    domain: str,
    priority: str,
    content: dict,
    tags: List[str] = None,
    references: List[str] = None,
    package_manager: PackageManager = Depends(get_package_manager)
):
    """Create a new context package"""
    try:
        package = package_manager.create_package(
            name=name,
            domain=domain,
            priority=priority,
            content=content,
            tags=tags,
            references=references
        )
        return {"id": package.id, "created": package.created}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/packages/{package_id}")
async def get_package(
    package_id: str,
    package_manager: PackageManager = Depends(get_package_manager)
):
    """Retrieve a context package"""
    package = package_manager.get_package(package_id)
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")
    return package

@app.put("/packages/{package_id}")
async def update_package(
    package_id: str,
    priority: str = None,
    tags: List[str] = None,
    package_manager: PackageManager = Depends(get_package_manager),
    tag_manager: TagManager = Depends(get_tag_manager)
):
    """Update a context package"""
    package = package_manager.get_package(package_id)
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")
    
    if priority:
        package.priority = priority
        package.last_modified = datetime.utcnow()
    
    if tags:
        tag_manager.add_tags(package_id, tags)
    
    return {"status": "updated"}

@app.delete("/packages/{package_id}")
async def delete_package(
    package_id: str,
    package_manager: PackageManager = Depends(get_package_manager)
):
    """Delete a context package"""
    success = package_manager.delete_package(package_id)
    if not success:
        raise HTTPException(status_code=404, detail="Package not found")
    return {"status": "deleted"}
```

## Step 5: Pruning Implementation

### Pruning Scheduler

```python
# services/pruning_scheduler.py
import schedule
import time
from datetime import datetime
from sqlalchemy.orm import Session
from services.package_manager import PackageManager
from services.rule_engine import RuleEngine

class PruningScheduler:
    def __init__(self, db_session: Session):
        self.db = db_session
        self.package_manager = PackageManager(db_session)
        self.rule_engine = RuleEngine(db_session)
    
    def schedule_pruning(self, interval_minutes: int = 30):
        """Schedule regular pruning operations"""
        schedule.every(interval_minutes).minutes.do(self.perform_pruning)
    
    def perform_pruning(self, strategy: str = "balanced"):
        """Perform a pruning operation"""
        print(f"Starting pruning operation at {datetime.now()}")
        
        # Get all active packages
        # (Implementation would depend on your specific database setup)
        # packages = self.db.query(ContextPackage).all()
        
        # Apply pruning rules
        # for package in packages:
        #     actions = self.rule_engine.evaluate_package(package.id, rules)
        #     if actions:
        #         self.rule_engine.execute_actions(package.id, actions)
        
        print(f"Pruning operation completed at {datetime.now()}")
    
    def run_scheduler(self):
        """Run the pruning scheduler"""
        while True:
            schedule.run_pending()
            time.sleep(1)
```

## Step 6: Testing and Validation

### Unit Tests

```python
# tests/test_package_manager.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.package import Base, ContextPackage
from services.package_manager import PackageManager

@pytest.fixture
def db_session():
    """Create a test database session"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_create_package(db_session):
    """Test package creation"""
    manager = PackageManager(db_session)
    
    package = manager.create_package(
        name="Test Package",
        domain="test-domain",
        priority="high",
        content={"test": "data"}
    )
    
    assert package.name == "Test Package"
    assert package.domain == "test-domain"
    assert package.priority.value == "high"

def test_get_package(db_session):
    """Test package retrieval"""
    manager = PackageManager(db_session)
    
    # Create a package
    created_package = manager.create_package(
        name="Test Package",
        domain="test-domain",
        priority="high",
        content={"test": "data"}
    )
    
    # Retrieve the package
    retrieved_package = manager.get_package(created_package.id)
    
    assert retrieved_package is not None
    assert retrieved_package.id == created_package.id
    assert retrieved_package.name == "Test Package"

def test_update_package_state(db_session):
    """Test package state update"""
    manager = PackageManager(db_session)
    
    # Create a package
    package = manager.create_package(
        name="Test Package",
        domain="test-domain",
        priority="high",
        content={"test": "data"}
    )
    
    # Update state
    updated_package = manager.update_package_state(package.id, "compressed")
    
    assert updated_package.state.value == "compressed"
```

## Step 7: Deployment

### Docker Configuration

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  context-pruning:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/context_pruning
    depends_on:
      - db
    volumes:
      - ./data:/app/data

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=context_pruning
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

## Step 8: Monitoring and Maintenance

### Health Check Endpoint

```python
# api/health.py
from fastapi import APIRouter
import psutil
import os

router = APIRouter()

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    # Get system metrics
    cpu_percent = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "system": {
            "cpu_percent": cpu_percent,
            "memory_percent": memory.percent,
            "memory_available": memory.available,
            "disk_usage": psutil.disk_usage("/").percent
        }
    }

@router.get("/metrics")
async def get_metrics():
    """Get system metrics"""
    # Implementation would depend on your specific monitoring needs
    pass
```

## Configuration Management

### Environment Configuration

```python
# config/settings.py
import os
from typing import Optional

class Settings:
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./context_pruning.db")
    
    # Storage settings
    STORAGE_PATH: str = os.getenv("STORAGE_PATH", "./data")
    MAX_ACTIVE_PACKAGES: int = int(os.getenv("MAX_ACTIVE_PACKAGES", "1000"))
    
    # Pruning settings
    PRUNING_INTERVAL_MINUTES: int = int(os.getenv("PRUNING_INTERVAL_MINUTES", "30"))
    DEFAULT_PRUNING_STRATEGY: str = os.getenv("DEFAULT_PRUNING_STRATEGY", "balanced")
    
    # Performance settings
    CACHE_SIZE: int = int(os.getenv("CACHE_SIZE", "1000"))
    COMPRESSION_ENABLED: bool = os.getenv("COMPRESSION_ENABLED", "true").lower() == "true"
    
    # Security settings
    API_KEY: Optional[str] = os.getenv("API_KEY")
    ENABLE_AUTH: bool = os.getenv("ENABLE_AUTH", "false").lower() == "true"

settings = Settings()
```

## Usage Examples

### Basic Usage

```python
# examples/basic_usage.py
from services.package_manager import PackageManager
from services.tag_manager import TagManager
from services.rule_engine import RuleEngine
from config.storage import get_db

# Initialize services
db = next(get_db())
package_manager = PackageManager(db)
tag_manager = TagManager(db)
rule_engine = RuleEngine(db)

# Create a context package
package = package_manager.create_package(
    name="Software Development Project",
    domain="software-development",
    priority="high",
    content={
        "framework": "FastAPI",
        "language": "Python",
        "requirements": ["fastapi", "sqlalchemy", "pydantic"]
    },
    tags=["backend", "api", "python"]
)

print(f"Created package: {package.id}")

# Add more tags
tag_manager.add_tags(package.id, ["urgent", "review-needed"])

# Retrieve the package
retrieved_package = package_manager.get_package(package.id)
print(f"Package tags: {retrieved_package.tags}")
```

### Advanced Pruning

```python
# examples/advanced_pruning.py
from services.rule_engine import RuleEngine
from config.storage import get_db

# Define pruning rules
rules = [
    {
        "name": "Critical System Retention",
        "conditions": [
            {"field": "domain", "operator": "equals", "value": "critical-systems"},
            {"field": "priority", "operator": "equals", "value": "critical"}
        ],
        "actions": [
            {"type": "retain", "target": "package"}
        ]
    },
    {
        "name": "Old Research Compression",
        "conditions": [
            {"field": "domain", "operator": "equals", "value": "research"},
            {"field": "last_accessed", "operator": "less_than", "value": "30_days_ago"}
        ],
        "actions": [
            {"type": "compress", "target": "package"}
        ]
    }
]

# Initialize rule engine
db = next(get_db())
rule_engine = RuleEngine(db)

# Evaluate and execute rules
# (Implementation would depend on your specific use case)
```

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Check database URL configuration
   - Verify database service is running
   - Ensure proper credentials

2. **Memory Issues**
   - Monitor active package count
   - Adjust cache size settings
   - Implement more aggressive pruning

3. **Performance Problems**
   - Optimize database indexes
   - Review rule complexity
   - Check storage I/O performance

### Debugging Tips

1. **Enable Detailed Logging**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

2. **Monitor System Resources**
```bash
# Monitor CPU and memory usage
top -p $(pgrep -f "context_pruning")

# Monitor disk usage
df -h
```

3. **Check Database Performance**
```sql
-- Check for slow queries
EXPLAIN QUERY PLAN SELECT * FROM context_packages WHERE domain = 'test';
```

## Next Steps

After implementing the basic system:

1. **Customize Rules**: Adapt pruning rules to your specific use cases
2. **Optimize Performance**: Fine-tune caching and compression strategies
3. **Add Monitoring**: Implement comprehensive metrics and alerting
4. **Enhance Security**: Add authentication and authorization
5. **Scale Deployment**: Set up load balancing and clustering

Continue to [Performance Metrics](performance-metrics.md) to understand the benefits you can expect from this implementation.