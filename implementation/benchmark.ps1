# Context Pruning Benchmark Script for PowerShell
# This script tests the performance and effectiveness of context pruning

param(
    [string]$OutputPath = "E:/Research/Projects/base41/context-pruning-dev/benchmark_results.json"
)

# Import required modules
Add-Type -AssemblyName System.Text.Json

# Function to generate test content
function Generate-TestContent {
    param([int]$SizeKB)
    
    $sizeBytes = $SizeKB * 1024
    $numEntries = [Math]::Max(1, [Math]::Floor($sizeBytes / 100))
    
    $content = @{
        data = @()
        metadata = @{
            generated_at = (Get-Date).ToString("o")
            size_target_kb = $SizeKB
        }
    }
    
    for ($i = 0; $i -lt $numEntries; $i++) {
        $content.data += @{
            id = "item_$i"
            value = "This is test data entry number $i with some additional text to increase size"
            timestamp = (Get-Date).AddSeconds($i).ToString("o")
            properties = @{
                key1 = "value_${i}_1"
                key2 = "value_${i}_2"
                key3 = "value_${i}_3"
            }
        }
    }
    
    return $content
}

# Function to create a context package
function New-ContextPackage {
    param(
        [string]$Name,
        [string]$Domain,
        [string]$Priority,
        [hashtable]$Content,
        [string[]]$Tags,
        [string[]]$References
    )
    
    $package = @{
        id = [System.Guid]::NewGuid().ToString()
        name = $Name
        domain = $Domain
        priority = $Priority
        state = "active"
        content = $Content
        tags = $Tags
        references = $References
        created_at = (Get-Date).ToString("o")
        last_accessed = (Get-Date).ToString("o")
        size = ($Content | ConvertTo-Json -Depth 10).Length
    }
    
    return $package
}

# Function to simulate context pruning engine
function New-ContextPruningEngine {
    $engine = @{
        active_context = @{}
        compressed_context = @{}
        detached_context = @{}
        storage_path = "E:/Research/Projects/base41/context-pruning-dev/storage"
    }
    
    # Create storage directory
    if (-not (Test-Path $engine.storage_path)) {
        New-Item -ItemType Directory -Path $engine.storage_path | Out-Null
    }
    
    return $engine
}

# Function to add package to engine
function Add-PackageToEngine {
    param(
        [hashtable]$Engine,
        [hashtable]$Package
    )
    
    $Engine.active_context[$Package.id] = $Package
}

# Function to prune context
function Invoke-ContextPruning {
    param(
        [hashtable]$Engine,
        [int]$MaxActiveSize = 1000000
    )
    
    $stats = @{
        packages_processed = $Engine.active_context.Count
        packages_retained = 0
        packages_compressed = 0
        packages_detached = 0
    }
    
    # Calculate current active context size
    $currentSize = ($Engine.active_context.Values | Measure-Object -Property size -Sum).Sum
    
    if ($currentSize -le $MaxActiveSize) {
        $stats.packages_retained = $Engine.active_context.Count
        return $stats
    }
    
    # Sort packages by priority and last accessed time
    $sortedPackages = $Engine.active_context.GetEnumerator() | Sort-Object {
        # Priority mapping (critical=4, high=3, medium=2, low=1)
        $priorityValue = switch ($_.Value.priority) {
            "critical" { 4 }
            "high" { 3 }
            "medium" { 2 }
            "low" { 1 }
            default { 0 }
        }
        # Combine with last accessed time (newer = higher priority)
        $lastAccessed = [DateTime]::Parse($_.Value.last_accessed)
        return "$priorityValue-$($lastAccessed.Ticks)"
    } -Descending
    
    # Move packages to compressed or detached storage
    $retainedSize = 0
    $newActiveContext = @{}
    
    foreach ($entry in $sortedPackages) {
        $package = $entry.Value
        if (($retainedSize + $package.size) -le $MaxActiveSize) {
            # Keep in active context
            $newActiveContext[$entry.Key] = $package
            $retainedSize += $package.size
            $stats.packages_retained++
        } elseif ($package.priority -eq "critical" -or $package.priority -eq "high") {
            # Compress but keep accessible
            $Engine.compressed_context[$entry.Key] = $package
            $stats.packages_compressed++
        } else {
            # Detach to storage
            $detachedDir = Join-Path $Engine.storage_path "detached"
            if (-not (Test-Path $detachedDir)) {
                New-Item -ItemType Directory -Path $detachedDir | Out-Null
            }
            
            $filename = "$($entry.Key).json"
            $storagePath = Join-Path $detachedDir $filename
            
            # Save to file
            $package.state = "detached"
            $package | ConvertTo-Json -Depth 10 | Out-File -FilePath $storagePath -Encoding UTF8
            
            # Store reference
            $Engine.detached_context[$entry.Key] = $storagePath
            $stats.packages_detached++
        }
    }
    
    $Engine.active_context = $newActiveContext
    return $stats
}

