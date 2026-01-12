# Notes: Distributed Task Orchestration System Design

## Core Concepts

### 1. Task Decomposition
- Break complex requests into independent atomic tasks
- Identify dependencies between tasks
- Define input/output for each task

### 2. Virtual Agents
- Agent-01, Agent-02, ... Agent-N
- Each agent is responsible for one or more atomic tasks
- Agents can be:
  - Local simulated execution
  - Independent processes launched via Claude CLI

### 3. Task State Management
```
Pending → Running → Completed
              ↓
           Failed
```

### 4. Claude CLI Integration Methods
```bash
# Basic call
claude -p "Task description" --output-format json

# Call with context
claude -p "Task description" --context-file context.md

# Background execution
Start-Process claude -ArgumentList '-p "Task description"' -NoNewWindow
```

## File Structure Design

```
distributed-task-orchestrator/
├── SKILL.md                 # Skill main entry
├── workflow.md              # Detailed workflow description
├── templates.md             # Task plan and status table templates
├── cli-integration.md       # Claude CLI integration guide
└── examples.md              # Usage examples
```

## Runtime Files (Generated in User's Project)

```
[user-project]/
├── .orchestrator/
│   ├── master_plan.md       # Master task plan
│   ├── agent_tasks/
│   │   ├── agent-01.md      # Agent-01's task description
│   │   ├── agent-02.md      # Agent-02's task description
│   │   └── ...
│   ├── results/
│   │   ├── agent-01-result.md
│   │   ├── agent-02-result.md
│   │   └── ...
│   └── final_output.md      # Final aggregated result
```

## Four-Phase Workflow

### Phase 1: Task Analysis and Decomposition
- Parse user intent
- Identify dependencies (DAG graph)
- Break down into atomic tasks
- Define input/output specifications

### Phase 2: Agent Assignment and Status Marking
- Assign Agent IDs
- Create task status table
- Generate task file for each Agent

### Phase 3: Simulated Parallel Execution
- Option: Local simulated execution
- Option: Launch subprocesses via CLI
- Record execution logs

### Phase 4: Result Aggregation and Integration
- Collect all Agent results
- Merge according to dependencies
- Generate final output

## Claude CLI Parameter Reference

CLI parameters to use:
- `-p, --prompt` - Pass prompt directly
- `--context-file` - Provide context file
- `--output-format` - Output format (text/json)
- `--no-interactive` - Non-interactive mode
