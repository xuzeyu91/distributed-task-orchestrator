# Examples: Distributed Task Orchestration Practical Examples

## Example 1: Codebase Analysis

### User Request
> "Analyze my TypeScript project for code quality, security vulnerabilities, and performance issues"

---

### Phase 1: Task Decomposition

```markdown
# .orchestrator/master_plan.md

## Original Request
> Analyze TypeScript project for code quality, security, and performance

## Goal Definition
**Primary Goal**: Generate comprehensive code analysis report
**Success Criteria**: Cover quality, security, and performance dimensions

## Task Decomposition

### Dependency Graph
```
[T-01: Code Scan] ──┬──→ [T-02: Quality Analysis]
                    ├──→ [T-03: Security Scan]
                    └──→ [T-04: Performance Analysis]
                               ↓
                    [T-05: Generate Report] ←─────┘
```

### Task List
| Task ID | Task Name | Description | Dependencies | Priority |
|---------|-----------|-------------|--------------|----------|
| T-01 | Code Scan | Read all .ts/.tsx files | None | P0 |
| T-02 | Quality Analysis | Check types, code style | T-01 | P1 |
| T-03 | Security Scan | Find vulnerabilities | T-01 | P1 |
| T-04 | Performance Analysis | Detect perf patterns | T-01 | P1 |
| T-05 | Generate Report | Integrate all results | T-02,T-03,T-04 | P2 |
```

---

### Phase 2: Agent Assignment

```markdown
## Task Status Table
| Task ID | Agent | Status | Start | End |
|---------|-------|--------|-------|-----|
| T-01 | Agent-01 | 🟡 Pending | - | - |
| T-02 | Agent-02 | ⏸️ Waiting | - | - |
| T-03 | Agent-03 | ⏸️ Waiting | - | - |
| T-04 | Agent-04 | ⏸️ Waiting | - | - |
| T-05 | Agent-05 | ⏸️ Waiting | - | - |
```

**Agent-01 Task File** (`.orchestrator/agent_tasks/agent-01.md`):
```markdown
# Agent-01 Task: Code Scan

## Task Description
Scan src/ directory, read all TypeScript files (.ts, .tsx)

## Expected Output
1. File list (path, line count, size)
2. Project stats (total files, total lines)
3. Main entry file identification

## Output Format
```json
{
  "files": [{"path": "...", "lines": 100, "size": 2048}],
  "stats": {"totalFiles": 15, "totalLines": 2847}
}
```
```

---

### Phase 3: Simulated Execution

```
══════════════════════════════════════════════════════════════════
                    🚀 Execution Batch #1
══════════════════════════════════════════════════════════════════

┌──────────────────────────────────────────────────────────────────
│ 🤖 Agent-01 [T-01: Code Scan]
├──────────────────────────────────────────────────────────────────
│ 📥 Instruction: Scan all TypeScript files in src/
│ ⚙️ Execution:
│    → Traverse directory structure
│    → Identify .ts and .tsx files
│    → Read and calculate statistics
│ 📤 Output: 
│    {
│      "files": [
│        {"path": "src/App.tsx", "lines": 45},
│        {"path": "src/components/Button.tsx", "lines": 32},
│        ... (15 files total)
│      ],
│      "stats": {"totalFiles": 15, "totalLines": 2847}
│    }
│ ⏱️ Duration: 1.8s
│ ✅ Completed
└──────────────────────────────────────────────────────────────────

══════════════════════════════════════════════════════════════════
                    🚀 Execution Batch #2 (Parallel)
══════════════════════════════════════════════════════════════════

┌──────────────────────────────────────────────────────────────────
│ 🤖 Agent-02 [T-02: Quality]  |  Agent-03 [T-03: Security]  |  Agent-04 [T-04: Perf]
├──────────────────────────────────────────────────────────────────
│ [Executing in parallel...]
│ 
│ Agent-02: Checking any type usage, unused vars, complexity
│ Agent-03: Scanning for hardcoded keys, injection risks
│ Agent-04: Finding missing useMemo, useCallback, large deps
│ 
│ Agent-04 completed ✅ (2.5s)
│ Agent-03 completed ✅ (2.8s)
│ Agent-02 completed ✅ (3.2s)
└──────────────────────────────────────────────────────────────────

══════════════════════════════════════════════════════════════════
                    🚀 Execution Batch #3
══════════════════════════════════════════════════════════════════

┌──────────────────────────────────────────────────────────────────
│ 🤖 Agent-05 [T-05: Generate Report]
├──────────────────────────────────────────────────────────────────
│ 📥 Instruction: Integrate all analysis results
│ ⚙️ Execution:
│    → Read Agent-02,03,04 results
│    → Sort issues by priority
│    → Generate Markdown report
│ 📤 Output: final_report.md
│ ✅ Completed (1.5s)
└──────────────────────────────────────────────────────────────────
```

---

### Phase 4: Result

