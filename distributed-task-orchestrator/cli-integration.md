# Claude CLI Deep Integration Guide

## Overview

This guide provides detailed instructions on launching sub-agents through Claude CLI to execute tasks, enabling true distributed task processing.

## Claude CLI Basics

### Installation Verification

```powershell
# Check if Claude CLI is available
claude --version

# If not installed, install via npm
npm install -g @anthropic-ai/claude-cli
```

### Basic Command Format

```bash
claude [options] [prompt]
```

### Common Parameters

| Parameter | Short | Description | Example |
|-----------|-------|-------------|---------|
| `--prompt` | `-p` | Pass prompt text directly | `claude -p "Task"` |
| `--output-format` | | Output format (text/json) | `--output-format json` |
| `--continue` | `-c` | Continue previous conversation | `claude -c -p "Continue"` |
| `--print` | | Print only, no interactive mode | `claude --print -p "Q"` |
| `--verbose` | `-v` | Verbose output | `claude -v` |

---

## Single Agent Execution

### Method 1: Direct Execution

```powershell
# Simple task
claude -p "Analyze the complexity of this code: function add(a,b) { return a+b; }"

# Task with context
$context = Get-Content "context.md" -Raw
claude -p "Complete task based on: $context"
```

### Method 2: Read Task from File

```powershell
# Read and execute task file
$task = Get-Content ".orchestrator/agent_tasks/agent-01.md" -Raw
claude -p $task

# Save result
claude -p $task | Out-File ".orchestrator/results/agent-01-result.md" -Encoding UTF8
```

### Method 3: Using Pipes

```powershell
# Pipe input
Get-Content "task.md" | claude -p -

# Chain processing
Get-Content "data.json" | claude -p "Analyze this JSON" | Out-File "analysis.md"
```

---

## Parallel Execution

### Windows PowerShell Jobs

```powershell
# Launch multiple Agents in parallel
$taskFiles = Get-ChildItem ".orchestrator/agent_tasks/*.md"

$jobs = foreach ($file in $taskFiles) {
    $agentId = $file.BaseName
    
    Start-Job -Name $agentId -ScriptBlock {
        param($taskPath, $resultPath)
        
        $task = Get-Content $taskPath -Raw
        $result = claude -p $task 2>&1
        $result | Out-File $resultPath -Encoding UTF8
        
        return @{
            Agent = $using:agentId
            Success = $LASTEXITCODE -eq 0
            Output = $result
        }
    } -ArgumentList $file.FullName, ".orchestrator/results/$agentId-result.md"
}

# Display real-time progress
while ($jobs | Where-Object { $_.State -eq 'Running' }) {
    $running = ($jobs | Where-Object { $_.State -eq 'Running' }).Count
    $completed = ($jobs | Where-Object { $_.State -eq 'Completed' }).Count
    Write-Progress -Activity "Executing" -Status "$completed/$($jobs.Count)" -PercentComplete (($completed/$jobs.Count)*100)
    Start-Sleep -Seconds 1
}

# Collect results
$results = $jobs | Wait-Job | Receive-Job

$results | ForEach-Object {
    if ($_.Success) {
        Write-Host "✅ $($_.Agent) completed" -ForegroundColor Green
    } else {
        Write-Host "❌ $($_.Agent) failed" -ForegroundColor Red
    }
}

$jobs | Remove-Job
```

### Runspace Pool (High Performance)

```powershell
function Invoke-ParallelAgents {
    param(
        [string]$TaskDir = ".orchestrator/agent_tasks",
        [string]$ResultDir = ".orchestrator/results",
        [int]$MaxConcurrency = 4
    )
    
    $pool = [RunspaceFactory]::CreateRunspacePool(1, $MaxConcurrency)
    $pool.Open()
    
    $tasks = Get-ChildItem "$TaskDir/*.md"
    $runspaces = @()
    
    foreach ($task in $tasks) {
        $ps = [PowerShell]::Create()
        $ps.RunspacePool = $pool
        
        [void]$ps.AddScript({
            param($taskPath, $resultPath)
            
            $startTime = Get-Date
            $task = Get-Content $taskPath -Raw
            
            try {
                $result = claude -p $task 2>&1
                $endTime = Get-Date
                
                @"
# Agent Execution Result

## Execution Info
- Status: ✅ Success
- Start: $startTime
- End: $endTime  
- Duration: $(($endTime - $startTime).TotalSeconds)s

## Output
$result
"@ | Out-File $resultPath -Encoding UTF8
                
                return @{ Success = $true; Duration = ($endTime - $startTime).TotalSeconds }
            }
            catch {
                return @{ Success = $false; Error = $_.Exception.Message }
            }
        })
        
        [void]$ps.AddParameter("taskPath", $task.FullName)
        [void]$ps.AddParameter("resultPath", "$ResultDir/$($task.BaseName)-result.md")
        
        $runspaces += [PSCustomObject]@{
            PowerShell = $ps
            Handle = $ps.BeginInvoke()
            Task = $task.BaseName
        }
    }
    
    # Wait and collect
    $results = @()
    foreach ($rs in $runspaces) {
        $result = $rs.PowerShell.EndInvoke($rs.Handle)
        $result | Add-Member -NotePropertyName "Agent" -NotePropertyValue $rs.Task
        $results += $result
        $rs.PowerShell.Dispose()
    }
    
    $pool.Close()
    $pool.Dispose()
    
    return $results
}

# Usage
$results = Invoke-ParallelAgents -MaxConcurrency 6
$results | Format-Table Agent, Success, Duration
```

