---
name: scheduled-task
description: Create and manage scheduled tasks that execute Claude CLI at specified times. Use when user mentions "定时", "scheduled", "timer", "cron", "每天", "每小时", "定期", "remind", "提醒", or wants to run automated tasks periodically.
---

# Scheduled Task Skill

Create, manage, and execute scheduled tasks using Claude CLI. Supports cron expressions, interval-based, and one-time scheduling.

## Quick Start

```
User Request → Parse Schedule → Generate Task MD → Register → Scheduler Executes → Notify
```

## Core Workflow

### 1. Create a Task

When user requests a scheduled task:

1. Parse the schedule type:
   - **cron**: `0 9 * * *` (daily at 9am)
   - **interval**: `30m`, `2h`, `1d` (every 30min/2hours/1day)
   - **once**: `2026-01-27 15:00` (one-time execution)

2. Generate task file and register:

```bash
python scripts/create_task.py \
  --name "Daily Code Review" \
  --schedule "cron:0 9 * * *" \
  --working-dir "/path/to/project" \
  --prompt "Review code quality in src/ directory"
```

### 2. Manage Tasks

```bash
# List all tasks
python scripts/list_tasks.py

# Cancel a task
python scripts/cancel_task.py --id task-001

# Run a task manually
python scripts/run_task.py --id task-001

# Start the scheduler (background)
python scripts/scheduler.py --daemon
```

### 3. Scheduler Operation

The scheduler runs in background, checking tasks every minute:
- Loads `registry.json` for task definitions
- Executes due tasks via `claude --print`
- Saves results to `.scheduled-tasks/results/`
- Sends cross-platform notifications

## Directory Structure (Runtime)

```
.scheduled-tasks/
├── registry.json          # Task registry
├── tasks/                 # Task MD files
│   └── task-001.md
├── results/               # Execution results
│   └── task-001_2026-01-26_09-00.md
└── logs/
    └── scheduler.log
```

## Task MD Template

```markdown
# Task: [Task Name]

## Context
- **Working Directory:** /path/to/project
- **Focus Files:** src/**/*.ts

## Instructions
[User-defined instructions for Claude to execute]

## Output Requirements
- Format: Markdown report
- Save to: .scheduled-tasks/results/
```

## Script Reference

### create_task.py

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--name` | Yes | Task name |
| `--schedule` | Yes | Schedule spec (cron:expr, interval:30m, once:datetime) |
| `--prompt` | Yes | Task instructions |
| `--working-dir` | No | Working directory (default: current) |
| `--focus-files` | No | File patterns to focus on |

### scheduler.py

| Parameter | Description |
|-----------|-------------|
| `--daemon` | Run as background process |
| `--once` | Check and run due tasks once, then exit |
| `--interval` | Check interval in seconds (default: 60) |

### list_tasks.py

| Parameter | Description |
|-----------|-------------|
| `--all` | Show all tasks including disabled |
| `--json` | Output as JSON |

### cancel_task.py

| Parameter | Description |
|-----------|-------------|
| `--id` | Task ID to cancel |
| `--all` | Cancel all tasks |

### run_task.py

| Parameter | Description |
|-----------|-------------|
| `--id` | Task ID to run |
| `--dry-run` | Show what would be executed |

## Schedule Patterns

See [schedule-patterns.md](references/schedule-patterns.md) for common patterns.

### Quick Reference

| Pattern | Type | Example |
|---------|------|---------|
| Every day at 9am | cron | `cron:0 9 * * *` |
| Every hour | interval | `interval:1h` |
| Every 30 minutes | interval | `interval:30m` |
| Tomorrow at 3pm | once | `once:2026-01-27 15:00` |
| Weekdays at 8am | cron | `cron:0 8 * * 1-5` |

## Cross-Platform Support

- **Windows**: Native toast notifications via win10toast
- **macOS**: osascript notifications
- **Linux**: notify-send (libnotify)

## Dependencies

Install before first use:

```bash
pip install -r scripts/requirements.txt
```

## Error Handling

| Error | Action |
|-------|--------|
| Claude CLI not found | Notify user, log error |
| Task timeout (5min default) | Kill process, mark failed, retry later |
| Invalid cron expression | Reject at creation time |

## Trigger Conditions

**USE when user says:**
- "定时执行...", "每天早上..."
- "Create a scheduled task"
- "Remind me to...", "提醒我..."
- "Run this every hour"
- "Set up a cron job"

**SKIP when:**
- One-time immediate execution
- No time/schedule mentioned
