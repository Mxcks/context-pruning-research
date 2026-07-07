import json

from context_pruning import ContextPruningEngine, Priority, State


def test_engine_prunes_and_restores_detached_package(tmp_path):
    engine = ContextPruningEngine(storage_path=tmp_path / "storage")

    critical_id = engine.create_package(
        name="Current Task",
        domain="demo",
        priority=Priority.CRITICAL,
        content={"summary": "keep this package active"},
        tags=["synthetic"],
    )
    low_id = engine.create_package(
        name="Historical Scratch",
        domain="demo",
        priority=Priority.LOW,
        content={"history": "synthetic historical context " * 20},
        tags=["synthetic", "history"],
    )

    stats = engine.prune_context(max_active_size=120)

    assert stats["packages_processed"] == 2
    assert stats["packages_detached"] == 1
    assert critical_id in engine.active_context or critical_id in engine.compressed_context

    restored = engine.get_package(low_id)
    assert restored is not None
    assert restored.state == State.DETACHED
    assert restored.priority == Priority.LOW
    assert restored.content["history"].startswith("synthetic historical context")


def test_engine_serializes_enum_fields(tmp_path):
    engine = ContextPruningEngine(storage_path=tmp_path / "storage")
    package_id = engine.create_package(
        name="Reference",
        domain="demo",
        priority="medium",
        content={"note": "synthetic"},
    )

    engine.prune_context(max_active_size=1)
    package_path = tmp_path / "storage" / "detached" / f"{package_id}.json"

    data = json.loads(package_path.read_text())
    assert data["priority"] == "medium"
    assert data["state"] == "detached"
    assert engine.get_package(package_id).priority == Priority.MEDIUM
