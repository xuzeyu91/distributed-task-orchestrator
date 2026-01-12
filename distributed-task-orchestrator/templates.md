# Templates: Distributed Task Orchestration Template Collection

## 1. Master Plan Template (master_plan.md)

```markdown
# 🎯 Distributed Task Plan

## Original Request
> [User's original request content]

## Goal Definition
**Primary Goal**: [One sentence describing the final result]
**Success Criteria**: [How to determine task completion]

---

## 📋 Task Decomposition

### Dependency Graph
```
[ASCII diagram showing task dependencies]
```

### Task List

| Task ID | Task Name | Description | Dependencies | Priority | Est. Time |
|---------|-----------|-------------|--------------|----------|-----------|
| T-01 | [Name] | [Brief description] | None | P0 | 1min |
| T-02 | [Name] | [Brief description] | T-01 | P1 | 2min |
| T-03 | [Name] | [Brief description] | T-01 | P1 | 3min |
| T-04 | [Name] | [Brief description] | T-02,T-03 | P2 | 2min |

---

## 🤖 Agent Assignment

| Task ID | Agent | Status | Start Time | End Time | Retries |
|---------|-------|--------|------------|----------|---------|
| T-01 | Agent-01 | 🟡 Pending | - | - | 0 |
| T-02 | Agent-02 | 🟡 Pending | - | - | 0 |
| T-03 | Agent-03 | 🟡 Pending | - | - | 0 |
| T-04 | Agent-04 | ⏸️ Waiting | - | - | 0 |

### Status Legend
- 🟡 Pending - Awaiting execution
- 🔵 Running - Currently executing
- ✅ Completed - Execution successful
- ❌ Failed - Execution failed
- ⏸️ Waiting - Dependencies not satisfied
- 🔄 Retrying - Retrying after failure

---

## 📊 Execution Progress

### Current Batch: #0
**Status**: Initializing

### Completion Statistics
- Total tasks: 4
- Completed: 0
- In progress: 0
- Waiting: 4
- Failed: 0

---

## 📝 Execution Log

### [YYYY-MM-DD HH:MM:SS] Initialization
- Task plan created
- Assigned N Agents

---

## ⚠️ Error Log

| Time | Agent | Task ID | Error Type | Description | Resolution |
|------|-------|---------|------------|-------------|------------|
| - | - | - | - | - | - |

---

## 📦 Final Output

**Output Location**: `.orchestrator/final_output.md`
**Status**: Pending generation
```

---

## 2. Agent Task Template (agent-XX.md)

```markdown
# 🤖 Agent-XX Task Assignment

## Task Information
- **Task ID**: T-XX
- **Task Name**: [Task name]
- **Priority**: P1
- **Estimated Time**: 3 minutes

---

## 📥 Input

### Parameter List
| Parameter | Type | Source | Value/Description |
|-----------|------|--------|-------------------|
| param1 | string | User input | [Value] |
| param2 | file | T-01 output | .orchestrator/results/agent-01-result.md |

### Context Information
[Background information helpful for task completion]

---

## 🎯 Task Description

[Detailed description of task to complete]

### Specific Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]

---

## 📤 Expected Output

### Output Format
[Describe expected format: text/JSON/Markdown etc.]

### Output Example
```
[Example of output format]
```

### Output Location
`.orchestrator/results/agent-XX-result.md`

---

## ⚠️ Constraints

- [Constraint 1: e.g., cannot modify original files]
- [Constraint 2: e.g., must use specific format]
- [Constraint 3: e.g., time limit]

---

## 💡 Execution Hints

[Hints or suggestions to help Agent complete the task]
```

---

## 3. Agent Result Template (agent-XX-result.md)

```markdown
# 📤 Agent-XX Execution Result

## Execution Summary
- **Task ID**: T-XX
- **Status**: ✅ Success / ❌ Failed
- **Start Time**: YYYY-MM-DD HH:MM:SS
- **End Time**: YYYY-MM-DD HH:MM:SS
- **Duration**: X.Xs

---

## 📋 Execution Process

### Step 1: [Step name]
- Action: [Action performed]
- Result: [Action result]

### Step 2: [Step name]
- Action: [Action performed]
- Result: [Action result]

---

## 📦 Output Result

[Actual output content]

---

## 📊 Statistics

| Metric | Value |
|--------|-------|
| Items processed | X |
| Successful | X |
| Warnings | X |
| Errors | X |

---

## ⚠️ Warnings and Errors

### Warnings
- [Warning information]

### Errors
- [Error information and handling]

---

## 📎 Additional Information

[Extra information useful for subsequent tasks]
```