```markdown
# .orchestrator/final_output.md

## 📊 Code Analysis Report

### Execution Summary
| Metric | Value |
|--------|-------|
| Files analyzed | 15 |
| Total lines | 2,847 |
| Issues found | 23 |
| Duration | 11.8s |

### 🔴 Critical (Immediate Action)

#### 1. Security Issue
- **API Key Exposure** (src/api/config.ts:12)
  ```typescript
  const API_KEY = "sk-abc123...";  // ❌ Hardcoded
  ```
  **Fix**: Use `process.env.API_KEY`

### 🟡 Warnings

#### 2. Code Quality
- 8 `any` type usages
- 3 unused variables
- 2 high complexity functions (CC > 10)

#### 3. Performance
- 5 missing `useMemo`
- 3 missing `useCallback`
- Suggest code splitting for `HeavyComponent`
```

---

## Example 2: Multi-Document Translation

### User Request
> "Translate the 5 English documents in docs/ to Chinese"

---

### Task Decomposition

```markdown
## Task Decomposition

### Dependencies
None - all translations fully parallelizable

### Task List
| Task ID | File | Agent | Status |
|---------|------|-------|--------|
| T-01 | docs/intro.md | Agent-01 | 🟡 |
| T-02 | docs/getting-started.md | Agent-02 | 🟡 |
| T-03 | docs/api-reference.md | Agent-03 | 🟡 |
| T-04 | docs/tutorials.md | Agent-04 | 🟡 |
| T-05 | docs/faq.md | Agent-05 | 🟡 |
```

### Parallel Execution

```powershell
# All Agents launch simultaneously
$docs = Get-ChildItem "docs/*.md"
$jobs = foreach ($doc in $docs) {
    $index = [array]::IndexOf($docs, $doc) + 1
    Start-Job -Name "Agent-0$index" -ScriptBlock {
        param($file)
        $content = Get-Content $file -Raw
        claude -p "Translate to Chinese, maintain Markdown: $content"
    } -ArgumentList $doc.FullName
}

$jobs | Wait-Job | Receive-Job
```

### Execution Result

```
══════════════════════════════════════════════════════════════════
              🚀 Parallel: 5 translations running
══════════════════════════════════════════════════════════════════

Agent-01 [intro.md]         ████████████████████░░░░ 80%
Agent-02 [getting-started]  ██████████████████████░░ 90%
Agent-03 [api-reference]    ████████████░░░░░░░░░░░░ 50%
Agent-04 [tutorials.md]     ██████████████████░░░░░░ 75%
Agent-05 [faq.md]           ████████████████████████ 100% ✅

Agent-02 completed ✅
Agent-01 completed ✅
Agent-04 completed ✅
Agent-03 completed ✅

══════════════════════════════════════════════════════════════════
                    ✅ All translations complete
══════════════════════════════════════════════════════════════════
Duration: 45s (Serial estimate: 180s)
Speedup: 4x
```

---

## Example 3: API Endpoint Testing

### User Request
> "Test all API endpoints for response time and correctness"

---

### Task Decomposition

```markdown
## Endpoint List
| Endpoint | Method | Agent |
|----------|--------|-------|
| /api/users | GET | Agent-01 |
| /api/users/:id | GET | Agent-02 |
| /api/users | POST | Agent-03 |
| /api/products | GET | Agent-04 |
| /api/orders | GET | Agent-05 |
```

### Agent Task Template

```markdown
# Agent-01 Task: Test GET /api/users

## Test Cases
1. Normal request - Expect 200 OK
2. Invalid params - Expect 400
3. Unauthorized - Expect 401

## Validation
- Response time < 500ms
- Returns JSON
- Contains pagination

## Output Format
```json
{
  "endpoint": "/api/users",
  "tests": [
    {"case": "Normal", "status": "pass", "responseTime": 123}
  ],
  "summary": {"total": 3, "pass": 3, "fail": 0}
}
```
```

### Final Report

```markdown
# API Test Report

## Overview
| Metric | Value |
|--------|-------|
| Endpoints tested | 5 |
| Test cases | 15 |
| Passed | 14 |
| Failed | 1 |
| Avg response | 156ms |

## Failed Cases

### ❌ POST /api/users - Large payload
- Status: Timeout
- Response: 5023ms (Limit: 1000ms)
- Recommendation: Optimize DB writes

## Performance Ranking

| Rank | Endpoint | Avg Time |
|------|----------|----------|
| 1 | GET /api/products | 89ms |
| 2 | GET /api/users | 123ms |
| 3 | GET /api/users/:id | 145ms |
| 4 | GET /api/orders | 198ms |
| 5 | POST /api/users | 856ms |
```

---

## Example 4: Real CLI Execution Script

```powershell
# orchestrate.ps1 - Complete orchestration example

param(
    [string]$Request = "Analyze code structure"
)

Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "       🤖 Distributed Task Orchestration" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Cyan

# Phase 1: Decompose
Write-Host "`n📋 Phase 1: Decomposing..." -ForegroundColor Yellow

$decomposePrompt = @"
Decompose into 3-5 independent atomic tasks.

Request: $Request

