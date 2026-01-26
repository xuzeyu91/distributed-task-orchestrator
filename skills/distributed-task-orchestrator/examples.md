# Examples: Practical Use Cases

## Example 1: Codebase Analysis

### Request
> "Analyze my TypeScript project for code quality, security, and performance"

### Task Decomposition

```markdown
# .orchestrator/master_plan.md

## Request
> Analyze TypeScript project: quality, security, performance

## Tasks
| ID | Name | Deps | Priority |
|----|------|------|----------|
| T-01 | Scan Files | None | P0 |
| T-02 | Quality Check | T-01 | P1 |
| T-03 | Security Scan | T-01 | P1 |
| T-04 | Performance Analysis | T-01 | P1 |
| T-05 | Generate Report | T-02,T-03,T-04 | P2 |

### Dependency Graph
```
[T-01] ──┬──→ [T-02] ──┐
         ├──→ [T-03] ──┼──→ [T-05]
         └──→ [T-04] ──┘
```
```

### Simulated Execution

```
═══════════════════════════════════════════════════════════
🚀 Batch #1
═══════════════════════════════════════════════════════════

🤖 Agent-01 [T-01: Scan Files]
───────────────────────────────────────────────────────────
📥 Input: src/ directory
⚙️ Executing:
   1. Traverse directory
   2. Identify .ts/.tsx files
   3. Calculate statistics
📤 Output: 15 files, 2,847 lines
✅ Completed (1.8s)

═══════════════════════════════════════════════════════════
🚀 Batch #2 (Parallel)
═══════════════════════════════════════════════════════════

🤖 Agent-02 [T-02: Quality] | Agent-03 [T-03: Security] | Agent-04 [T-04: Performance]
───────────────────────────────────────────────────────────
[Executing in parallel...]

Agent-04 ✅ (2.5s)
Agent-03 ✅ (2.8s)
Agent-02 ✅ (3.2s)

═══════════════════════════════════════════════════════════
🚀 Batch #3
═══════════════════════════════════════════════════════════

🤖 Agent-05 [T-05: Generate Report]
───────────────────────────────────────────────────────────
⚙️ Merging results from T-02, T-03, T-04
📤 Output: final_report.md
✅ Completed (1.5s)
```

### Final Output

```markdown
# Code Analysis Report

## Summary
| Metric | Value |
|--------|-------|
| Files | 15 |
| Lines | 2,847 |
| Issues | 23 |
| Duration | 11.8s |

## Critical Issues

### 🔴 Security: API Key Exposure
- **File:** src/api/config.ts:12
- **Issue:** Hardcoded API key
- **Fix:** Use environment variable

## Warnings

### 🟡 Code Quality
- 8 `any` type usages
- 3 unused variables
- 2 high complexity functions

### 🟡 Performance
- 5 missing `useMemo`
- 3 missing `useCallback`
```

---

## Example 2: Multi-Document Translation

### Request
> "Translate the 5 English docs in docs/ to Chinese"

### Task Decomposition

All translations are independent - maximum parallelism!

```markdown
## Tasks
| ID | File | Agent | Status |
|----|------|-------|--------|
| T-01 | docs/intro.md | Agent-01 | 🟡 |
| T-02 | docs/getting-started.md | Agent-02 | 🟡 |
| T-03 | docs/api-reference.md | Agent-03 | 🟡 |
| T-04 | docs/tutorials.md | Agent-04 | 🟡 |
| T-05 | docs/faq.md | Agent-05 | 🟡 |
```

### Execution (CLI Mode)

```powershell
$docs = Get-ChildItem "docs/*.md"
$jobs = foreach ($doc in $docs) {
    $name = $doc.BaseName
    Start-Job -Name $name -ScriptBlock {
        param($file)
        $content = Get-Content $file -Raw
        claude --print "Translate to Chinese, preserve Markdown formatting: $content"
    } -ArgumentList $doc.FullName
}

$jobs | Wait-Job | Receive-Job
```

### Result

```
═══════════════════════════════════════════════════════════
🚀 5 Translations Running in Parallel
═══════════════════════════════════════════════════════════

Agent-05 [faq.md]           ✅ (15s)
Agent-02 [getting-started]  ✅ (22s)
Agent-01 [intro.md]         ✅ (25s)
Agent-04 [tutorials.md]     ✅ (28s)
Agent-03 [api-reference]    ✅ (35s)

═══════════════════════════════════════════════════════════
✅ All Translations Complete
═══════════════════════════════════════════════════════════
Duration: 35s (Serial estimate: 125s)
Speedup: 3.6x
```

---

## Example 3: API Endpoint Testing

### Request
> "Test all API endpoints for response time and correctness"

### Task Decomposition

```markdown
## Endpoints
| Endpoint | Method | Agent |
|----------|--------|-------|
| /api/users | GET | Agent-01 |
| /api/users/:id | GET | Agent-02 |
| /api/users | POST | Agent-03 |
| /api/products | GET | Agent-04 |
| /api/orders | GET | Agent-05 |
```

### Agent Task Example

