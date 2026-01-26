---
name: scheduled-task
description: Create and manage scheduled tasks that execute Claude CLI at specified times. Use when user mentions "定时", "scheduled", "timer", "cron", "每天", "每小时", "定期", "remind", "提醒", or wants to run automated tasks periodically. Supports cron expressions, interval-based, and one-time scheduling.
license: Apache-2.0
metadata:
  author: ai-agent-toolkit
  version: "1.0.0"
---

# Scheduled Task

Create, manage, and execute scheduled tasks using Claude CLI.

## Quick Start

```
User Request → Parse Schedule → Generate Task MD → Register → Scheduler Executes → Notify
```

## Create a Task

Parse the schedule type and generate task file:

```bash
python scripts/create_task.py \
  --name "Daily Code Review" \
  --schedule "cron:0 9 * * *" \
  --working-dir "/path/to/project" \
  --prompt "Review code quality in src/ directory"
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

## Manage Tasks

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

## Cross-Platform Support

- **Windows**: Native toast notifications via win10toast
- **macOS**: osascript notifications
- **Linux**: notify-send (libnotify)

## Dependencies

```bash
pip install -r scripts/requirements.txt
```

## Error Handling

| Error | Action |
|-------|--------|
| Claude CLI not found | Notify user, log error |
| Task timeout (5min default) | Kill process, mark failed, retry later |
| Invalid cron expression | Reject at creation time |

## Reference Files

- [schedule-patterns.md](references/schedule-patterns.md) - Complete schedule pattern reference
