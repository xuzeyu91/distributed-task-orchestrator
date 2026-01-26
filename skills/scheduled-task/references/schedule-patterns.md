# Schedule Patterns Reference

Common scheduling patterns for the scheduled-task skill.

## Cron Expression Format

```
┌───────────── minute (0-59)
│ ┌─────────── hour (0-23)
│ │ ┌───────── day of month (1-31)
│ │ │ ┌─────── month (1-12)
│ │ │ │ ┌───── day of week (0-6, 0=Sunday)
│ │ │ │ │
* * * * *
```

### Special Characters

| Char | Description | Example |
|------|-------------|---------|
| `*` | Any value | `* * * * *` = every minute |
| `,` | List | `0,30 * * * *` = at 0 and 30 minutes |
| `-` | Range | `0-5 * * * *` = minutes 0 through 5 |
| `/` | Step | `*/15 * * * *` = every 15 minutes |

## Common Cron Patterns

### Daily Schedules

| Description | Cron | Command |
|-------------|------|---------|
| Every day at midnight | `0 0 * * *` | `cron:0 0 * * *` |
| Every day at 9am | `0 9 * * *` | `cron:0 9 * * *` |
| Every day at 6pm | `0 18 * * *` | `cron:0 18 * * *` |
| Twice daily (9am, 6pm) | `0 9,18 * * *` | `cron:0 9,18 * * *` |

### Hourly Schedules

| Description | Cron | Command |
|-------------|------|---------|
| Every hour | `0 * * * *` | `cron:0 * * * *` |
| Every 2 hours | `0 */2 * * *` | `cron:0 */2 * * *` |
| Every 6 hours | `0 */6 * * *` | `cron:0 */6 * * *` |
| At :30 every hour | `30 * * * *` | `cron:30 * * * *` |

### Minute Schedules

| Description | Cron | Command |
|-------------|------|---------|
| Every minute | `* * * * *` | `cron:* * * * *` |
| Every 5 minutes | `*/5 * * * *` | `cron:*/5 * * * *` |
| Every 15 minutes | `*/15 * * * *` | `cron:*/15 * * * *` |
| Every 30 minutes | `*/30 * * * *` | `cron:*/30 * * * *` |

### Weekly Schedules

| Description | Cron | Command |
|-------------|------|---------|
| Every Monday at 9am | `0 9 * * 1` | `cron:0 9 * * 1` |
| Weekdays at 9am | `0 9 * * 1-5` | `cron:0 9 * * 1-5` |
| Weekends at 10am | `0 10 * * 0,6` | `cron:0 10 * * 0,6` |
| Friday at 5pm | `0 17 * * 5` | `cron:0 17 * * 5` |

### Monthly Schedules

| Description | Cron | Command |
|-------------|------|---------|
| 1st of month at midnight | `0 0 1 * *` | `cron:0 0 1 * *` |
| 15th of month at noon | `0 12 15 * *` | `cron:0 12 15 * *` |
| Last day approach (28th) | `0 9 28 * *` | `cron:0 9 28 * *` |

## Interval Format

Simple interval-based scheduling.

| Format | Description |
|--------|-------------|
| `Ns` | Every N seconds |
| `Nm` | Every N minutes |
| `Nh` | Every N hours |
| `Nd` | Every N days |

### Interval Examples

| Description | Command |
|-------------|---------|
| Every 30 seconds | `interval:30s` |
| Every 5 minutes | `interval:5m` |
| Every 30 minutes | `interval:30m` |
| Every hour | `interval:1h` |
| Every 2 hours | `interval:2h` |
| Every day | `interval:1d` |

## One-Time Schedule

For tasks that should run only once.

| Format | Description |
|--------|-------------|
| `YYYY-MM-DD HH:MM` | Specific date and time |
| `YYYY-MM-DDTHH:MM` | ISO format |

### One-Time Examples

| Description | Command |
|-------------|---------|
| Tomorrow at 3pm | `once:2026-01-27 15:00` |
| Next Monday 9am | `once:2026-02-02 09:00` |
| Specific datetime | `once:2026-03-15 14:30` |

## Use Case Examples

### Development Tasks

```bash
# Daily code review at 9am
python create_task.py -n "Daily Review" -s "cron:0 9 * * 1-5" \
  -p "Review code changes in src/ for quality issues"

# Hourly build check
python create_task.py -n "Build Check" -s "interval:1h" \
  -p "Run build and report any errors"
```

### Maintenance Tasks

```bash
# Weekly dependency check on Monday
python create_task.py -n "Dep Check" -s "cron:0 10 * * 1" \
  -p "Check for outdated dependencies and security issues"

# Daily log cleanup at midnight
python create_task.py -n "Log Cleanup" -s "cron:0 0 * * *" \
  -p "Summarize and archive old log files"
```

### Monitoring Tasks

```bash
# Every 15 minutes health check
python create_task.py -n "Health Check" -s "interval:15m" \
  -p "Check system health and report anomalies"

# Every 6 hours status report
python create_task.py -n "Status Report" -s "cron:0 */6 * * *" \
  -p "Generate a status report of all services"
```

### Reminder Tasks

```bash
# One-time reminder
python create_task.py -n "Meeting Prep" -s "once:2026-01-27 14:00" \
  -p "Remind to prepare for the 3pm meeting"

# Daily standup reminder at 9:55am
python create_task.py -n "Standup" -s "cron:55 9 * * 1-5" \
  -p "Remind about the 10am standup meeting"
```

## Tips

1. **Use interval for simple repeating tasks** - Easier to understand than cron
2. **Use cron for precise scheduling** - When you need specific times
3. **Use once for reminders** - One-time notifications or tasks
4. **Test with dry-run first** - `python run_task.py --id xxx --dry-run`
5. **Check scheduler status** - `python list_tasks.py` shows if scheduler is running
