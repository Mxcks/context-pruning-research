import copy

import pytest

from implementation.benchmark import BENCHMARK_EXPECTATIONS, validate_results


def _valid_benchmark_results():
    return {
        "performance": {
            "initial_stats": {
                "active_packages": BENCHMARK_EXPECTATIONS["performance_created_packages"],
                "active_context_size": BENCHMARK_EXPECTATIONS[
                    "performance_prune_limit_bytes"
                ]
                + 1,
            },
            "first_prune_stats": {"packages_detached": 10},
            "large_prune_stats": {"packages_detached": 5},
            "final_stats": {
                "active_context_size": BENCHMARK_EXPECTATIONS[
                    "large_prune_limit_bytes"
                ],
                "detached_packages": 15,
                "total_packages": BENCHMARK_EXPECTATIONS[
                    "performance_created_packages"
                ]
                + BENCHMARK_EXPECTATIONS["performance_large_packages"],
            },
        },
        "comparison": {
            "baseline_stats": {
                "active_packages": BENCHMARK_EXPECTATIONS[
                    "comparison_created_packages"
                ],
            },
            "pruned_stats": {
                "active_context_size": BENCHMARK_EXPECTATIONS[
                    "comparison_prune_limit_bytes"
                ],
            },
            "prune_stats": {"packages_detached": 100},
            "size_savings_kb": 10,
            "size_savings_percent": 10,
        },
    }


def test_benchmark_validator_accepts_expected_shape():
    validate_results(_valid_benchmark_results())


def test_benchmark_validator_rejects_missing_detachment():
    results = copy.deepcopy(_valid_benchmark_results())
    results["comparison"]["prune_stats"]["packages_detached"] = 0

    with pytest.raises(AssertionError):
        validate_results(results)