```markdown
# Agent-01: Test GET /api/users

## Test Cases
1. Normal request → Expect 200 OK
2. Invalid params → Expect 400
3. Unauthorized → Expect 401

## Validation
- Response time < 500ms
- Returns valid JSON
- Contains pagination info

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

## Summary
| Metric | Value |
|--------|-------|
| Endpoints | 5 |
| Test Cases | 15 |
| Passed | 14 |
| Failed | 1 |
| Avg Response | 156ms |

## Failed Tests

### ❌ POST /api/users - Large Payload
- Expected: < 1000ms
- Actual: 5023ms
- Recommendation: Optimize DB write

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

## Example 4: Full CLI Script

```powershell
# orchestrate.ps1
param([string]$Request = "Analyze code structure")

Write-Host "═══════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "    🤖 Distributed Task Orchestration" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════" -ForegroundColor Cyan

# Phase 1: Decompose
Write-Host "`n📋 Phase 1: Decomposing..." -ForegroundColor Yellow

$prompt = @"
Break this into 3-5 independent tasks. Output JSON:
{"tasks": [{"id": "T-01", "name": "...", "desc": "...", "deps": []}]}

Request: $Request
"@

$json = claude --print $prompt 2>$null
$tasks = $json | ConvertFrom-Json
Write-Host "  ✅ $($tasks.tasks.Count) tasks created" -ForegroundColor Green

# Phase 2: Create files
Write-Host "`n🤖 Phase 2: Assigning agents..." -ForegroundColor Yellow

$dir = ".orchestrator"
New-Item -ItemType Directory -Path "$dir/agent_tasks", "$dir/results" -Force | Out-Null

$i = 1
foreach ($task in $tasks.tasks) {
    $agent = "agent-{0:D2}" -f $i
    "# $agent`: $($task.name)`n`n$($task.desc)" | Out-File "$dir/agent_tasks/$agent.md" -Encoding UTF8
    Write-Host "  📝 $agent → $($task.name)" -ForegroundColor Gray
    $i++
}

# Phase 3: Execute
Write-Host "`n🚀 Phase 3: Executing..." -ForegroundColor Yellow
$start = Get-Date

$jobs = Get-ChildItem "$dir/agent_tasks/*.md" | ForEach-Object {
    $name = $_.BaseName
    Write-Host "  ▶ $name" -ForegroundColor Cyan
    Start-Job -Name $name -ScriptBlock {
        param($path, $out)
        claude --print (Get-Content $path -Raw) | Out-File $out -Encoding UTF8
    } -ArgumentList $_.FullName, "$dir/results/$name-result.md"
}

$jobs | Wait-Job | Out-Null
$duration = ((Get-Date) - $start).TotalSeconds

Write-Host ""
foreach ($job in $jobs) {
    $icon = if ($job.State -eq 'Completed') { "✅" } else { "❌" }
    Write-Host "  $icon $($job.Name)" -ForegroundColor Green
}

$jobs | Remove-Job

# Phase 4: Aggregate
Write-Host "`n📊 Phase 4: Aggregating..." -ForegroundColor Yellow

$results = Get-ChildItem "$dir/results/*.md" | ForEach-Object {
    "## $($_.BaseName)`n$(Get-Content $_ -Raw)"
} | Out-String

$mergePrompt = "Create a summary report from these results:`n$results"
claude --print $mergePrompt | Out-File "$dir/final_output.md" -Encoding UTF8

Write-Host "  ✅ Report complete" -ForegroundColor Green

Write-Host "`n═══════════════════════════════════════════" -ForegroundColor Green
Write-Host "              ✅ Complete" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════" -ForegroundColor Green
Write-Host "📁 Results: $dir" -ForegroundColor Yellow
Write-Host "📄 Report: $dir/final_output.md" -ForegroundColor Yellow
Write-Host "⏱️  Duration: $([math]::Round($duration, 2))s" -ForegroundColor Yellow
```

---

## Example 5: Error Recovery

### Scenario: Agent-03 Timeout

```
═══════════════════════════════════════════════════════════
🚀 Batch #2
═══════════════════════════════════════════════════════════

Agent-01 ✅ (2.1s)
Agent-02 ✅ (1.8s)
Agent-03 ❌ Timeout (60s exceeded)
Agent-04 ✅ (2.3s)

═══════════════════════════════════════════════════════════
🔄 Error Recovery
═══════════════════════════════════════════════════════════

Detected: Agent-03 failed
→ Logging error
→ Retry 1/3...
→ Agent-03 re-executing
→ ✅ Retry successful (3.5s)

═══════════════════════════════════════════════════════════
Continuing...
═══════════════════════════════════════════════════════════
```

### Error Log

```markdown
## Errors
| Time | Agent | Error | Retries | Result |
|------|-------|-------|---------|--------|
| 14:30:22 | Agent-03 | Timeout | 1 | ✅ Success |
```

---

## Best Practices Summary

### ✅ Good Task Design
- "Analyze code quality in src/components" (specific scope)
- "Translate docs/intro.md to Chinese" (clear deliverable)
- "Test GET /api/users endpoint" (atomic operation)

### ❌ Poor Task Design
- "Analyze entire codebase" (too broad)
- "Check one variable" (too small)
- "Make it better" (vague)

### Optimal Settings
- **Concurrency:** 4-8 parallel agents (balance speed vs resources)
- **Task size:** 1-5 minutes per task
- **Dependencies:** Minimize to maximize parallelism

### Error Handling
- Always log failures
- Implement retry with backoff
- Preserve partial results for debugging
