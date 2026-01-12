# Templates: Ready-to-Use Templates

## 1. Master Plan Template

**File:** `.orchestrator/master_plan.md`

```markdown
# Task Plan

## Request
> [User's original request]

## Goal
**Objective:** [One sentence describing end result]
**Success Criteria:** [How to verify completion]

---

## Tasks

| ID | Name | Description | Deps | Priority | Status |
|----|------|-------------|------|----------|--------|
| T-01 | [Name] | [Brief desc] | None | P0 | 🟡 |
| T-02 | [Name] | [Brief desc] | T-01 | P1 | ⏸️ |
| T-03 | [Name] | [Brief desc] | T-01 | P1 | ⏸️ |
| T-04 | [Name] | [Brief desc] | T-02,T-03 | P2 | ⏸️ |

### Dependency Graph
```
[T-01] ──┬──→ [T-02] ──┬──→ [T-04]
         └──→ [T-03] ──┘
```

---

## Agents

| Task | Agent | Status | Start | End | Retries |
|------|-------|--------|-------|-----|---------|
| T-01 | Agent-01 | 🟡 Pending | - | - | 0 |
| T-02 | Agent-02 | ⏸️ Waiting | - | - | 0 |
| T-03 | Agent-03 | ⏸️ Waiting | - | - | 0 |
| T-04 | Agent-04 | ⏸️ Waiting | - | - | 0 |

### Status Legend
- 🟡 Pending - Ready to execute
- 🔵 Running - In progress
- ✅ Completed - Success
- ❌ Failed - Error occurred
- ⏸️ Waiting - Dependencies not met
- 🔄 Retrying - Retry in progress

---

## Progress

**Current Batch:** #0
**Completed:** 0/4
**In Progress:** 0
**Failed:** 0

---

## Log

### [YYYY-MM-DD HH:MM:SS] Initialized
- Created task plan with 4 tasks

---

## Errors

| Time | Agent | Error | Action |
|------|-------|-------|--------|
| - | - | - | - |

---

## Output

**Location:** `.orchestrator/final_output.md`
**Status:** Pending
```

---

## 2. Agent Task Template

**File:** `.orchestrator/agent_tasks/agent-XX.md`

```markdown
# Agent-XX: [Task Name]

## Task Info
- **ID:** T-XX
- **Priority:** P1
- **Est. Time:** 2 min

---

## Input

| Parameter | Type | Source | Value |
|-----------|------|--------|-------|
| files | list | User | src/*.ts |
| config | file | T-01 output | .orchestrator/results/agent-01-result.md |

---

## Instructions

[Detailed task description]

### Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]

---

## Expected Output

**Format:** Markdown / JSON / Plain text

**Example:**
```json
{
  "items": [...],
  "summary": "..."
}
```

**Save to:** `.orchestrator/results/agent-XX-result.md`

---

## Constraints
- [Constraint 1]
- [Constraint 2]

---

## Hints
- [Helpful tip for task completion]
```

---

## 3. Agent Result Template

**File:** `.orchestrator/results/agent-XX-result.md`

```markdown
# Agent-XX Result

## Summary
- **Task:** T-XX
- **Status:** ✅ Success / ❌ Failed
- **Duration:** X.Xs
- **Timestamp:** YYYY-MM-DD HH:MM:SS

---

## Process

### Step 1: [Name]
- Action: [What was done]
- Result: [Outcome]

### Step 2: [Name]
- Action: [What was done]
- Result: [Outcome]

---

## Output

[Actual result content]

---

## Stats

| Metric | Value |
|--------|-------|
| Items processed | X |
| Succeeded | X |
| Warnings | X |
| Errors | X |

---

## Issues

### Warnings
- [Warning message]

### Errors
- [Error message and resolution]

---

## Notes

[Additional info useful for downstream tasks]
```

---

## 4. Final Output Template

**File:** `.orchestrator/final_output.md`

```markdown
# Execution Report

## Summary

| Metric | Value |
|--------|-------|
| Total Tasks | N |
| Succeeded | X |
| Failed | Y |
| Duration | Zs |
| Parallel Efficiency | XX% |

---

## Original Request
> [User's request]

---

## Task Results

| ID | Task | Agent | Status | Duration |
|----|------|-------|--------|----------|
| T-01 | [Name] | Agent-01 | ✅ | 1.2s |
| T-02 | [Name] | Agent-02 | ✅ | 2.3s |
| T-03 | [Name] | Agent-03 | ✅ | 1.8s |
| T-04 | [Name] | Agent-04 | ✅ | 0.9s |

---

## Integrated Results

### [Section 1]
[Content from Agent-01]

### [Section 2]
[Merged content from Agent-02 and Agent-03]

### [Section 3]
[Content from Agent-04]

---

## Key Findings

1. [Finding 1]
2. [Finding 2]
3. [Finding 3]

---

## Recommendations

- [Recommendation 1]
- [Recommendation 2]

---

## Timeline

```
T-01: ████████ (1.2s)
T-02:          ████████████ (2.3s)
T-03:          █████████ (1.8s)  
T-04:                         █████ (0.9s)
────────────────────────────────────────→ Time
0s                                     4.2s
```

---

## Appendix

### Agent Outputs
- [Agent-01 Result](./results/agent-01-result.md)
- [Agent-02 Result](./results/agent-02-result.md)
- [Agent-03 Result](./results/agent-03-result.md)
- [Agent-04 Result](./results/agent-04-result.md)

### Errors Encountered
[List if any]
```