---

## Advanced Integration Patterns

### 1. Dependency-Aware Scheduling

```powershell
# Define task dependencies
$taskGraph = @{
    "T-01" = @{ Agent = "Agent-01"; Deps = @() }
    "T-02" = @{ Agent = "Agent-02"; Deps = @("T-01") }
    "T-03" = @{ Agent = "Agent-03"; Deps = @("T-01") }
    "T-04" = @{ Agent = "Agent-04"; Deps = @("T-02", "T-03") }
}

$completed = @{}
$taskDir = ".orchestrator/agent_tasks"
$resultDir = ".orchestrator/results"

function Get-ReadyTasks {
    param($graph, $completed)
    
    $ready = @()
    foreach ($taskId in $graph.Keys) {
        if (-not $completed.ContainsKey($taskId)) {
            $deps = $graph[$taskId].Deps
            $allDepsComplete = $true
            foreach ($dep in $deps) {
                if (-not $completed.ContainsKey($dep)) {
                    $allDepsComplete = $false
                    break
                }
            }
            if ($allDepsComplete) {
                $ready += $taskId
            }
        }
    }
    return $ready
}

# Execute with topological ordering
while ($completed.Count -lt $taskGraph.Count) {
    $readyTasks = Get-ReadyTasks -graph $taskGraph -completed $completed
    
    if ($readyTasks.Count -eq 0) {
        Write-Error "Circular dependency detected!"
        break
    }
    
    Write-Host "═══ Batch: $($readyTasks -join ', ') ═══" -ForegroundColor Cyan
    
    $jobs = foreach ($taskId in $readyTasks) {
        $agent = $taskGraph[$taskId].Agent
        Start-Job -Name $taskId -ScriptBlock {
            param($agentFile, $resultFile)
            $task = Get-Content $agentFile -Raw
            claude -p $task | Out-File $resultFile -Encoding UTF8
            return $true
        } -ArgumentList "$taskDir/$agent.md", "$resultDir/$agent-result.md"
    }
    
    $jobs | Wait-Job | Out-Null
    
    foreach ($job in $jobs) {
        $completed[$job.Name] = $true
        Write-Host "  ✅ $($job.Name) completed" -ForegroundColor Green
    }
    
    $jobs | Remove-Job
}

Write-Host "All tasks completed!" -ForegroundColor Green
```

### 2. Timeout and Retry

```powershell
function Invoke-AgentWithRetry {
    param(
        [string]$TaskFile,
        [string]$ResultFile,
        [int]$TimeoutSeconds = 300,
        [int]$MaxRetries = 3
    )
    
    $retryCount = 0
    
    while ($retryCount -lt $MaxRetries) {
        $job = Start-Job -ScriptBlock {
            param($taskPath)
            $task = Get-Content $taskPath -Raw
            claude -p $task
        } -ArgumentList $TaskFile
        
        $completed = Wait-Job $job -Timeout $TimeoutSeconds
        
        if ($completed) {
            $result = Receive-Job $job
            Remove-Job $job
            
            if ($LASTEXITCODE -eq 0) {
                $result | Out-File $ResultFile -Encoding UTF8
                return @{ Success = $true; Retries = $retryCount }
            }
        }
        else {
            Stop-Job $job
            Remove-Job $job
            Write-Warning "Timeout, retry ($($retryCount + 1)/$MaxRetries)"
        }
        
        $retryCount++
        Start-Sleep -Seconds (5 * $retryCount)  # Exponential backoff
    }
    
    return @{ Success = $false; Retries = $retryCount }
}
```

### 3. Streaming Output

```powershell
function Invoke-AgentStreaming {
    param([string]$TaskFile)
    
    $task = Get-Content $TaskFile -Raw
    $process = Start-Process claude -ArgumentList "-p `"$task`"" -NoNewWindow -PassThru -RedirectStandardOutput "temp_output.txt"
    
    $reader = New-Object System.IO.StreamReader("temp_output.txt")
    while (-not $process.HasExited) {
        while (-not $reader.EndOfStream) {
            Write-Host $reader.ReadLine()
        }
        Start-Sleep -Milliseconds 100
    }
    
    while (-not $reader.EndOfStream) {
        Write-Host $reader.ReadLine()
    }
    
    $reader.Close()
    Remove-Item "temp_output.txt"
}
```

---

## Context Passing

### Method 1: Inline Context

```powershell
$context = @"
## Project Background
React project with TypeScript.

## Coding Standards
- ESLint enabled
- Strict mode

