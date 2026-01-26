# Claude Agent Skills Collection

A collection of powerful agent skills for task automation and orchestration. This repository contains skills that extend Claude's capabilities for handling complex workflows.

## Skills Overview

| Skill | Description | Trigger Keywords |
|-------|-------------|------------------|
| [Distributed Task Orchestrator](#distributed-task-orchestrator) | Decompose complex tasks into parallel sub-agents | "parallel", "agents", "orchestrate", "subtasks" |
| [Scheduled Task](#scheduled-task) | Create and manage scheduled tasks with Claude CLI | "定时", "scheduled", "timer", "cron", "每天" |

---

## Distributed Task Orchestrator

A powerful skill for orchestrating complex, multi-step tasks through distributed sub-agent execution.

### Features

- **Task Decomposition**: Automatically breaks down complex requests into manageable atomic tasks
- **Dependency Management**: Handles serial, parallel, and DAG dependencies between tasks
- **Virtual Agent System**: Assigns Agent-01, Agent-02, etc. to execute each task
- **Parallel Execution**: Maximizes efficiency by running independent tasks simultaneously
- **State Persistence**: Uses markdown files to track progress and maintain context
- **Claude CLI Integration**: Optionally launch real sub-agents via Claude CLI

### When to Use

| Trigger | Description | Example |
|---------|-------------|---------|
| Complex multi-step tasks | Tasks requiring 3+ distinct steps | "Build a complete authentication system" |
| Parallel execution needs | Independent tasks that can run simultaneously | "Translate 5 documents to Chinese" |
| Sub-agent orchestration | Need to coordinate multiple specialized agents | "Analyze code for quality, security, and performance" |
| Large-scale analysis | Tasks requiring analysis of multiple files/components | "Review all API endpoints in the project" |

### Quick Start

```bash
# Initialize orchestration directory
mkdir .orchestrator
mkdir .orchestrator/agent_tasks
mkdir .orchestrator/results
```

Create `.orchestrator/master_plan.md`:

```markdown
# Task Plan

## Original Request
> Analyze my TypeScript project for code quality, security, and performance

## Task Decomposition
| Task ID | Description | Dependencies | Agent |
|---------|-------------|--------------|-------|
| T-01 | Scan source files | None | Agent-01 |
| T-02 | Check code quality | T-01 | Agent-02 |
| T-03 | Security scan | T-01 | Agent-03 |
| T-04 | Performance analysis | T-01 | Agent-04 |
| T-05 | Generate report | T-02,T-03,T-04 | Agent-05 |
```

### Workflow

```
[T-01: Code Scan] ──┬──→ [T-02: Quality Analysis]
                    ├──→ [T-03: Security Scan]
                    └──→ [T-04: Performance Analysis]
                                   ↓
                    [T-05: Generate Report] ←─────┘
```

### File Structure

```
distributed-task-orchestrator/
├── SKILL.md              # Main skill entry point
├── workflow.md           # Detailed workflow documentation
├── templates.md          # Task and status templates
├── cli-integration.md    # Claude CLI integration guide
├── examples.md           # Practical examples
└── notes.md              # Design notes
```

### Runtime Files (Generated)

```
[user-project]/
├── .orchestrator/
│   ├── master_plan.md          # Master task plan and status
│   ├── agent_tasks/
│   │   ├── agent-01.md         # Agent task descriptions
│   │   └── ...
│   ├── results/
│   │   ├── agent-01-result.md  # Agent execution results
│   │   └── ...
│   └── final_output.md         # Aggregated final output
```

### Status Icons

- 🟡 Pending - Awaiting execution
- 🔵 Running - Currently executing
- ✅ Completed - Execution successful
- ❌ Failed - Execution failed
- ⏸️ Waiting - Dependencies not satisfied
- 🔄 Retrying - Retry in progress

---

## Scheduled Task

A cross-platform skill for creating and managing scheduled tasks that execute Claude CLI at specified times.

### Features

- **Multiple Schedule Types**: Supports cron expressions, interval-based, and one-time scheduling
- **Cross-Platform**: Pure Python implementation works on Windows, macOS, and Linux
- **Background Daemon**: Scheduler runs in background, checking tasks every minute
- **Desktop Notifications**: Cross-platform notifications when tasks complete
- **Result Persistence**: All execution results saved to files

### When to Use

| Trigger | Description | Example |
|---------|-------------|---------|
| Periodic tasks | Tasks that need to run regularly | "每天早上9点检查代码质量" |
| Timed reminders | One-time scheduled execution | "30分钟后提醒我查看 PR" |
| Interval tasks | Tasks that repeat at fixed intervals | "每隔2小时同步一次数据" |
| Cron jobs | Complex schedule patterns | "工作日早上8点执行任务" |

### Quick Start

```bash
# Install dependencies
pip install -r scheduled-task/scripts/requirements.txt

# Create a scheduled task
python scheduled-task/scripts/create_task.py \
  --name "Daily Code Review" \
  --schedule "cron:0 9 * * *" \
  --prompt "Review code quality in src/ directory"

# Start the scheduler
python scheduled-task/scripts/scheduler.py --daemon

# List all tasks
python scheduled-task/scripts/list_tasks.py
```

### Schedule Types

| Type | Format | Example | Description |
|------|--------|---------|-------------|
| Cron | `cron:expr` | `cron:0 9 * * *` | Daily at 9am |
| Interval | `interval:Xu` | `interval:30m` | Every 30 minutes |
| Once | `once:datetime` | `once:2026-01-27 15:00` | One-time execution |

### Common Patterns

| Pattern | Schedule |
|---------|----------|
| Every day at 9am | `cron:0 9 * * *` |
| Every hour | `interval:1h` |
| Every 30 minutes | `interval:30m` |
| Weekdays at 8am | `cron:0 8 * * 1-5` |
| Tomorrow at 3pm | `once:2026-01-27 15:00` |

### File Structure

```
scheduled-task/
├── SKILL.md                    # Main skill entry point
├── scripts/
│   ├── scheduler.py            # Core scheduler daemon
│   ├── create_task.py          # Create new tasks
│   ├── list_tasks.py           # List all tasks
│   ├── cancel_task.py          # Cancel/delete tasks
│   ├── run_task.py             # Manually run a task
│   ├── notify.py               # Cross-platform notifications
│   └── requirements.txt        # Python dependencies
└── references/
    └── schedule-patterns.md    # Schedule pattern reference
```

### Runtime Files (Generated)

```
[user-project]/
├── .scheduled-tasks/
│   ├── registry.json           # Task registry
│   ├── tasks/
│   │   └── task-001.md         # Task MD files
│   ├── results/
│   │   └── task-001_2026-01-26_09-00.md  # Execution results
│   └── logs/
│       └── scheduler.log       # Scheduler logs
```

### Script Commands

```bash
# Create a task
python create_task.py --name "Task Name" --schedule "cron:0 9 * * *" --prompt "Instructions"

# List tasks
python list_tasks.py [--all] [--json]

# Cancel a task
python cancel_task.py --id task-001 [--delete]

# Run a task manually
python run_task.py --id task-001 [--dry-run]

# Start scheduler
python scheduler.py [--daemon] [--once] [--interval 60]
```

### Cross-Platform Notifications

| Platform | Method |
|----------|--------|
| Windows | win10toast / PowerShell Toast |
| macOS | osascript |
| Linux | notify-send / zenity / kdialog |

---

## Installation

These skills are located at:

```
C:\Users\{User}\.claude\skills\distributed-task-orchestrator\SKILL.md
C:\Users\{User}\.claude\skills\scheduled-task\SKILL.md
```

Or:

```
C:\Users\{User}\.cursor\skills\distributed-task-orchestrator\SKILL.md
C:\Users\{User}\.cursor\skills\scheduled-task\SKILL.md
```

---

## Dependencies

### Distributed Task Orchestrator

- No external dependencies (uses standard library)
- Optional: Claude CLI for real sub-agent execution

### Scheduled Task

```bash
pip install croniter python-dateutil
# Optional for Windows notifications:
pip install win10toast
```

---

## Best Practices

### Task Granularity

- **Ideal**: Each task completes in 1-5 minutes
- **Too large**: Break down further
- **Too small**: Consider merging

### Maximize Parallelism

- Design independent tasks whenever possible
- Use files to pass intermediate results
- Recommended concurrency: 4-8 agents

### Error Handling

- Isolate failures - one agent's failure shouldn't block others
- Implement automatic retry with exponential backoff
- Preserve partial results for recovery

### State Persistence

- Update status files after every state change
- Use file system as external memory
- Log all executions and errors

---

## Related Documentation

### Distributed Task Orchestrator

- [workflow.md](distributed-task-orchestrator/workflow.md) - Detailed workflow documentation
- [templates.md](distributed-task-orchestrator/templates.md) - Complete template collection
- [cli-integration.md](distributed-task-orchestrator/cli-integration.md) - Claude CLI deep integration
- [examples.md](distributed-task-orchestrator/examples.md) - Practical examples

### Scheduled Task

- [schedule-patterns.md](scheduled-task/references/schedule-patterns.md) - Schedule pattern reference

---

## Contributing

To extend or modify these skills:

1. Edit files in the respective skill directory
2. Update `SKILL.md` for core workflow changes
3. Add new templates or examples as needed
4. Test thoroughly before deployment

---

## License

This skill collection is part of a personal knowledge base and skill library.