---

## 4. Final Output Template (final_output.md)

```markdown
# 📊 Distributed Task Execution Report

## Execution Summary

| Metric | Value |
|--------|-------|
| Total tasks | N |
| Successful tasks | X |
| Failed tasks | Y |
| Total duration | Zs |
| Parallel efficiency | XX% |

---

## 🎯 Original Goal

> [User's original request]

---

## ✅ Completion Status

### Task Completion Details

| Task ID | Task Name | Agent | Status | Duration |
|---------|-----------|-------|--------|----------|
| T-01 | [Name] | Agent-01 | ✅ | 1.2s |
| T-02 | [Name] | Agent-02 | ✅ | 2.3s |
| T-03 | [Name] | Agent-03 | ✅ | 1.8s |
| T-04 | [Name] | Agent-04 | ✅ | 0.9s |

---

## 📦 Integrated Results

[Final result logically integrated from each Agent's output]

### Part One: [Title]
[Processing result from Agent-01]

### Part Two: [Title]
[Merged results from Agent-02 and Agent-03]

### Part Three: [Title]
[Processing result from Agent-04]

---

## 📈 Key Findings/Recommendations

1. [Finding/Recommendation 1]
2. [Finding/Recommendation 2]
3. [Finding/Recommendation 3]

---

## ⚠️ Notes

- [Items requiring user attention]
- [Suggested follow-up actions]

---

## 📝 Execution Timeline

```
T-01: ████████ (1.2s)
T-02:          ████████████ (2.3s)
T-03:          █████████ (1.8s)  
T-04:                         █████ (0.9s)
─────────────────────────────────────────→ Time
0s                                      4.2s
```

---

## 📎 Appendix

### A. Detailed Agent Outputs
- [Agent-01 Result](./results/agent-01-result.md)
- [Agent-02 Result](./results/agent-02-result.md)
- [Agent-03 Result](./results/agent-03-result.md)
- [Agent-04 Result](./results/agent-04-result.md)

### B. Error Log
[List any errors here]
```

---

## 5. CLI Launch Scripts

### Windows PowerShell (run-agents.ps1)

```powershell
# Distributed Task Orchestration - Agent Launch Script
# Usage: .\run-agents.ps1 [-Parallel] [-MaxJobs 5]

param(
    [switch]$Parallel = $false,
    [int]$MaxJobs = 4,
    [string]$TaskDir = ".orchestrator/agent_tasks",
    [string]$ResultDir = ".orchestrator/results"
)

# Ensure result directory exists
if (-not (Test-Path $ResultDir)) {
    New-Item -ItemType Directory -Path $ResultDir -Force | Out-Null
}

# Get all task files
$taskFiles = Get-ChildItem "$TaskDir/*.md" | Sort-Object Name

Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  🚀 Distributed Task Orchestration - Agent Executor" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "Found $($taskFiles.Count) tasks" -ForegroundColor Yellow
Write-Host "Parallel mode: $Parallel (Max: $MaxJobs)" -ForegroundColor Yellow
Write-Host ""

if ($Parallel) {
    $jobs = foreach ($file in $taskFiles) {
        $agentId = $file.BaseName
        Start-Job -Name $agentId -ScriptBlock {
            param($taskPath, $resultPath, $agentName)
            $task = Get-Content $taskPath -Raw
            $startTime = Get-Date
            
            try {
                $result = claude -p $task 2>&1
                $endTime = Get-Date
                $duration = ($endTime - $startTime).TotalSeconds
                
                @"
# Agent Execution Result

## Execution Info
- Agent: $agentName
- Status: ✅ Success
- Start: $startTime
- End: $endTime
- Duration: $duration seconds

## Output

$result
"@ | Out-File $resultPath -Encoding UTF8
                
                return @{ Agent = $agentName; Status = "Success"; Duration = $duration }
            }
            catch {
                $endTime = Get-Date
                @"
# Agent Execution Result

## Execution Info
- Agent: $agentName
- Status: ❌ Failed
- Start: $startTime
- End: $endTime
- Error: $($_.Exception.Message)
"@ | Out-File $resultPath -Encoding UTF8
                
                return @{ Agent = $agentName; Status = "Failed"; Error = $_.Exception.Message }
            }
        } -ArgumentList $file.FullName, "$ResultDir/$agentId-result.md", $agentId
    }
    
    Write-Host "Waiting for tasks..." -ForegroundColor Yellow
    $jobs | Wait-Job | Out-Null
    
    Write-Host ""
    Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Green
    Write-Host "                  Execution Complete" -ForegroundColor Green
    Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Green
    
    foreach ($job in $jobs) {
        $result = Receive-Job $job
        if ($result.Status -eq "Success") {
            Write-Host "✅ $($result.Agent): Success ($([math]::Round($result.Duration, 2))s)" -ForegroundColor Green
        } else {
            Write-Host "❌ $($result.Agent): Failed - $($result.Error)" -ForegroundColor Red
        }
    }
    
    $jobs | Remove-Job
}
else {
    foreach ($file in $taskFiles) {
        $agentId = $file.BaseName
        Write-Host "▶ Executing $agentId..." -ForegroundColor Cyan
        
        $task = Get-Content $file.FullName -Raw
        $startTime = Get-Date
        
        try {
            $result = claude -p $task 2>&1
            $endTime = Get-Date
            $duration = ($endTime - $startTime).TotalSeconds
            
            $result | Out-File "$ResultDir/$agentId-result.md" -Encoding UTF8
            Write-Host "  ✅ Completed ($([math]::Round($duration, 2))s)" -ForegroundColor Green
        }
        catch {
            Write-Host "  ❌ Failed: $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}

Write-Host ""
Write-Host "Results saved to: $ResultDir" -ForegroundColor Yellow
```

