#!/usr/bin/env python3
"""
Manually run a scheduled task
"""

import argparse
import json
import logging
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


def save_registry(registry: dict):
    """Save the task registry"""
    registry_path = get_registry_path()
    with open(registry_path, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)


def get_task_by_id(task_id: str) -> dict:
    """Get a task by its ID"""
    registry = load_registry()
    for task in registry.get("tasks", []):
        if task.get("id") == task_id:
            return task
    return None


def run_task(task_id: str, dry_run: bool = False):
    """Run a specific task"""
    task = get_task_by_id(task_id)
    
    if not task:
        print(f"❌ Task not found: {task_id}", file=sys.stderr)
        sys.exit(1)
    
    task_name = task.get("name", "Unnamed")
    task_file = get_base_dir() / task.get("taskFile", "")
    working_dir = task.get("workingDir", str(Path.cwd()))
    
    print(f"Task: {task_name} ({task_id})")
    print(f"Task File: {task_file}")
    print(f"Working Directory: {working_dir}")
    print()
    
    if not task_file.exists():
        print(f"❌ Task file not found: {task_file}", file=sys.stderr)
        sys.exit(1)
    
    # Read task content
    with open(task_file, "r", encoding="utf-8") as f:
        task_content = f.read()
    
    if dry_run:
        print("=== DRY RUN - Task Content ===")
        print(task_content)
        print("=== END ===")
        print()
        print("Would execute: claude --print <task_content>")
        print(f"In directory: {working_dir}")
        return
    
    print("Executing task...")
    print()
    
    # Import and use execute_task from scheduler
    try:
        # Setup basic logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s"
        )
        logger = logging.getLogger(__name__)
        
        # Import execute function
        from scheduler import execute_task, update_task_after_run, load_registry
        
        success = execute_task(task, logger)
        
        # Update task status
        registry = load_registry()
        update_task_after_run(registry, task_id, success)
        
        if success:
            print()
            print(f"✅ Task completed successfully")
            
            # Show result file location
            results_dir = get_base_dir() / "results"
            results = sorted(results_dir.glob(f"{task_id}_*.md"), reverse=True)
            if results:
                print(f"Result saved to: {results[0]}")
        else:
            print()
            print(f"❌ Task failed")
            sys.exit(1)
    
    except ImportError as e:
        print(f"❌ Could not import scheduler module: {e}", file=sys.stderr)
        print("Make sure you're running from the correct directory.", file=sys.stderr)
        sys.exit(1)


def list_available_tasks():
    """List tasks that can be run"""
    registry = load_registry()
    tasks = registry.get("tasks", [])
    
    if not tasks:
        print("No tasks available.")
        return
    
    print("Available tasks:")
    print()
    for task in tasks:
        enabled = "✓" if task.get("enabled", True) else "✗"
        print(f"  [{enabled}] {task['id']}: {task.get('name', 'Unnamed')}")
    print()
    print("Run a task with: python run_task.py --id <task-id>")


def main():
    parser = argparse.ArgumentParser(description="Manually run a scheduled task")
    parser.add_argument("--id", "-i",
                        help="Task ID to run")
    parser.add_argument("--dry-run", "-n", action="store_true",
                        help="Show what would be executed without running")
    parser.add_argument("--list", "-l", action="store_true",
                        help="List available tasks")
    
    args = parser.parse_args()
    
    if args.list:
        list_available_tasks()
        return
    
    if not args.id:
        parser.print_help()
        print()
        print("Examples:")
        print("  python run_task.py --list              # List available tasks")
        print("  python run_task.py --id task-001       # Run task")
        print("  python run_task.py --id task-001 -n    # Dry run (preview)")
        return
    
    run_task(args.id, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