---

## 5. Quick Init Script

### Windows PowerShell

**File:** `init-orchestrator.ps1`

```powershell
param([string]$Name = "task")

$base = ".orchestrator"
@("$base", "$base/agent_tasks", "$base/results") | ForEach-Object {
    if (-not (Test-Path $_)) {
        New-Item -ItemType Directory -Path $_ -Force | Out-Null
        Write-Host "Created: $_" -ForegroundColor Green
    }
}

@"
# Task Plan: $Name

## Request
> [Fill in request]

## Tasks
| ID | Name | Deps | Status |
|----|------|------|--------|
| T-01 | | None | 🟡 |

## Agents
| Task | Agent | Status |
|------|-------|--------|
| T-01 | Agent-01 | 🟡 |

## Log
### [$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Initialized
"@ | Out-File "$base/master_plan.md" -Encoding UTF8

Write-Host "Initialized: $base/master_plan.md" -ForegroundColor Cyan
```

### Bash

**File:** `init-orchestrator.sh`

```bash
#!/bin/bash
NAME=${1:-task}
BASE=".orchestrator"

mkdir -p "$BASE/agent_tasks" "$BASE/results"

cat > "$BASE/master_plan.md" << EOF
# Task Plan: $NAME

## Request
> [Fill in request]

## Tasks
| ID | Name | Deps | Status |
|----|------|------|--------|
| T-01 | | None | 🟡 |

## Agents
| Task | Agent | Status |
|------|-------|--------|
| T-01 | Agent-01 | 🟡 |

## Log
### [$(date '+%Y-%m-%d %H:%M:%S')] Initialized
EOF

echo "Initialized: $BASE/master_plan.md"
```

---

## 6. Execution Script

### Windows PowerShell

**File:** `run-agents.ps1`

```powershell
param(
    [switch]$Parallel,
    [int]$MaxJobs = 4,
    [string]$TaskDir = ".orchestrator/agent_tasks",
    [string]$ResultDir = ".orchestrator/results"
)

if (-not (Test-Path $ResultDir)) {
    New-Item -ItemType Directory -Path $ResultDir -Force | Out-Null
}

$tasks = Get-ChildItem "$TaskDir/*.md" | Sort-Object Name
Write-Host "Found $($tasks.Count) tasks (Parallel: $Parallel)" -ForegroundColor Cyan

if ($Parallel) {
    $jobs = foreach ($file in $tasks) {
        $name = $file.BaseName
        Start-Job -Name $name -ScriptBlock {
            param($path, $out)
            claude --print (Get-Content $path -Raw) | Out-File $out -Encoding UTF8
        } -ArgumentList $file.FullName, "$ResultDir/$name-result.md"
    }
    
    $jobs | Wait-Job | Out-Null
    
    foreach ($job in $jobs) {
        $icon = if ($job.State -eq 'Completed') { "✅" } else { "❌" }
        Write-Host "$icon $($job.Name)" -ForegroundColor $(if ($job.State -eq 'Completed') { 'Green' } else { 'Red' })
    }
    
    $jobs | Remove-Job
} else {
    foreach ($file in $tasks) {
        $name = $file.BaseName
        Write-Host "▶ $name" -ForegroundColor Yellow
        claude --print (Get-Content $file.FullName -Raw) | Out-File "$ResultDir/$name-result.md" -Encoding UTF8
        Write-Host "  ✅ Done" -ForegroundColor Green
    }
}

Write-Host "`nResults: $ResultDir" -ForegroundColor Cyan
```

### Bash

**File:** `run-agents.sh`

```bash
#!/bin/bash
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

echo "Found $(ls -1 "$TASK_DIR"/*.md 2>/dev/null | wc -l) tasks (Parallel: $PARALLEL)"

run_task() {
    local file=$1
    local name=$(basename "$file" .md)
    claude --print "$(cat "$file")" > "$RESULT_DIR/${name}-result.md"
    echo "✅ $name"
}

export -f run_task
export RESULT_DIR

if $PARALLEL; then
    ls "$TASK_DIR"/*.md | parallel -j "$MAX_JOBS" run_task {}
else
    for file in "$TASK_DIR"/*.md; do
        run_task "$file"
    done
fi

echo "Results: $RESULT_DIR"
```
