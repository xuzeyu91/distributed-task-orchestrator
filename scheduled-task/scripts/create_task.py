#!/usr/bin/env python3
"""
Create a new scheduled task
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# Try to import croniter for validation
try:
    from croniter import croniter
    HAS_CRONITER = True
except ImportError:
    HAS_CRONITER = False


def get_base_dir() -> Path:
    """Get the .scheduled-tasks directory"""
    return Path.cwd() / ".scheduled-tasks"


def get_registry_path() -> Path:
    """Get the registry.json path"""
    return get_base_dir() / "registry.json"


def load_registry() -> dict:
    """Load the task registry"""
    registry_path = get_registry_path()
    if registry_path.exists():
        with open(registry_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"tasks": [], "schedulerPid": None}


def save_registry(registry: dict):
    """Save the task registry"""
    registry_path = get_registry_path()
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    with open(registry_path, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)


def generate_task_id(registry: dict) -> str:
    """Generate a unique task ID"""
    existing_ids = [t.get("id", "") for t in registry.get("tasks", [])]
    
    for i in range(1, 1000):
        task_id = f"task-{i:03d}"
        if task_id not in existing_ids:
            return task_id
    
    # Fallback to timestamp-based ID
    return f"task-{int(datetime.now().timestamp())}"


def parse_schedule(schedule_str: str) -> dict:
    """
    Parse schedule string into structured format
    
    Formats:
    - cron:0 9 * * *     -> Cron expression
    - interval:30m       -> Every 30 minutes
    - interval:2h        -> Every 2 hours
    - once:2026-01-27 15:00 -> One-time execution
    """
    if ":" not in schedule_str:
        raise ValueError(f"Invalid schedule format: {schedule_str}")
    
    stype, expr = schedule_str.split(":", 1)
    stype = stype.strip().lower()
    expr = expr.strip()
    
    if stype == "cron":
        # Validate cron expression
        if HAS_CRONITER:
            try:
                croniter(expr)
            except Exception as e:
                raise ValueError(f"Invalid cron expression: {e}")
        
        # Generate human-readable description
        desc = describe_cron(expr)
        return {"type": "cron", "expression": expr, "description": desc}
    
    elif stype == "interval":
        # Validate interval format (e.g., 30m, 2h, 1d)
        if not re.match(r"^\d+[smhd]$", expr, re.IGNORECASE):
            raise ValueError(f"Invalid interval format: {expr}. Use format like 30m, 2h, 1d")
        
        desc = describe_interval(expr)
        return {"type": "interval", "expression": expr, "description": desc}
    
    elif stype == "once":
        # Validate datetime format
        try:
            dt = datetime.fromisoformat(expr.replace(" ", "T"))
            if dt <= datetime.now():
                raise ValueError(f"Scheduled time must be in the future: {expr}")
        except ValueError as e:
            raise ValueError(f"Invalid datetime format: {expr}. Use YYYY-MM-DD HH:MM")
        
        return {"type": "once", "expression": expr, "description": f"Once at {expr}"}
    
    else:
        raise ValueError(f"Unknown schedule type: {stype}. Use cron, interval, or once")


def describe_cron(expr: str) -> str:
    """Generate human-readable description for cron expression"""
    parts = expr.split()
    if len(parts) != 5:
        return expr
    
    minute, hour, day, month, weekday = parts
    
    # Common patterns
    if expr == "* * * * *":
        return "Every minute"
    if expr == "0 * * * *":
        return "Every hour"
    if minute != "*" and hour != "*" and day == "*" and month == "*" and weekday == "*":
        return f"Daily at {hour.zfill(2)}:{minute.zfill(2)}"
    if minute != "*" and hour != "*" and weekday == "1-5":
        return f"Weekdays at {hour.zfill(2)}:{minute.zfill(2)}"
    if minute != "*" and hour != "*" and weekday == "0,6":
        return f"Weekends at {hour.zfill(2)}:{minute.zfill(2)}"
    
    return expr


def describe_interval(expr: str) -> str:
    """Generate human-readable description for interval"""
    unit_names = {"s": "second", "m": "minute", "h": "hour", "d": "day"}
    value = expr[:-1]
    unit = expr[-1].lower()
    
    unit_name = unit_names.get(unit, unit)
    if int(value) > 1:
        unit_name += "s"
    
    return f"Every {value} {unit_name}"


def calculate_next_run(schedule: dict) -> Optional[str]:
    """Calculate the next run time"""
    stype = schedule.get("type")
    expr = schedule.get("expression")
    now = datetime.now()
    
    if stype == "cron":
        if HAS_CRONITER:
            try:
                cron = croniter(expr, now)
                next_run = cron.get_next(datetime)
                return next_run.isoformat()
            except Exception:
                pass
        return None
    
    elif stype == "interval":
        # For new interval tasks, start immediately or after first interval
        return now.isoformat()
    
    elif stype == "once":
        return expr.replace(" ", "T")
    
    return None


def create_task_file(task_id: str, name: str, prompt: str, 
                     working_dir: str, focus_files: Optional[str]) -> Path:
    """Create the task markdown file"""
    tasks_dir = get_base_dir() / "tasks"
    tasks_dir.mkdir(parents=True, exist_ok=True)
    
    task_file = tasks_dir / f"{task_id}.md"
    
    focus_section = ""
    if focus_files:
        focus_section = f"- **Focus Files:** {focus_files}\n"
    
    content = f"""# Task: {name}