## Task
Analyze code quality of src/App.tsx
"@

claude -p $context
```

### Method 2: Reference Files

```powershell
$context = @(
    (Get-Content "project-info.md" -Raw),
    (Get-Content "coding-standards.md" -Raw),
    (Get-Content ".orchestrator/agent_tasks/agent-01.md" -Raw)
) -join "`n`n---`n`n"

claude -p $context
```

### Method 3: Inject Previous Results

```powershell
# Agent-02 depends on Agent-01's result
$agent01Result = Get-Content ".orchestrator/results/agent-01-result.md" -Raw
$agent02Task = Get-Content ".orchestrator/agent_tasks/agent-02.md" -Raw

$fullPrompt = @"
## Previous Result (Agent-01)

$agent01Result

---

## Current Task

$agent02Task
"@

claude -p $fullPrompt | Out-File ".orchestrator/results/agent-02-result.md"
```

---

## Result Aggregation

### Intelligent Merge

```powershell
function Merge-AgentResults {
    param(
        [string]$ResultDir = ".orchestrator/results",
        [string]$OutputFile = ".orchestrator/final_output.md"
    )
    
    $results = Get-ChildItem "$ResultDir/*-result.md" | ForEach-Object {
        @{
            Agent = $_.BaseName -replace '-result$', ''
            Content = Get-Content $_.FullName -Raw
        }
    }
    
    $mergePrompt = @"
You are a result aggregation expert. Integrate the following subtask results into a complete report.

Requirements:
1. Preserve all key information
2. Organize logically
3. Eliminate duplicates
4. Generate executive summary
5. List key findings

---

"@
    
    foreach ($result in $results) {
        $mergePrompt += @"

## $($result.Agent) Result

$($result.Content)

---

"@
    }
    
    $finalReport = claude -p $mergePrompt
    $finalReport | Out-File $OutputFile -Encoding UTF8
    
    Write-Host "✅ Report generated: $OutputFile" -ForegroundColor Green
    return $OutputFile
}
```

---

## Error Handling Best Practices

### 1. Capture and Log Errors

```powershell
function Invoke-AgentSafe {
    param(
        [string]$Agent,
        [string]$TaskFile,
        [string]$ResultFile,
        [string]$ErrorLog = ".orchestrator/error.log"
    )
    
    try {
        $task = Get-Content $TaskFile -Raw
        $result = claude -p $task 2>&1
        
        if ($LASTEXITCODE -ne 0) {
            throw "Claude CLI error code: $LASTEXITCODE"
        }
        
        $result | Out-File $ResultFile -Encoding UTF8
        return @{ Success = $true }
    }
    catch {
        $errorEntry = @"
[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] $Agent failed
Error: $($_.Exception.Message)
Task: $TaskFile

"@
        Add-Content $ErrorLog $errorEntry
        return @{ Success = $false; Error = $_.Exception.Message }
    }
}
```

### 2. Graceful Degradation

```powershell
function Invoke-AgentWithFallback {
    param([string]$TaskFile)
    
    $cliAvailable = Get-Command claude -ErrorAction SilentlyContinue
    
    if ($cliAvailable) {
        $task = Get-Content $TaskFile -Raw
        return claude -p $task
    }
    else {
        Write-Warning "Claude CLI unavailable, using simulation mode"
        return "[Simulated] Task received, CLI unavailable"
    }
}
```

---

## Complete Example: Code Review Workflow

```powershell
# Complete distributed code review

# 1. Initialize
$orchestratorDir = ".orchestrator"
New-Item -ItemType Directory -Path "$orchestratorDir/agent_tasks" -Force | Out-Null
New-Item -ItemType Directory -Path "$orchestratorDir/results" -Force | Out-Null

# 2. Create task files
$tasks = @{
    "agent-01" = "Read all TypeScript files in src/, list filenames and line counts"
    "agent-02" = "Check TypeScript type errors and any type usage"
    "agent-03" = "Scan for security vulnerabilities and sensitive info"
    "agent-04" = "Analyze code complexity and duplication"
}

foreach ($agent in $tasks.Keys) {
    $tasks[$agent] | Out-File "$orchestratorDir/agent_tasks/$agent.md" -Encoding UTF8
}

# 3. Parallel execution
Write-Host "🚀 Starting distributed code review..." -ForegroundColor Cyan

$jobs = foreach ($agent in $tasks.Keys) {
    Start-Job -Name $agent -ScriptBlock {
        param($taskPath, $resultPath)
        $task = Get-Content $taskPath -Raw
        claude -p $task | Out-File $resultPath -Encoding UTF8
    } -ArgumentList "$orchestratorDir/agent_tasks/$agent.md", "$orchestratorDir/results/$agent-result.md"
}

$jobs | Wait-Job | Out-Null
Write-Host "✅ All reviews completed" -ForegroundColor Green

# 4. Aggregate results
Merge-AgentResults

Write-Host "📋 Report: $orchestratorDir/final_output.md" -ForegroundColor Yellow
```
