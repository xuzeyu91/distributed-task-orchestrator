#!/usr/bin/env python3
"""
List all scheduled tasks
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path


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


def format_datetime(dt_str: str) -> str:
    """Format datetime string for display"""
    if not dt_str:
        return "-"
    try:
        dt = datetime.fromisoformat(dt_str)
        return dt.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return dt_str


def is_scheduler_running(pid: int) -> bool:
    """Check if the scheduler process is running"""
    if pid is None:
        return False
    
    try:
        if sys.platform == "win32":
            import subprocess
            result = subprocess.run(
                ["tasklist", "/FI", f"PID eq {pid}"],
                capture_output=True, text=True
            )
            return str(pid) in result.stdout
        else:
            os.kill(pid, 0)
            return True
    except (OSError, subprocess.SubprocessError):
        return False


def list_tasks(show_all: bool = False, as_json: bool = False):
    """List all scheduled tasks"""
    registry = load_registry()
    tasks = registry.get("tasks", [])
    scheduler_pid = registry.get("schedulerPid")
    
    if as_json:
        print(json.dumps({
            "tasks": tasks,
            "schedulerPid": scheduler_pid,
            "schedulerRunning": is_scheduler_running(scheduler_pid)
        }, indent=2, ensure_ascii=False))
        return
    
    # Filter disabled tasks unless --all
    if not show_all:
        tasks = [t for t in tasks if t.get("enabled", True)]
    
    if not tasks:
        print("No scheduled tasks found.")
        print()
        print("Create a task with:")
        print('  python create_task.py --name "My Task" --schedule "cron:0 9 * * *" --prompt "Do something"')
        return
    
    # Scheduler status
    if is_scheduler_running(scheduler_pid):
        print(f"🟢 Scheduler running (PID: {scheduler_pid})")
    else:
        print("🔴 Scheduler not running")
        print("   Start with: python scheduler.py --daemon")
    print()
    
    # Print header
    print(f"{'ID':<12} {'Name':<25} {'Schedule':<20} {'Next Run':<18} {'Status':<10}")
    print("-" * 90)
    
    for task in tasks:
        task_id = task.get("id", "?")
        name = task.get("name", "Unnamed")[:24]
        schedule_desc = task.get("schedule", {}).get("description", "-")[:19]
        next_run = format_datetime(task.get("nextRun"))
        
        # Status indicator
        enabled = task.get("enabled", True)
        last_status = task.get("lastStatus")
        
        if not enabled:
            status = "⏸ Disabled"
        elif last_status == "success":
            status = "✅ Success"
        elif last_status == "failed":
            status = "❌ Failed"
        else:
            status = "🟡 Pending"
        
        print(f"{task_id:<12} {name:<25} {schedule_desc:<20} {next_run:<18} {status:<10}")
    
    print()
    print(f"Total: {len(tasks)} task(s)")


def main():
    parser = argparse.ArgumentParser(description="List scheduled tasks")
    parser.add_argument("--all", "-a", action="store_true",
                        help="Show all tasks including disabled")
    parser.add_argument("--json", "-j", action="store_true",
                        help="Output as JSON")
    
    args = parser.parse_args()
    list_tasks(show_all=args.all, as_json=args.json)


if __name__ == "__main__":
    main()
