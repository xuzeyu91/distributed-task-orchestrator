# Workflow: Detailed Execution Specification

## Execution Flow Overview

```
┌─────────────────────────────────────────────────────────────┐
│                   User Request Received                      │
└──────────────────────────┬──────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Phase 1: Task Decomposition                                  │
│  • Parse intent and identify dependencies                    │
│  • Break into atomic tasks                                   │
│  • Define I/O for each task                                  │
│  → Output: .orchestrator/master_plan.md                      │
└──────────────────────────┬──────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Phase 2: Agent Assignment                                    │
│  • Assign Agent ID per task                                  │
│  • Create status table                                       │
│  • Generate agent task files                                 │
│  → Output: .orchestrator/agent_tasks/agent-XX.md             │
└──────────────────────────┬──────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Phase 3: Parallel Execution                                  │
│  • Group tasks by dependency level                           │
│  • Execute each batch (simulated or CLI)                     │
│  • Record logs and handle errors                             │
│  → Output: .orchestrator/results/agent-XX-result.md          │
└──────────────────────────┬──────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Phase 4: Result Aggregation                                  │
│  • Collect all agent results                                 │
│  • Verify completeness                                       │
│  • Merge by dependency order                                 │
│  → Output: .orchestrator/final_output.md                     │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Task Decomposition

### 1.1 Intent Analysis

Before decomposing, answer these questions:

| Question | Purpose |
|----------|---------|
| What is the primary goal? | Define success criteria |
| What are implicit requirements? | Avoid missing expectations |
| What constraints exist? | Time, resources, scope |
| Can it be parallelized? | Determine if orchestration needed |

### 1.2 Dependency Types

| Type | Description | Example |
|------|-------------|---------|
| Data | B needs A's output | Parse file → Analyze data |
| Sequential | B must follow A | Create dir → Write file |
| Resource | A and B share resource | Write to same file |
| None | Independent | Process different files |

### 1.3 Atomic Task Criteria

A well-defined atomic task must be:

- **Single Responsibility** - Does exactly one thing
- **Independent** - No runtime context dependency
- **Verifiable** - Clear success/failure criteria
- **Retriable** - Can safely retry after failure

### 1.4 Building the Dependency Graph

```
Example: Code Review

          ┌─→ [T-02: Style Check] ─┐
[T-01] ──┤                         ├──→ [T-05: Report]
Read code ├─→ [T-03: Security]  ───┤
          └─→ [T-04: Performance] ─┘
```

---

## Phase 2: Agent Assignment

### 2.1 Naming Convention

```
Agent-{NN}  where NN = 01, 02, 03, ...
```

### 2.2 Priority Levels

| Priority | Meaning | Execute |
|----------|---------|---------|
| P0 | Critical path | First |
| P1 | Has downstream deps | High |
| P2 | Standard | Normal |
| P3 | Optional/Deferrable | Last |

### 2.3 Status Transitions

```
🟡 Pending ──→ 🔵 Running ──→ ✅ Completed
                    │
                    ▼
               ❌ Failed ──→ 🔄 Retrying ──→ (back to Running)

⏸️ Waiting ──→ (deps complete) ──→ 🟡 Pending
```

---

## Phase 3: Execution

### 3.1 Batch Scheduling Algorithm

```python
def schedule(tasks, deps):
    ready = [t for t in tasks if no_deps(t)]
    completed = set()
    
    while ready or running:
        # Launch all ready tasks
        for task in ready:
            start(task)
        ready.clear()
        
        # Wait for any to complete
        done = wait_any(running)
        completed.add(done)
        
        # Find newly ready tasks
        for task in remaining:
            if all_deps_in(task, completed):
                ready.append(task)
```

### 3.2 Simulated Execution Format

```
═══════════════════════════════════════════════════════════
🚀 Batch #1 (No Dependencies)
═══════════════════════════════════════════════════════════

🤖 Agent-01 [T-01: Task Name]
───────────────────────────────────────────────────────────
📥 Input: [description]
⚙️ Executing:
   1. [Step 1]
   2. [Step 2]
📤 Output: [summary]
⏱️ Duration: 1.2s
✅ Completed
```

### 3.3 CLI Execution

For real parallel execution via Claude CLI:

**Windows PowerShell:**
```powershell
$jobs = Get-ChildItem ".orchestrator/agent_tasks/*.md" | ForEach-Object {
    $name = $_.BaseName
    Start-Job -Name $name -ScriptBlock {
        param($path, $out)
        $task = Get-Content $path -Raw
        claude --print $task | Out-File $out -Encoding UTF8
    } -ArgumentList $_.FullName, ".orchestrator/results/$name-result.md"
}

# Monitor progress
while ($running = $jobs | Where-Object State -eq 'Running') {
    Write-Progress -Activity "Executing" -Status "$($jobs.Count - $running.Count)/$($jobs.Count)"
    Start-Sleep -Seconds 1
}

$jobs | Wait-Job | Receive-Job
$jobs | Remove-Job
```

**Bash (with GNU parallel):**
```bash
parallel -j4 'claude --print "$(cat {})" > .orchestrator/results/{/.}-result.md' ::: .orchestrator/agent_tasks/*.md
```

---

## Phase 4: Result Aggregation

### 4.1 Collection Checklist

| Agent | Expected File | Status |
|-------|---------------|--------|
| Agent-01 | agent-01-result.md | ✅/❌ |
| Agent-02 | agent-02-result.md | ✅/❌ |

### 4.2 Merge Strategies

**Simple Concatenation:**
```markdown
# Results
## Agent-01 Output
[content]

## Agent-02 Output
[content]
```

**Structured Merge:**
```markdown
# Analysis Report

## Summary
- Issues found: 15 (from Agent-02)
- Security risks: 3 (from Agent-03)

## Details
[Organized by category, not by agent]
```

**AI-Powered Merge:**
```powershell
$results = Get-Content ".orchestrator/results/*.md" -Raw
$prompt = "Merge these results into a coherent report:`n$results"
claude --print $prompt | Out-File ".orchestrator/final_output.md"
```

---

## State Persistence

Update `master_plan.md` on every state change:

```markdown
## Execution Log

### [2025-01-12 14:30:00] Initialized
- Created 5 tasks
- Assigned 5 agents

### [2025-01-12 14:30:15] Batch #1 Started
- Agent-01 executing T-01

### [2025-01-12 14:30:22] Agent-01 Completed
- Duration: 7s
- Output saved

### [2025-01-12 14:31:00] All Tasks Completed
- Total duration: 45s
- Result: .orchestrator/final_output.md
```

---

## Error Recovery

### Retry Logic

```powershell
function Invoke-WithRetry {
    param($Task, $MaxRetries = 3)
    
    for ($i = 1; $i -le $MaxRetries; $i++) {
        try {
            return & $Task
        } catch {
            if ($i -eq $MaxRetries) { throw }
            Start-Sleep -Seconds (5 * $i)  # Exponential backoff
        }
    }
}
```

### Failure Strategies

| Strategy | Use When |
|----------|----------|
| Retry | Timeout, transient network error |
| Skip | Non-critical task, partial results acceptable |
| Fail-fast | Critical dependency, data integrity required |
| Fallback | Alternative method available |
