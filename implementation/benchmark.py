#!/usr/bin/env python3
"""
Benchmarking script for Context Pruning Implementation
"""

import time
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from context_pruning import ContextPruningEngine, Priority

def generate_test_content(size_kb: int) -> dict:
    """Generate test content of approximately the specified size in KB"""
    size_bytes = size_kb * 1024
    # Each entry is roughly 100 bytes, so we need size_bytes/100 entries
    num_entries = max(1, size_bytes // 100)
    
    content = {
        "data": [],
        "metadata": {
            "generated_at": time.time(),
            "size_target_kb": size_kb
        }
    }
    
    for i in range(num_entries):
        content["data"].append({
            "id": f"item_{i}",
            "value": f"This is test data entry number {i} with some additional text to increase size",
            "timestamp": time.time() + i,
            "properties": {
                "key1": f"value_{i}_1",
                "key2": f"value_{i}_2",
                "key3": f"value_{i}_3"
            }
        })
    
    return content

def run_performance_test():
    """Run performance tests on the context pruning engine"""
    print("=== Context Pruning Performance Benchmark ===\n")
    
    # Initialize engine
    temp_dir = tempfile.TemporaryDirectory()
    engine = ContextPruningEngine(storage_path=Path(temp_dir.name) / "performance")
    
    # Test 1: Package Creation Performance
    print("Test 1: Package Creation Performance")
    start_time = time.time()
    
    package_ids = []
    for i in range(100):
        pkg_id = engine.create_package(
            name=f"Test Package {i}",
            domain="benchmark",
            priority=Priority.MEDIUM,
            content=generate_test_content(5),  # 5KB each
            tags=[f"test_{i}", "benchmark"]
        )
        package_ids.append(pkg_id)
    
    creation_time = time.time() - start_time
    print(f"  Created 100 packages in {creation_time:.4f} seconds")
    print(f"  Average creation time: {creation_time/100*1000:.2f} ms per package")
    
    # Test 2: Context Size Measurement
    print("\nTest 2: Context Size and Memory Usage")
    stats = engine.get_stats()
    print(f"  Active packages: {stats['active_packages']}")
    print(f"  Active context size: {stats['active_context_size']} bytes ({stats['active_context_size']/1024:.2f} KB)")
    print(f"  Compressed packages: {stats['compressed_packages']}")
    print(f"  Detached packages: {stats['detached_packages']}")
    
    # Test 3: Pruning Performance
    print("\nTest 3: Pruning Performance")
    start_time = time.time()
    prune_stats = engine.prune_context(max_active_size=100000)  # 100KB limit
    prune_time = time.time() - start_time
    print(f"  Pruning completed in {prune_time:.4f} seconds")
    print(f"  Packages retained: {prune_stats['packages_retained']}")
    print(f"  Packages compressed: {prune_stats['packages_compressed']}")
    print(f"  Packages detached: {prune_stats['packages_detached']}")
    
    # Test 4: Package Retrieval Performance
    print("\nTest 4: Package Retrieval Performance")
    retrieval_times = []
    
    # Test retrieval of active packages
    active_packages = list(engine.active_context.keys())[:10]  # Test first 10
    if active_packages:  # Only run if we have active packages
        start_time = time.time()
        for pkg_id in active_packages:
            engine.get_package(pkg_id)
        active_retrieval_time = time.time() - start_time
        print(f"  Retrieved {len(active_packages)} active packages in {active_retrieval_time:.4f} seconds")
        print(f"  Average active retrieval: {active_retrieval_time/len(active_packages)*1000:.2f} ms per package")
    else:
        print("  No active packages to retrieve")
        active_retrieval_time = 0
    
    # Test retrieval of compressed packages
    compressed_packages = list(engine.compressed_context.keys())[:10]  # Test first 10
    if compressed_packages:  # Only run if we have compressed packages
        start_time = time.time()
        for pkg_id in compressed_packages:
            engine.get_package(pkg_id)
        compressed_retrieval_time = time.time() - start_time
        print(f"  Retrieved {len(compressed_packages)} compressed packages in {compressed_retrieval_time:.4f} seconds")
        print(f"  Average compressed retrieval: {compressed_retrieval_time/len(compressed_packages)*1000:.2f} ms per package")
    else:
        print("  No compressed packages to retrieve")
        compressed_retrieval_time = 0
    
    # Test 5: Large Context Handling
    print("\nTest 5: Large Context Handling")
    # Create a few very large packages
    large_package_ids = []
    for i in range(5):
        pkg_id = engine.create_package(
            name=f"Large Package {i}",
            domain="large-data",
            priority=Priority.LOW,
            content=generate_test_content(50),  # 50KB each
            tags=[f"large_{i}", "benchmark"]
        )
        large_package_ids.append(pkg_id)
    
    print(f"  Created 5 large packages (50KB each)")
    large_stats = engine.get_stats()
    print(f"  Total context size: {large_stats['active_context_size']/1024:.2f} KB")
    
    # Prune with very small limit to force detachment
    start_time = time.time()
    prune_stats = engine.prune_context(max_active_size=50000)  # 50KB limit
    large_prune_time = time.time() - start_time
    print(f"  Pruned large context in {large_prune_time:.4f} seconds")
    print(f"  Packages detached due to size: {prune_stats['packages_detached']}")
    
    # Final statistics
    print("\n=== Final Benchmark Results ===")
    final_stats = engine.get_stats()
    print(f"Context Statistics:")
    for key, value in final_stats.items():
        print(f"  {key}: {value}")
    
    # Performance Summary
    print(f"\nPerformance Summary:")
    print(f"  Package creation: {creation_time/100*1000:.2f} ms avg")
    
    if active_packages:
        active_avg = active_retrieval_time/len(active_packages)*1000
        print(f"  Active package retrieval: {active_avg:.2f} ms avg")
    else:
        print("  Active package retrieval: N/A (no active packages)")

    if compressed_packages:
        compressed_avg = compressed_retrieval_time/len(compressed_packages)*1000
        print(f"  Compressed package retrieval: {compressed_avg:.2f} ms avg")
    else:
        print("  Compressed package retrieval: N/A (no compressed packages)")

    results = {
        "package_creation_avg_ms": creation_time/100*1000,
        "pruning_time_seconds": prune_time,
        "active_retrieval_avg_ms": (active_retrieval_time/len(active_packages)*1000) if active_packages else 0,
        "compressed_retrieval_avg_ms": (compressed_retrieval_time/len(compressed_packages)*1000) if compressed_packages else 0,
        "final_stats": final_stats
    }
    temp_dir.cleanup()
    return results

def run_comparison_test():
    """Compare context pruning vs no pruning"""
    print("\n=== Context Pruning vs No Pruning Comparison ===\n")
    
    temp_dir = tempfile.TemporaryDirectory()

    # Test without pruning (baseline)
    print("Baseline Test (No Pruning):")
    engine_baseline = ContextPruningEngine(storage_path=Path(temp_dir.name) / "baseline")
    
    # Create many packages
    for i in range(200):
        engine_baseline.create_package(
            name=f"Baseline Package {i}",
            domain="baseline",
            priority=Priority.MEDIUM,
            content=generate_test_content(10),  # 10KB each
            tags=[f"baseline_{i}"]
        )
    
    baseline_stats = engine_baseline.get_stats()
    print(f"  Active context size: {baseline_stats['active_context_size']/1024:.2f} KB")
    print(f"  Active packages: {baseline_stats['active_packages']}")
    
    # Test with pruning
    print("\nPruned Test (With Context Pruning):")
    engine_pruned = ContextPruningEngine(storage_path=Path(temp_dir.name) / "pruned")
    
    # Create same packages
    for i in range(200):
        engine_pruned.create_package(
            name=f"Pruned Package {i}",
            domain="pruned",
            priority=Priority.MEDIUM,
            content=generate_test_content(10),  # 10KB each
            tags=[f"pruned_{i}"]
        )
    
    # Prune to 50KB limit
    prune_stats = engine_pruned.prune_context(max_active_size=50000)
    pruned_stats = engine_pruned.get_stats()
    
    print(f"  Active context size: {pruned_stats['active_context_size']/1024:.2f} KB")
    print(f"  Active packages: {pruned_stats['active_packages']}")
    print(f"  Compressed packages: {pruned_stats['compressed_packages']}")
    print(f"  Detached packages: {pruned_stats['detached_packages']}")
    print(f"  Packages detached: {prune_stats['packages_detached']}")
    
    # Calculate savings
    if baseline_stats['active_context_size'] > 0:
        size_savings_kb = (baseline_stats['active_context_size'] - pruned_stats['active_context_size']) / 1024
        size_savings_percent = (size_savings_kb / (baseline_stats['active_context_size'] / 1024)) * 100
        memory_efficiency = (pruned_stats['active_context_size'] / baseline_stats['active_context_size'] * 100)
    else:
        size_savings_kb = 0
        size_savings_percent = 0
        memory_efficiency = 0
    
    print(f"\nSavings:")
    print(f"  Size reduction: {size_savings_kb:.2f} KB ({size_savings_percent:.1f}%)")
    print(f"  Memory efficiency: {memory_efficiency:.1f}% of baseline")
    
    results = {
        "baseline_size_kb": baseline_stats['active_context_size'] / 1024 if baseline_stats['active_context_size'] > 0 else 0,
        "pruned_size_kb": pruned_stats['active_context_size'] / 1024 if pruned_stats['active_context_size'] > 0 else 0,
        "size_savings_kb": size_savings_kb,
        "size_savings_percent": size_savings_percent,
        "memory_efficiency_percent": memory_efficiency
    }
    temp_dir.cleanup()
    return results

if __name__ == "__main__":
    print("Starting Context Pruning Benchmark Suite...")
    
    # Run performance tests
    performance_results = run_performance_test()
    
    # Run comparison tests
    comparison_results = run_comparison_test()
    
    # Save results
    results = {
        "performance": performance_results,
        "comparison": comparison_results,
        "timestamp": time.time()
    }
    
    # Save to file
    results_file = "benchmark_results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n=== Benchmark Complete ===")
    print(f"Results saved to: {results_file}")
    
    # Print key metrics
    print(f"\nKey Metrics:")
    print(f"  Context size reduction: {comparison_results['size_savings_percent']:.1f}%")
    print(f"  Memory efficiency: {comparison_results['memory_efficiency_percent']:.1f}%")
    print(f"  Avg package creation: {performance_results['package_creation_avg_ms']:.2f} ms")
    print(f"  Pruning time: {performance_results['pruning_time_seconds']:.4f} seconds")
