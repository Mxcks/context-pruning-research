import json

from context_pruning.cli import main


def test_cli_status_outputs_json(tmp_path, capsys):
    exit_code = main(
        [
            "status",
            "--storage-path",
            str(tmp_path / "storage"),
            "--json",
        ]
    )

    assert exit_code == 0
    assert '"active_packages": 0' in capsys.readouterr().out


def test_cli_prune_demo_uses_engine(tmp_path, capsys):
    exit_code = main(
        [
            "prune-demo",
            "--storage-path",
            str(tmp_path / "storage"),
            "--max-active-size",
            "120",
            "--json",
        ]
    )

    output = capsys.readouterr().out
    assert exit_code == 0
    assert '"packages_processed": 3' in output
    assert '"total_packages": 3' in output


def test_cli_persists_created_package_across_runs(tmp_path, capsys):
    storage = str(tmp_path / "storage")

    create_exit = main(
        [
            "create-package",
            "--storage-path",
            storage,
            "--json",
            "--name",
            "Persistent Package",
            "--domain",
            "demo",
            "--priority",
            "high",
            "--content",
            '{"note":"synthetic"}',
        ]
    )
    created = json.loads(capsys.readouterr().out)
    package_id = created["package"]["id"]

    status_exit = main(["status", "--storage-path", storage, "--json"])
    status = json.loads(capsys.readouterr().out)

    get_exit = main(["get-package", "--storage-path", storage, "--json", package_id])
    package = json.loads(capsys.readouterr().out)

    assert create_exit == 0
    assert status_exit == 0
    assert get_exit == 0
    assert status["total_packages"] == 1
    assert package["package"]["name"] == "Persistent Package"


def test_cli_prunes_and_restores_persisted_package(tmp_path, capsys):
    storage = str(tmp_path / "storage")

    main(
        [
            "create-package",
            "--storage-path",
            storage,
            "--json",
            "--name",
            "Low Priority Package",
            "--domain",
            "demo",
            "--priority",
            "low",
            "--content",
            '{"note":"synthetic content synthetic content synthetic content"}',
        ]
    )
    package_id = json.loads(capsys.readouterr().out)["package"]["id"]

    prune_exit = main(
        ["prune", "--storage-path", storage, "--json", "--max-active-size", "1"]
    )
    pruned = json.loads(capsys.readouterr().out)

    restore_exit = main(["restore", "--storage-path", storage, "--json", package_id])
    restored = json.loads(capsys.readouterr().out)

    assert prune_exit == 0
    assert restore_exit == 0
    assert pruned["packages_detached"] == 1
    assert restored["package"]["state"] == "active"