# Function to get engine statistics
function Get-EngineStats {
    param([hashtable]$Engine)
    
    $activeSize = ($Engine.active_context.Values | Measure-Object -Property size -Sum).Sum
    $compressedSize = ($Engine.compressed_context.Values | Measure-Object -Property size -Sum).Sum
    
    return @{
        active_packages = $Engine.active_context.Count
        compressed_packages = $Engine.compressed_context.Count
        detached_packages = $Engine.detached_context.Count
        active_context_size = $activeSize
        compressed_context_size = $compressedSize
        total_packages = $Engine.active_context.Count + $Engine.compressed_context.Count + $Engine.detached_context.Count
    }
}

# Main benchmark function
function Start-Benchmark {
    Write-Host "=== Context Pruning Performance Benchmark ===" -ForegroundColor Green
    Write-Host ""
    
    # Initialize engine
    $engine = New-ContextPruningEngine
    
    # Test 1: Package Creation Performance
    Write-Host "Test 1: Package Creation Performance" -ForegroundColor Yellow
    $startTime = Get-Date
    
    $packageIds = @()
    for ($i = 0; $i -lt 100; $i++) {
        $content = Generate-TestContent -SizeKB 5
        $package = New-ContextPackage -Name "Test Package $i" -Domain "benchmark" -Priority "medium" -Content $content -Tags @("test_$i", "benchmark")
        Add-PackageToEngine -Engine $engine -Package $package
        $packageIds += $package.id
    }
    
    $creationTime = (Get-Date) - $startTime
    Write-Host "  Created 100 packages in $($creationTime.TotalSeconds.ToString("F4")) seconds"
    Write-Host "  Average creation time: $(($creationTime.TotalMilliseconds / 100).ToString("F2")) ms per package"
    
    # Test 2: Context Size Measurement
    Write-Host ""
    Write-Host "Test 2: Context Size and Memory Usage" -ForegroundColor Yellow
    $stats = Get-EngineStats -Engine $engine
    foreach ($key in $stats.Keys) {
        Write-Host "  $key`: $($stats[$key])"
    }
    
    # Test 3: Pruning Performance
    Write-Host ""
    Write-Host "Test 3: Pruning Performance" -ForegroundColor Yellow
    $startTime = Get-Date
    $pruneStats = Invoke-ContextPruning -Engine $engine -MaxActiveSize 100000
    $pruneTime = (Get-Date) - $startTime
    Write-Host "  Pruning completed in $($pruneTime.TotalSeconds.ToString("F4")) seconds"
    foreach ($key in $pruneStats.Keys) {
        Write-Host "  $key`: $($pruneStats[$key])"
    }
    
    # Test 4: Final Statistics
    Write-Host ""
    Write-Host "Test 4: Final Context Statistics" -ForegroundColor Yellow
    $finalStats = Get-EngineStats -Engine $engine
    foreach ($key in $finalStats.Keys) {
        Write-Host "  $key`: $($finalStats[$key])"
    }
    
    # Performance Summary
    Write-Host ""
    Write-Host "=== Performance Summary ===" -ForegroundColor Green
    Write-Host "  Package creation: $(($creationTime.TotalMilliseconds / 100).ToString("F2")) ms avg"
    Write-Host "  Context pruning: $($pruneTime.TotalSeconds.ToString("F4")) seconds"
    Write-Host "  Context size reduction: $(($stats.active_context_size - $finalStats.active_context_size) / 1024).ToString("F2") KB"
    
    # Return results
    return @{
        performance = @{
            package_creation_avg_ms = ($creationTime.TotalMilliseconds / 100)
            pruning_time_seconds = $pruneTime.TotalSeconds
            final_stats = $finalStats
        }
        comparison = @{
            baseline_size_kb = $stats.active_context_size / 1024
            pruned_size_kb = $finalStats.active_context_size / 1024
            size_savings_kb = ($stats.active_context_size - $finalStats.active_context_size) / 1024
            size_savings_percent = if ($stats.active_context_size -gt 0) { (($stats.active_context_size - $finalStats.active_context_size) / $stats.active_context_size) * 100 } else { 0 }
            memory_efficiency_percent = if ($stats.active_context_size -gt 0) { ($finalStats.active_context_size / $stats.active_context_size) * 100 } else { 0 }
        }
        timestamp = (Get-Date).ToString("o")
    }
}

# Run the benchmark
Write-Host "Starting Context Pruning Benchmark Suite..." -ForegroundColor Cyan

try {
    $results = Start-Benchmark
    
    # Save results to file
    $results | ConvertTo-Json -Depth 10 | Out-File -FilePath $OutputPath -Encoding UTF8
    
    Write-Host ""
    Write-Host "=== Benchmark Complete ===" -ForegroundColor Green
    Write-Host "Results saved to: $OutputPath"
    
    # Print key metrics
    Write-Host ""
    Write-Host "Key Metrics:" -ForegroundColor Yellow
    Write-Host "  Context size reduction: $($results.comparison.size_savings_percent.ToString("F1"))%"
    Write-Host "  Memory efficiency: $($results.comparison.memory_efficiency_percent.ToString("F1"))%"
    Write-Host "  Avg package creation: $($results.performance.package_creation_avg_ms.ToString("F2")) ms"
    Write-Host "  Pruning time: $($results.performance.pruning_time_seconds.ToString("F4")) seconds"
    
} catch {
    Write-Error "Benchmark failed: $($_.Exception.Message)"
    Write-Error $_.ScriptStackTrace
}