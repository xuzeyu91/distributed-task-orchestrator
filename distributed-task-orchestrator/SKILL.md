---
name: distributed-task-orchestrator
description: Advanced distributed task orchestration system. Decomposes complex requests into atomic tasks, manages parallel sub-agent execution, supports Claude CLI integration. Use when handling complex multi-step tasks requiring parallel execution, task decomposition, or sub-agent orchestration.
---

# Distributed Task Orchestrator

You are an advanced distributed task orchestration system. Your core capability is decomposing complex user requests into independent atomic tasks, managing parallel Sub-Agent execution, and aggregating results.

## Decision Flow

Before starting orchestration, evaluate:

```
Is the task complex? (3+ independent steps, multiple files, parallel opportunities)
├── NO → Execute directly without orchestration
└── YES → Does user want real CLI execution?
    ├── NO → Use simulated parallel execution (Method A)
    └── YES → Use Claude CLI sub-agents (Method B)
```

**Skip orchestration for:**
- Single-file operations
- Simple queries or explanations
- Tasks completable in < 3 steps
- Sequential operations with no parallelism benefit

## Quick Start

For complex tasks requiring orchestration:

```bash
mkdir -p .orchestrator/agent_tasks .orchestrator/results
```

## Core Four-Phase Workflow

### Phase 1: Task Analysis and Decomposition

1. **Analyze user intent** - identify dependencies
2. **Decompose into atomic tasks** - each independently executable
3. **Define I/O** - input parameters and expected output per task

Create `.orchestrator/master_plan.md`:

```markdown
# Distributed Task Plan

## Original Request
> [User's request]

## Task Decomposition
| Task ID | Description | Dependencies | Input | Expected Output |
|---------|-------------|--------------|-------|-----------------|
| T-01 | [Desc] | None | [Input] | [Output type] |
| T-02 | [Desc] | T-01 | [T-01 output] | [Output type] |
| T-03 | [Desc] | None | [Input] | [Output type] |
```

### Phase 2: Agent Assignment

1. Assign **virtual agent** per atomic task (Agent-01, Agent-02, ...)
2. Create **status table**
3. Generate **task files** for each Agent

```markdown
## Status Table
| Task ID | Agent | Status | Start | End |
|---------|-------|--------|-------|-----|
| T-01 | Agent-01 | 🟡 Pending | - | - |
| T-02 | Agent-02 | ⏸️ Waiting | - | - |
| T-03 | Agent-03 | 🟡 Pending | - | - |
```

**Status Icons:**
- 🟡 Pending - ready to execute
- 🔵 Running - currently executing
- ✅ Completed - finished successfully
- ❌ Failed - execution failed
- ⏸️ Waiting - blocked by dependencies

### Phase 3: Execution

#### Method A: Simulated Parallel Execution (Default)

Execute sequentially but present as parallel batches:

```
═══════════════════════════════════════════════════
🚀 Batch #1 (No Dependencies)
═══════════════════════════════════════════════════

🤖 Agent-01 [T-01: Task Name]
───────────────────────────────────────────────────
📥 Input: [description]
⚙️ Executing:
   1. [Step 1]
   2. [Step 2]
📤 Output: [result summary]
✅ Completed

🤖 Agent-03 [T-03: Task Name]
───────────────────────────────────────────────────
📥 Input: [description]
⚙️ Executing:
   1. [Step 1]
📤 Output: [result summary]
✅ Completed

═══════════════════════════════════════════════════
🚀 Batch #2 (After Batch #1)
═══════════════════════════════════════════════════

🤖 Agent-02 [T-02: Task Name]
───────────────────────────────────────────────────
...
```

#### Method B: Claude CLI Sub-Agents (Real Parallel)

Use when user explicitly requests CLI execution:

**Windows PowerShell:**
```powershell
# Single agent
$task = Get-Content ".orchestrator/agent_tasks/agent-01.md" -Raw
claude -p $task | Out-File ".orchestrator/results/agent-01-result.md"

# Parallel agents
$jobs = Get-ChildItem ".orchestrator/agent_tasks/*.md" | ForEach-Object {
    Start-Job -ScriptBlock {
        param($path, $out)
        claude -p (Get-Content $path -Raw) | Out-File $out
    } -ArgumentList $_.FullName, ".orchestrator/results/$($_.BaseName)-result.md"
}
$jobs | Wait-Job | Receive-Job
$jobs | Remove-Job
```

**Linux/Mac:**
```bash
# Single agent
claude -p "$(cat .orchestrator/agent_tasks/agent-01.md)" > .orchestrator/results/agent-01-result.md

# Parallel agents (requires GNU parallel)
parallel claude -p "$(cat {})" ">" .orchestrator/results/{/.}-result.md ::: .orchestrator/agent_tasks/*.md
```

### Phase 4: Result Aggregation

1. Collect all Agent results
2. Assemble based on dependency order
3. Handle cross-Agent data dependencies
4. Generate final output

```markdown
# .orchestrator/final_output.md

## Execution Summary
- Total tasks: N
- Successful: X
- Failed: Y
- Duration: Z

## Integrated Results
[Merged output organized logically]

## Key Findings
1. [Finding 1]
2. [Finding 2]
```

## Agent Task File Template

`.orchestrator/agent_tasks/agent-XX.md`:

```markdown
# Agent-XX Task

## Task ID
T-XX

## Description
[Specific task description]

## Input
- [Parameter 1]: [Value/Source]
- [Parameter 2]: [Value/Source]

## Expected Output
[Format and content expectations]

## Constraints
- [Constraint 1]
- [Constraint 2]
```

## Dependency Patterns

**Serial:** T-01 → T-02 → T-03 (each waits for previous)

**Parallel:** T-01, T-02, T-03 → T-04 (first three parallel, T-04 waits for all)

**DAG:** Complex graphs use topological sort for execution order

## Error Handling

```markdown
## Error Log
| Agent | Task | Error | Strategy |
|-------|------|-------|----------|
| Agent-02 | T-02 | Timeout | Retry 3x |
| Agent-05 | T-05 | Dep failed | Skip |
```

**Recovery strategies:**
- Retry with exponential backoff (default: 3 attempts)
- Skip and mark (for non-critical tasks)
- Fail-fast (for critical dependencies)

## Best Practices

### Task Granularity
- Target 1-5 minute completion per task
- Split large tasks, merge trivial ones
- Each task should have clear success criteria

### Maximize Parallelism
- Minimize inter-task dependencies
- Use file-based data passing
- Batch independent operations

### State Management
- Update `master_plan.md` on state changes
- Use filesystem as persistent memory
- Log all executions for debugging

## Trigger Conditions

**Use this skill when:**
- Complex multi-step tasks (3+ independent steps)
- User mentions: "parallel", "concurrent", "subtasks", "agents"
- Multiple independent operations possible
- Need Claude CLI for real sub-agent execution
- Large-scale batch processing

**Do NOT use when:**
- Simple single-step tasks
- Purely sequential operations
- Quick queries or explanations

## Related Documentation

- [workflow.md](workflow.md) - Detailed workflow specification
- [templates.md](templates.md) - Complete template collection
- [cli-integration.md](cli-integration.md) - Claude CLI deep integration
- [examples.md](examples.md) - Practical usage examples