## Context
- **Working Directory:** {working_dir}
{focus_section}
## Instructions

{prompt}

## Output Requirements
- Format: Markdown report
- Be concise and actionable
"""
    
    with open(task_file, "w", encoding="utf-8") as f:
        f.write(content)
    
    return task_file


def create_task(name: str, schedule_str: str, prompt: str,
                working_dir: Optional[str] = None,
                focus_files: Optional[str] = None) -> dict:
    """Create a new scheduled task"""
    
    # Parse and validate schedule
    schedule = parse_schedule(schedule_str)
    
    # Load registry
    registry = load_registry()
    
    # Generate task ID
    task_id = generate_task_id(registry)
    
    # Determine working directory
    if working_dir is None:
        working_dir = str(Path.cwd())
    else:
        working_dir = str(Path(working_dir).resolve())
    
    # Create task file
    task_file = create_task_file(task_id, name, prompt, working_dir, focus_files)
    task_file_rel = str(task_file.relative_to(get_base_dir()))
    
    # Calculate next run
    next_run = calculate_next_run(schedule)
    
    # Create task entry
    task = {
        "id": task_id,
        "name": name,
        "schedule": schedule,
        "taskFile": task_file_rel,
        "workingDir": working_dir,
        "enabled": True,
        "lastRun": None,
        "lastStatus": None,
        "nextRun": next_run,
        "createdAt": datetime.now().isoformat()
    }
    
    # Add to registry
    registry["tasks"].append(task)
    save_registry(registry)
    
    return task


def main():
    parser = argparse.ArgumentParser(description="Create a scheduled task")
    parser.add_argument("--name", "-n", required=True,
                        help="Task name")
    parser.add_argument("--schedule", "-s", required=True,
                        help="Schedule (cron:expr, interval:30m, once:datetime)")
    parser.add_argument("--prompt", "-p", required=True,
                        help="Task instructions for Claude")
    parser.add_argument("--working-dir", "-w",
                        help="Working directory (default: current)")
    parser.add_argument("--focus-files", "-f",
                        help="File patterns to focus on (e.g., src/**/*.ts)")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON")
    
    args = parser.parse_args()
    
    try:
        task = create_task(
            name=args.name,
            schedule_str=args.schedule,
            prompt=args.prompt,
            working_dir=args.working_dir,
            focus_files=args.focus_files
        )
        
        if args.json:
            print(json.dumps(task, indent=2, ensure_ascii=False))
        else:
            print(f"✅ Task created successfully!")
            print(f"   ID: {task['id']}")
            print(f"   Name: {task['name']}")
            print(f"   Schedule: {task['schedule']['description']}")
            print(f"   Next Run: {task['nextRun']}")
            print(f"   Task File: {task['taskFile']}")
            print()
            print("Start the scheduler with:")
            print("  python scheduler.py --daemon")
    
    except ValueError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
