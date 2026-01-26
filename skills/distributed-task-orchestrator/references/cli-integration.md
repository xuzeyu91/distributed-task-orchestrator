# Claude CLI Integration Guide

## Overview

This guide covers launching real sub-agents via Claude CLI for true parallel task execution.

## Prerequisites

```powershell
# Verify Claude CLI is installed
claude --version

# If not available, refer to Anthropic documentation for installation
```

## CLI Quick Reference

| Option | Description | Example |
|--------|-------------|---------|
| `--print` | Output only, no interactive mode | `claude --print "task"` |
| `-p` | Shorthand for prompt | `claude -p "task"` |
| `--output-format` | Output format (text/json) | `--output-format json` |
| `-c, --continue` | Continue previous conversation | `claude -c -p "more"` |

---

## Single Agent Execution

### Direct Prompt

```powershell
# Simple task
claude --print "Analyze complexity: function add(a,b) { return a+b; }"

# With file content
$code = Get-Content "src/App.tsx" -Raw
claude --print "Review this code: $code"
```

### From Task File

```powershell
$task = Get-Content ".orchestrator/agent_tasks/agent-01.md" -Raw
$result = claude --print $task
$result | Out-File ".orchestrator/results/agent-01-result.md" -Encoding UTF8
```

---

## Parallel Execution

### Method 1: PowerShell Jobs

```powershell
$taskDir = ".orchestrator/agent_tasks"
$resultDir = ".orchestrator/results"

$jobs = Get-ChildItem "$taskDir/*.md" | ForEach-Object {
    $name = $_.BaseName
    Start-Job -Name $name -ScriptBlock {
        param($path, $out)
        $task = Get-Content $path -Raw
        $result = claude --print $task 2>&1
        $result | Out-File $out -Encoding UTF8
        return @{ Agent = $using:name; Success = $? }
    } -ArgumentList $_.FullName, "$resultDir/$name-result.md"
}

# Wait with progress
while ($running = ($jobs | Where-Object State -eq 'Running')) {
    $done = $jobs.Count - $running.Count
    Write-Progress -Activity "Executing" -Status "$done/$($jobs.Count)" -PercentComplete (($done / $jobs.Count) * 100)
    Start-Sleep -Seconds 1
}

# Collect results
$jobs | ForEach-Object {
    $result = Receive-Job $_
    $icon = if ($result.Success) { "✅" } else { "❌" }
    Write-Host "$icon $($_.Name)"
}

$jobs | Remove-Job
```

### Method 2: Runspace Pool (Higher Performance)

```powershell
function Invoke-ParallelAgents {
    param(
        [string]$TaskDir = ".orchestrator/agent_tasks",
        [string]$ResultDir = ".orchestrator/results",
        [int]$MaxConcurrency = 4
    )
    
    $pool = [RunspaceFactory]::CreateRunspacePool(1, $MaxConcurrency)
    $pool.Open()
    
    $runspaces = @()
    
    foreach ($file in Get-ChildItem "$TaskDir/*.md") {
        $ps = [PowerShell]::Create()
        $ps.RunspacePool = $pool
        
        [void]$ps.AddScript({
            param($path, $out)
            $task = Get-Content $path -Raw
            $result = claude --print $task
            $result | Out-File $out -Encoding UTF8
            return @{ Success = $LASTEXITCODE -eq 0 }
        }).AddParameter("path", $file.FullName).AddParameter("out", "$ResultDir/$($file.BaseName)-result.md")
        
        $runspaces += @{
            PS = $ps
            Handle = $ps.BeginInvoke()
            Name = $file.BaseName
        }
    }
    
    # Collect results
    foreach ($rs in $runspaces) {
        $result = $rs.PS.EndInvoke($rs.Handle)
        Write-Host "$(if ($result.Success) {'✅'} else {'❌'}) $($rs.Name)"
        $rs.PS.Dispose()
    }
    
    $pool.Close()
    $pool.Dispose()
}

# Usage
Invoke-ParallelAgents -MaxConcurrency 6
```

### Method 3: Bash with GNU Parallel

```bash
# Install: apt-get install parallel (or brew install parallel)

# Execute all tasks in parallel (max 4 at a time)
parallel -j4 'claude --print "$(cat {})" > .orchestrator/results/{/.}-result.md' ::: .orchestrator/agent_tasks/*.md

# With progress bar
parallel --bar -j4 'claude --print "$(cat {})" > .orchestrator/results/{/.}-result.md' ::: .orchestrator/agent_tasks/*.md
```

---

## Dependency-Aware Execution

### Topological Scheduling

```powershell
# Define task graph
$graph = @{
    "T-01" = @{ Agent = "Agent-01"; Deps = @() }
    "T-02" = @{ Agent = "Agent-02"; Deps = @("T-01") }
    "T-03" = @{ Agent = "Agent-03"; Deps = @("T-01") }
    "T-04" = @{ Agent = "Agent-04"; Deps = @("T-02", "T-03") }
}

$completed = @{}
$taskDir = ".orchestrator/agent_tasks"
$resultDir = ".orchestrator/results"

function Get-ReadyTasks($graph, $completed) {
    $graph.Keys | Where-Object {
        -not $completed.ContainsKey($_) -and
        ($graph[$_].Deps | Where-Object { -not $completed.ContainsKey($_) }).Count -eq 0
    }
}

# Execute in batches
while ($completed.Count -lt $graph.Count) {
    $ready = Get-ReadyTasks $graph $completed
    
    if (-not $ready) {
        Write-Error "Circular dependency detected"
        break
    }
    
    Write-Host "═══ Batch: $($ready -join ', ') ═══" -ForegroundColor Cyan
    
    $jobs = foreach ($taskId in $ready) {
        $agent = $graph[$taskId].Agent
        Start-Job -Name $taskId -ScriptBlock {
            param($path, $out)
            claude --print (Get-Content $path -Raw) | Out-File $out -Encoding UTF8
        } -ArgumentList "$taskDir/$agent.md", "$resultDir/$agent-result.md"
    }
    
    $jobs | Wait-Job | Out-Null
    
    foreach ($job in $jobs) {
        $completed[$job.Name] = $true
        Write-Host "  ✅ $($job.Name)" -ForegroundColor Green
    }
    
    $jobs | Remove-Job
}

Write-Host "All tasks completed!" -ForegroundColor Green
```

