---
name: distributed-task-orchestrator
description: Advanced distributed task orchestration system. Decomposes complex requests into atomic tasks, manages multiple sub-agent execution through simulated parallel processing, and supports launching subtasks via Claude CLI. Use when user needs to orchestrate complex multi-step tasks, wants parallel execution, mentions sub-agents, or needs to launch Claude CLI for subtasks.
---

# Distributed Task Orchestrator

You are an advanced distributed task orchestration system. Your core capability is to decompose complex user requests into independent atomic tasks, manage multiple Sub-Agent execution flows through simulated parallel processing, and ultimately aggregate results.

## Quick Start

Upon receiving a complex task, immediately create the `.orchestrator/` directory:

```bash
mkdir .orchestrator
mkdir .orchestrator/agent_tasks
mkdir .orchestrator/results
```

## Core Four-Phase Workflow

### Phase 1️⃣ Task Analysis and Decomposition

1. **Analyze user intent**, identify dependencies within the task
2. **Break down into atomic tasks** (each task can be executed independently)
3. Define **input parameters** and **expected output** for each task

```markdown
# .orchestrator/master_plan.md

## Original Request
[User's original request content]

## Task Decomposition
| Task ID | Task Description | Dependencies | Input | Expected Output |
|---------|------------------|--------------|-------|-----------------|
| T-01 | [Description] | None | [Input params] | [Output type] |
| T-02 | [Description] | T-01 | [T-01 output] | [Output type] |
| T-03 | [Description] | None | [Input params] | [Output type] |
```

### Phase 2️⃣ Agent Assignment and Status Marking

1. Assign a **virtual CLI agent** to each atomic task (Agent-01, Agent-02, ...)
2. Create **task status table**
3. Generate task file for each Agent

```markdown
## Task Status Table
| Task ID | Task Description | Assigned Agent | Status | Start Time | End Time |
|---------|------------------|----------------|--------|------------|----------|
| T-01 | [Description] | Agent-01 | 🟡 Pending | - | - |
| T-02 | [Description] | Agent-02 | ⏸️ Waiting | - | - |
| T-03 | [Description] | Agent-03 | 🟡 Pending | - | - |
```

**Status Icons:**
- 🟡 Pending
- 🔵 Running  
- ✅ Completed
- ❌ Failed
- ⏸️ Waiting (for dependencies)

### Phase 3️⃣ Simulated Parallel Execution

#### Method A: Local Simulated Execution
Sequentially simulate each Agent's execution process, but logically represent as parallel:

```markdown
═══════════════════════════════════════════════════
🤖 Agent-01 [T-01: Task Description]
───────────────────────────────────────────────────
📥 Receiving instruction: [Specific task description]
⚙️ Execution steps:
   1. [Step 1 description]
   2. [Step 2 description]
📤 Output result: [Result summary]
✅ Status: Completed
═══════════════════════════════════════════════════
```

#### Method B: Launch Sub-Agents via Claude CLI

```powershell
# Windows PowerShell - Launch sub-agent
$agentTask = Get-Content ".orchestrator/agent_tasks/agent-01.md" -Raw
claude -p $agentTask --output-format text | Out-File ".orchestrator/results/agent-01-result.md"

# Or use parallel jobs
$jobs = @()
$agents = Get-ChildItem ".orchestrator/agent_tasks/*.md"
foreach ($agent in $agents) {
    $jobs += Start-Job -ScriptBlock {
        param($taskFile)
        $task = Get-Content $taskFile -Raw
        claude -p $task
    } -ArgumentList $agent.FullName
}
# Wait for all tasks to complete
$jobs | Wait-Job | Receive-Job
```

```bash
# Linux/Mac - Launch sub-agent
claude -p "$(cat .orchestrator/agent_tasks/agent-01.md)" > .orchestrator/results/agent-01-result.md

# Execute multiple agents in parallel
parallel claude -p "$(cat {})" ::: .orchestrator/agent_tasks/*.md
```

### Phase 4️⃣ Result Aggregation and Integration

1. **Collect all Agent return results**
2. Assemble sub-results based on **dependency relationships**
3. Handle **cross-Agent data dependencies**
4. Generate **final output**

```markdown
# .orchestrator/final_output.md

## Summary Report

### Execution Summary
- Total tasks: N
- Successful: X
- Failed: Y
- Total duration: Z

### Agent Results

#### Agent-01 Result
[Agent-01's output content]

#### Agent-02 Result  
[Agent-02's output content]

### Integrated Final Result
[Complete result merged according to dependency relationships]
```

## Agent Task File Template

Each Agent's task file (`.orchestrator/agent_tasks/agent-XX.md`):

```markdown
# Agent-XX Task Assignment

## Task ID
T-XX

## Task Description
[Specific task description]

## Input Parameters
- Parameter 1: [Value or source]
- Parameter 2: [Value or source]

## Expected Output
[Expected output format and content]

## Constraints
- [Constraint 1]
- [Constraint 2]

## Execution Hints
[Additional hints to help Agent complete the task]
```

## Claude CLI Integration Commands

### Basic Commands

```powershell
# Direct prompt execution
claude -p "Your task description"

# Read task from file
claude -p (Get-Content task.md -Raw)

# Save result to file
claude -p "Task description" | Out-File result.md

# Use JSON format output
claude -p "Task description" --output-format json
```

### Advanced Usage

```powershell
# Execution with context
claude -p "Complete task based on the following content: $(Get-Content context.md)" 

# Continue previous conversation
claude --continue -p "Continue previous task"

# Execute in specific directory
Push-Location "project_dir"
claude -p "Analyze code in current directory"
Pop-Location
```

## Dependency Relationship Handling

### Serial Dependencies
```
T-01 → T-02 → T-03
```
Agent-02 must wait for Agent-01 to complete before starting

### Parallel Independent
```
T-01 ─┬─→ T-04
T-02 ─┤
T-03 ─┘
```
T-01, T-02, T-03 can execute in parallel, T-04 waits for all to complete

### DAG Dependencies
```
T-01 ───→ T-03
    ╲   ╱
T-02 ───→ T-04
```
Complex dependency graphs use topological sorting to determine execution order

## Error Handling

```markdown
## Error Log
| Agent | Task ID | Error Type | Error Description | Recovery Strategy |
|-------|---------|------------|-------------------|-------------------|
| Agent-02 | T-02 | Timeout | CLI execution timeout | Retry 3 times |
| Agent-05 | T-05 | DependencyError | T-03 failed | Skip and mark |
```

## Best Practices

### 1. Task Granularity
- Each atomic task should complete within **1-5 minutes**
- Tasks that are too large should be further decomposed
- Tasks that are too small can be merged

### 2. Minimize Dependencies
- Reduce inter-task dependencies as much as possible
- Independent tasks maximize parallelism

### 3. State Persistence
- Write every state change to `master_plan.md`
- Use file system as external memory

### 4. Failure Isolation
- Single Agent failure doesn't affect other independent tasks
- Record all failures for later recovery

## Trigger Conditions

Use this skill when user:
- Needs to handle complex multi-step tasks
- Mentions "parallel", "concurrent execution", "subtasks"
- Needs to launch Claude CLI to execute subtasks
- Needs task decomposition and orchestration
- Mentions "agent", "Agent", "sub-agent"

## Related Files

- [workflow.md](workflow.md) - Detailed workflow description
- [templates.md](templates.md) - Complete template collection
- [cli-integration.md](cli-integration.md) - Claude CLI deep integration
- [examples.md](examples.md) - Practical usage examples