### Bash Script (run-agents.sh)

```bash
#!/bin/bash

# Distributed Task Orchestration - Agent Launch Script
# Usage: ./run-agents.sh [-p] [-j 4]

PARALLEL=false
MAX_JOBS=4
TASK_DIR=".orchestrator/agent_tasks"
RESULT_DIR=".orchestrator/results"

while getopts "pj:" opt; do
    case $opt in
        p) PARALLEL=true ;;
        j) MAX_JOBS=$OPTARG ;;
    esac
done

mkdir -p "$RESULT_DIR"

echo "═══════════════════════════════════════════════════"
echo "  🚀 Distributed Task Orchestration - Agent Executor"
echo "═══════════════════════════════════════════════════"
echo ""

task_count=$(ls -1 "$TASK_DIR"/*.md 2>/dev/null | wc -l)
echo "Found $task_count tasks"
echo "Parallel mode: $PARALLEL (Max: $MAX_JOBS)"
echo ""

run_agent() {
    local task_file=$1
    local agent_id=$(basename "$task_file" .md)
    local result_file="$RESULT_DIR/${agent_id}-result.md"
    
    local start_time=$(date +%s)
    
    if claude -p "$(cat "$task_file")" > "$result_file" 2>&1; then
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))
        echo "✅ $agent_id: Success (${duration}s)"
    else
        echo "❌ $agent_id: Failed"
    fi
}

export -f run_agent
export RESULT_DIR

if $PARALLEL; then
    ls -1 "$TASK_DIR"/*.md | parallel -j "$MAX_JOBS" run_agent {}
else
    for task_file in "$TASK_DIR"/*.md; do
        run_agent "$task_file"
    done
fi

echo ""
echo "Results saved to: $RESULT_DIR"
```

---

## 6. Quick Initialization Script

### init-orchestrator.ps1

```powershell
# Initialize distributed task orchestration directory structure
param(
    [string]$ProjectName = "task"
)

$baseDir = ".orchestrator"

# Create directories
$dirs = @(
    $baseDir,
    "$baseDir/agent_tasks",
    "$baseDir/results"
)

foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "✅ Created: $dir" -ForegroundColor Green
    }
}

# Create master plan
$masterPlan = @"
# 🎯 Distributed Task Plan: $ProjectName

## Original Request
> [Fill in user request here]

## Goal Definition
**Primary Goal**: [Goal description]
**Success Criteria**: [Success criteria]

---

## 📋 Task Decomposition

| Task ID | Task Name | Description | Dependencies | Priority |
|---------|-----------|-------------|--------------|----------|
| T-01 | | | None | P0 |

---

## 🤖 Agent Assignment

| Task ID | Agent | Status | Start Time | End Time |
|---------|-------|--------|------------|----------|
| T-01 | Agent-01 | 🟡 Pending | - | - |

---

## 📝 Execution Log

### [$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Initialization
- Task plan created
"@

$masterPlan | Out-File "$baseDir/master_plan.md" -Encoding UTF8
Write-Host "✅ Created: $baseDir/master_plan.md" -ForegroundColor Green

Write-Host ""
Write-Host "🎉 Initialization complete!" -ForegroundColor Cyan
Write-Host "Next: Edit $baseDir/master_plan.md to define tasks" -ForegroundColor Yellow
```