---

## Error Handling

### Retry with Backoff

```powershell
function Invoke-WithRetry {
    param(
        [string]$TaskFile,
        [string]$ResultFile,
        [int]$MaxRetries = 3,
        [int]$TimeoutSec = 300
    )
    
    for ($i = 1; $i -le $MaxRetries; $i++) {
        $job = Start-Job -ScriptBlock {
            param($path)
            claude --print (Get-Content $path -Raw)
        } -ArgumentList $TaskFile
        
        $completed = Wait-Job $job -Timeout $TimeoutSec
        
        if ($completed -and $job.State -eq 'Completed') {
            $result = Receive-Job $job
            Remove-Job $job
            $result | Out-File $ResultFile -Encoding UTF8
            return @{ Success = $true; Retries = $i - 1 }
        }
        
        Stop-Job $job -ErrorAction SilentlyContinue
        Remove-Job $job
        
        Write-Warning "Attempt $i/$MaxRetries failed, retrying..."
        Start-Sleep -Seconds (5 * $i)  # Exponential backoff
    }
    
    return @{ Success = $false; Retries = $MaxRetries }
}
```

### Safe Execution Wrapper

```powershell
function Invoke-AgentSafe {
    param(
        [string]$Agent,
        [string]$TaskFile,
        [string]$ResultFile,
        [string]$ErrorLog = ".orchestrator/errors.log"
    )
    
    try {
        $task = Get-Content $TaskFile -Raw
        $result = claude --print $task 2>&1
        
        if ($LASTEXITCODE -ne 0) {
            throw "CLI exit code: $LASTEXITCODE"
        }
        
        $result | Out-File $ResultFile -Encoding UTF8
        return @{ Success = $true }
    }
    catch {
        $entry = "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] $Agent failed: $($_.Exception.Message)"
        Add-Content $ErrorLog $entry
        return @{ Success = $false; Error = $_.Exception.Message }
    }
}
```

---

## Context Passing

### Inline Context

```powershell
$context = @"
## Project Info
- Language: TypeScript
- Framework: React

## Task
Analyze src/App.tsx for performance issues.
"@

claude --print $context
```

### Inject Previous Results

```powershell
# Agent-02 needs Agent-01's output
$prev = Get-Content ".orchestrator/results/agent-01-result.md" -Raw
$task = Get-Content ".orchestrator/agent_tasks/agent-02.md" -Raw

$prompt = @"
## Previous Agent Output
$prev

---

## Your Task
$task
"@

claude --print $prompt | Out-File ".orchestrator/results/agent-02-result.md"
```

---

## Result Aggregation

### AI-Powered Merge

```powershell
function Merge-Results {
    param(
        [string]$ResultDir = ".orchestrator/results",
        [string]$OutputFile = ".orchestrator/final_output.md"
    )
    
    $results = Get-ChildItem "$ResultDir/*-result.md" | ForEach-Object {
        "## $($_.BaseName)`n`n$(Get-Content $_ -Raw)"
    }
    
    $prompt = @"
Merge these sub-agent results into a coherent report:

$($results -join "`n---`n")

Requirements:
1. Create executive summary
2. Eliminate duplicates
3. Organize logically
4. List key findings
"@
    
    claude --print $prompt | Out-File $OutputFile -Encoding UTF8
    Write-Host "Report saved: $OutputFile" -ForegroundColor Green
}
```

---

## Complete Example: Code Review

```powershell
# 1. Initialize
$dir = ".orchestrator"
New-Item -ItemType Directory -Path "$dir/agent_tasks", "$dir/results" -Force | Out-Null

# 2. Create tasks
@{
    "agent-01" = "List all TypeScript files in src/ with line counts"
    "agent-02" = "Find 'any' type usage and type safety issues"
    "agent-03" = "Check for security issues (hardcoded secrets, injection risks)"
    "agent-04" = "Analyze React performance (missing useMemo, useCallback)"
} | ForEach-Object {
    $_.GetEnumerator() | ForEach-Object {
        $_.Value | Out-File "$dir/agent_tasks/$($_.Key).md" -Encoding UTF8
    }
}

# 3. Execute in parallel
Write-Host "🚀 Starting code review..." -ForegroundColor Cyan

$jobs = Get-ChildItem "$dir/agent_tasks/*.md" | ForEach-Object {
    $name = $_.BaseName
    Start-Job -Name $name -ScriptBlock {
        param($path, $out)
        claude --print (Get-Content $path -Raw) | Out-File $out -Encoding UTF8
    } -ArgumentList $_.FullName, "$dir/results/$name-result.md"
}

$jobs | Wait-Job | Out-Null
$jobs | ForEach-Object { Write-Host "✅ $($_.Name)" -ForegroundColor Green }
$jobs | Remove-Job

# 4. Aggregate
Merge-Results

Write-Host "📋 Report: $dir/final_output.md" -ForegroundColor Yellow
```
