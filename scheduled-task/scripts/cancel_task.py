#!/usr/bin/env python3
"""
Cancel (disable or delete) scheduled tasks
"""

import argparse
import json
import sys
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


def save_registry(registry: dict):
    """Save the task registry"""
    registry_path = get_registry_path()
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    with open(registry_path, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)


def cancel_task(task_id: str, delete: bool = False) -> bool:
    """Cancel a specific task"""
    registry = load_registry()
    tasks = registry.get("tasks", [])
    
    found = False
    for i, task in enumerate(tasks):
        if task.get("id") == task_id:
            found = True
            if delete:
                # Delete task and its file
                task_file = get_base_dir() / task.get("taskFile", "")
                if task_file.exists():
                    task_file.unlink()
                    print(f"Deleted task file: {task_file}")
                
                tasks.pop(i)
                print(f"✅ Task {task_id} deleted")
            else:
                # Just disable the task
                task["enabled"] = False
                task["nextRun"] = None
                print(f"✅ Task {task_id} disabled")
            break
    
    if not found:
        print(f"❌ Task not found: {task_id}", file=sys.stderr)
        return False
    
    registry["tasks"] = tasks
    save_registry(registry)
    return True


def cancel_all_tasks(delete: bool = False) -> int:
    """Cancel all tasks"""
    registry = load_registry()
    tasks = registry.get("tasks", [])
    
    if not tasks:
        print("No tasks to cancel.")
        return 0
    
    count = len(tasks)
    
    if delete:
        # Delete all task files
        for task in tasks:
            task_file = get_base_dir() / task.get("taskFile", "")
            if task_file.exists():
                task_file.unlink()
        
        registry["tasks"] = []
        print(f"✅ Deleted {count} task(s)")
    else:
        # Disable all tasks
        for task in tasks:
            task["enabled"] = False
            task["nextRun"] = None
        print(f"✅ Disabled {count} task(s)")
    
    save_registry(registry)
    return count


def enable_task(task_id: str) -> bool:
    """Re-enable a disabled task"""
    registry = load_registry()
    
    for task in registry.get("tasks", []):
        if task.get("id") == task_id:
            if task.get("enabled"):
                print(f"Task {task_id} is already enabled")
                return True
            
            task["enabled"] = True
            
            # Recalculate next run time
            # Import here to avoid circular dependency
            from scheduler import get_next_run_time
            next_run = get_next_run_time(task)
            task["nextRun"] = next_run.isoformat() if next_run else None
            
            save_registry(registry)
            print(f"✅ Task {task_id} enabled")
            print(f"   Next run: {task['nextRun']}")
            return True
    
    print(f"❌ Task not found: {task_id}", file=sys.stderr)
    return False


def main():
    parser = argparse.ArgumentParser(description="Cancel scheduled tasks")
    parser.add_argument("--id", "-i",
                        help="Task ID to cancel")
    parser.add_argument("--all", "-a", action="store_true",
                        help="Cancel all tasks")
    parser.add_argument("--delete", "-d", action="store_true",
                        help="Delete task instead of just disabling")
    parser.add_argument("--enable", "-e", action="store_true",
                        help="Re-enable a disabled task")
    
    args = parser.parse_args()
    
    if args.enable:
        if not args.id:
            print("❌ --id required when using --enable", file=sys.stderr)
            sys.exit(1)
        success = enable_task(args.id)
        sys.exit(0 if success else 1)
    
    if args.all:
        cancel_all_tasks(delete=args.delete)
    elif args.id:
        success = cancel_task(args.id, delete=args.delete)
        sys.exit(0 if success else 1)
    else:
        parser.print_help()
        print()
        print("Examples:")
        print("  python cancel_task.py --id task-001        # Disable task")
        print("  python cancel_task.py --id task-001 -d     # Delete task")
        print("  python cancel_task.py --all                # Disable all")
        print("  python cancel_task.py --id task-001 -e     # Re-enable task")


if __name__ == "__main__":
    main()
