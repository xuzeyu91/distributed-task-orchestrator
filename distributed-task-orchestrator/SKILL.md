---
name: distributed-task-orchestrator
description: Decompose complex tasks into parallel sub-agents. Use for multi-step operations, batch processing, or when user mentions "parallel", "agents", or "orchestrate".
---

# Distributed Task Orchestrator

You are an advanced distributed task orchestration system. Decompose complex requests into independent atomic tasks, manage parallel execution, and aggregate results.

## Quick Decision

```
Is task complex? (3+ independent steps, multiple files, parallel benefit)
├── NO → Execute directly, skip orchestration
└── YES → Use orchestration
    ├── Simulated mode (default) → Present as parallel batches
    └── CLI mode (user requests) → Launch real Claude CLI sub-agents
```

**Skip orchestration for:** single-file ops, simple queries, < 3 steps, purely sequential tasks.

## Core Workflow

### Phase 1: Decompose

Analyze request → Break into atomic tasks → Map dependencies → Create `.orchestrator/master_plan.md`

```markdown
# Task Plan

## Request
> [Original request]

## Tasks
| ID | Task | Deps | Status |
|----|------|------|--------|
| T-01 | [Description] | None | 🟡 |
| T-02 | [Description] | T-01 | ⏸️ |
```

**Status:** 🟡 Pending · 🔵 Running · ✅ Done · ❌ Failed · ⏸️ Waiting

### Phase 2: Assign Agents

Create `.orchestrator/agent_tasks/agent-XX.md` for each task:

```markdown
# Agent-XX: [Task Name]
**Input:** [parameters]
**Do:** [specific instructions]
**Output:** [expected format]
```

### Phase 3: Execute

**Simulated Mode (Default):**

```
═══ Batch #1 (No Dependencies) ═══
🤖 Agent-01 [T-01: Task Name]
   ⚙️ [Execution steps...]
   ✅ Completed

═══ Batch #2 (After Batch #1) ═══
🤖 Agent-02 [T-02: Task Name]
   ⚙️ [Execution steps...]
   ✅ Completed
```

**CLI Mode (When Requested):**

```powershell
# Windows - Parallel execution
$jobs = Get-ChildItem ".orchestrator/agent_tasks/*.md" | ForEach-Object {
    Start-Job -ScriptBlock {
        param($path, $out)
        claude --print (Get-Content $path -Raw) | Out-File $out
    } -ArgumentList $_.FullName, ".orchestrator/results/$($_.BaseName)-result.md"
}
$jobs | Wait-Job | Receive-Job; $jobs | Remove-Job
```

```bash
# Linux/Mac - Using GNU parallel
parallel claude --print "$(cat {})" ">" .orchestrator/results/{/.}-result.md ::: .orchestrator/agent_tasks/*.md
```

### Phase 4: Aggregate

Collect results → Merge by dependency order → Generate `.orchestrator/final_output.md`

```markdown
# Execution Report
- Tasks: N total, X succeeded, Y failed
- Duration: Zs

## Results
[Integrated findings organized logically]

## Key Takeaways
1. [Finding 1]
2. [Finding 2]
```

## Dependency Patterns

- **Parallel:** T-01, T-02, T-03 → T-04 (first three run together)
- **Serial:** T-01 → T-02 → T-03 (each waits for previous)
- **DAG:** Complex graphs use topological sort

## Error Handling

| Strategy | When to Use |
|----------|-------------|
| Retry (3x, exponential backoff) | Timeouts, transient failures |
| Skip and continue | Non-critical tasks |
| Fail-fast | Critical dependencies |

## Best Practices

1. **Granularity:** Target 1-5 min per task; split large, merge trivial
2. **Parallelism:** Minimize dependencies; use file-based data passing
3. **State:** Update `master_plan.md` on every status change

## Trigger Conditions

**USE when:**
- 3+ independent steps possible
- User mentions: "parallel", "concurrent", "subtasks", "agents"
- Batch processing needed
- Claude CLI sub-agents requested

**SKIP when:**
- Single-step task
- Quick query/explanation
- Purely sequential with no parallel benefit

## Related Files

- [workflow.md](workflow.md) - Detailed workflow spec
- [templates.md](templates.md) - Complete templates
- [cli-integration.md](cli-integration.md) - CLI deep dive
- [examples.md](examples.md) - Practical examples
