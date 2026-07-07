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