Output JSON:
{
  "tasks": [
    {"id": "T-01", "name": "Name", "description": "Desc", "deps": []}
  ]
}
"@

$taskJson = claude -p $decomposePrompt 2>$null
$tasks = $taskJson | ConvertFrom-Json

Write-Host "  ✅ Found $($tasks.tasks.Count) tasks" -ForegroundColor Green

# Phase 2: Create files
Write-Host "`n🤖 Phase 2: Assigning agents..." -ForegroundColor Yellow

$orchestratorDir = ".orchestrator"
New-Item -ItemType Directory -Path "$orchestratorDir/agent_tasks" -Force | Out-Null
New-Item -ItemType Directory -Path "$orchestratorDir/results" -Force | Out-Null

$agentIndex = 1
foreach ($task in $tasks.tasks) {
    $agentId = "agent-{0:D2}" -f $agentIndex
    
    $taskContent = @"
# $agentId Task

## Task ID: $($task.id)
## Name: $($task.name)

$($task.description)

Complete and output result.
"@
    
    $taskContent | Out-File "$orchestratorDir/agent_tasks/$agentId.md" -Encoding UTF8
    Write-Host "  📝 $agentId -> $($task.name)" -ForegroundColor Gray
    $agentIndex++
}

# Phase 3: Execute
Write-Host "`n🚀 Phase 3: Executing..." -ForegroundColor Yellow

$taskFiles = Get-ChildItem "$orchestratorDir/agent_tasks/*.md"
$startTime = Get-Date

$jobs = foreach ($file in $taskFiles) {
    $agentId = $file.BaseName
    Write-Host "  ▶ Launching $agentId" -ForegroundColor Cyan
    
    Start-Job -Name $agentId -ScriptBlock {
        param($taskPath, $resultPath)
        $task = Get-Content $taskPath -Raw
        claude -p $task 2>&1 | Out-File $resultPath -Encoding UTF8
    } -ArgumentList $file.FullName, "$orchestratorDir/results/$agentId-result.md"
}

$jobs | Wait-Job | Out-Null
$endTime = Get-Date
$duration = ($endTime - $startTime).TotalSeconds

Write-Host ""
foreach ($job in $jobs) {
    $status = if ($job.State -eq 'Completed') { "✅" } else { "❌" }
    Write-Host "  $status $($job.Name)" -ForegroundColor Green
}

# Phase 4: Aggregate
Write-Host "`n📊 Phase 4: Aggregating..." -ForegroundColor Yellow

$allResults = Get-ChildItem "$orchestratorDir/results/*.md" | ForEach-Object {
    "## $($_.BaseName)`n`n$(Get-Content $_ -Raw)"
} | Out-String

$mergePrompt = @"
Integrate subtask results into concise report:

$allResults

Generate executive summary and key findings.
"@

claude -p $mergePrompt 2>$null | Out-File "$orchestratorDir/final_output.md" -Encoding UTF8

Write-Host "  ✅ Report complete" -ForegroundColor Green

$jobs | Remove-Job

Write-Host "`n═══════════════════════════════════════════════════" -ForegroundColor Green
Write-Host "                  ✅ Complete" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Green
Write-Host "`n📁 Results: $orchestratorDir" -ForegroundColor Yellow
Write-Host "📄 Report: $orchestratorDir/final_output.md" -ForegroundColor Yellow
Write-Host "⏱️ Duration: $([math]::Round($duration, 2))s" -ForegroundColor Yellow
```

---

## Example 5: Error Recovery

### Scenario: Agent-03 Failed

```
══════════════════════════════════════════════════════════════════
                    🚀 Execution Batch #2
══════════════════════════════════════════════════════════════════

Agent-01 ✅ Completed (2.1s)
Agent-02 ✅ Completed (1.8s)
Agent-03 ❌ Failed - Timeout
Agent-04 ✅ Completed (2.3s)

══════════════════════════════════════════════════════════════════
                    🔄 Error Recovery
══════════════════════════════════════════════════════════════════

Agent-03 failure detected
→ Update error log
→ Retry #1/3...
→ Agent-03 re-executing
→ ✅ Retry successful (3.5s)

══════════════════════════════════════════════════════════════════
                    Continuing Execution
══════════════════════════════════════════════════════════════════
```

### Error Log

```markdown
## ⚠️ Error Log

| Time | Agent | Error | Retries | Result |
|------|-------|-------|---------|--------|
| 14:30:22 | Agent-03 | Timeout (>60s) | 1 | ✅ Success |
```

---

## Tips Summary

### 1. Task Granularity
- ✅ Good: "Analyze code quality in src/components"
- ❌ Bad: "Analyze entire codebase" (too large)
- ❌ Bad: "Check one variable" (too small)

### 2. Minimize Dependencies
- Design independent tasks when possible
- Use files for intermediate results
- Avoid circular dependencies

### 3. Parallel Efficiency
- More independent tasks = greater speedup
- Control concurrency (4-8 recommended)
- Monitor resource usage

### 4. Error Handling
- Log all failures
- Implement auto-retry
- Preserve partial results
