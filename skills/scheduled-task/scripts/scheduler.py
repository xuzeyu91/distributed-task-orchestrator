#!/usr/bin/env python3
"""
Scheduled Task Scheduler - Core scheduling daemon
Runs in background, executes due tasks via Claude CLI
"""

import argparse
import json
import logging
import os
import signal
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

# Try to import croniter for cron parsing
try:
    from croniter import croniter
    HAS_CRONITER = True
except ImportError:
    HAS_CRONITER = False
    print("Warning: croniter not installed. Cron expressions won't work.")
    print("Install with: pip install croniter")

# Import local notification module
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

try:
    from notify import send_notification
except ImportError:
    def send_notification(title, message):
        print(f"[NOTIFY] {title}: {message}")


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


def setup_logging():
    """Setup logging to file and console"""
    log_dir = get_base_dir() / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    log_file = log_dir / "scheduler.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)


def parse_interval(interval_str: str) -> int:
    """Parse interval string to seconds (e.g., '30m' -> 1800)"""
    multipliers = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    unit = interval_str[-1].lower()
    if unit in multipliers:
        try:
            value = int(interval_str[:-1])
            return value * multipliers[unit]
        except ValueError:
            pass
    raise ValueError(f"Invalid interval format: {interval_str}")


def get_next_run_time(task: dict) -> Optional[datetime]:
    """Calculate next run time for a task"""
    schedule = task.get("schedule", {})
    stype = schedule.get("type")
    expr = schedule.get("expression")
    
    now = datetime.now()
    
    if stype == "cron":
        if not HAS_CRONITER:
            return None
        try:
            cron = croniter(expr, now)
            return cron.get_next(datetime)
        except Exception:
            return None
    
    elif stype == "interval":
        try:
            interval_secs = parse_interval(expr)
            last_run = task.get("lastRun")
            if last_run:
                last_dt = datetime.fromisoformat(last_run)
                next_run = last_dt.replace(microsecond=0) + \
                           __import__("datetime").timedelta(seconds=interval_secs)
                if next_run <= now:
                    return now
                return next_run
            else:
                # First run: schedule for now + interval
                return now
        except Exception:
            return None
    
    elif stype == "once":
        try:
            run_time = datetime.fromisoformat(expr.replace(" ", "T"))
            if run_time > now:
                return run_time
            return None  # Already passed
        except Exception:
            return None
    
    return None


def is_task_due(task: dict) -> bool:
    """Check if a task is due for execution"""
    if not task.get("enabled", True):
        return False
    
    next_run_str = task.get("nextRun")
    if not next_run_str:
        return False
    
    try:
        next_run = datetime.fromisoformat(next_run_str)
        return datetime.now() >= next_run
    except Exception:
        return False


def execute_task(task: dict, logger: logging.Logger) -> bool:
    """Execute a task using Claude CLI"""
    task_id = task.get("id", "unknown")
    task_name = task.get("name", "Unnamed Task")
    task_file = get_base_dir() / task.get("taskFile", "")
    working_dir = task.get("workingDir", str(Path.cwd()))
    
    logger.info(f"Executing task: {task_id} - {task_name}")
    
    if not task_file.exists():
        logger.error(f"Task file not found: {task_file}")
        send_notification("Task Failed", f"Task file not found: {task_name}")
        return False
    
    # Read task content
    with open(task_file, "r", encoding="utf-8") as f:
        task_content = f.read()
    
    # Prepare result file
    results_dir = get_base_dir() / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    result_file = results_dir / f"{task_id}_{timestamp}.md"
    
    try:
        # Execute Claude CLI
        logger.info(f"Running claude --print for task {task_id}")
        
        result = subprocess.run(
            ["claude", "--print", task_content],
            cwd=working_dir,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        # Save result
        output = result.stdout if result.returncode == 0 else result.stderr
        
        result_content = f"""# Task Result: {task_name}

## Execution Info
- **Task ID:** {task_id}
- **Executed At:** {datetime.now().isoformat()}
- **Working Directory:** {working_dir}
- **Status:** {"Success" if result.returncode == 0 else "Failed"}

## Output

{output}
"""
        
        with open(result_file, "w", encoding="utf-8") as f:
            f.write(result_content)
        
        logger.info(f"Result saved to: {result_file}")
        
        if result.returncode == 0:
            send_notification(
                "Task Completed",
                f"{task_name} executed successfully"
            )
            return True
        else:
            send_notification(
                "Task Failed",
                f"{task_name} failed: {result.stderr[:100]}"
            )
            return False
    
    except subprocess.TimeoutExpired:
        logger.error(f"Task {task_id} timed out")
        send_notification("Task Timeout", f"{task_name} timed out after 5 minutes")
        return False
    
    except FileNotFoundError:
        logger.error("Claude CLI not found. Please install it first.")
        send_notification("Error", "Claude CLI not found")
        return False
    
    except Exception as e:
        logger.error(f"Error executing task {task_id}: {e}")
        send_notification("Task Error", f"{task_name}: {str(e)[:100]}")
        return False


def update_task_after_run(registry: dict, task_id: str, success: bool):
    """Update task status after execution"""
    for task in registry.get("tasks", []):
        if task.get("id") == task_id:
            task["lastRun"] = datetime.now().isoformat()
            task["lastStatus"] = "success" if success else "failed"
            
            # Calculate next run time
            schedule = task.get("schedule", {})
            if schedule.get("type") == "once":
                # One-time task: disable after execution
                task["enabled"] = False
                task["nextRun"] = None
            else:
                next_run = get_next_run_time(task)
                task["nextRun"] = next_run.isoformat() if next_run else None
            
            break
    
    save_registry(registry)


def run_scheduler(interval: int = 60, once: bool = False, logger: logging.Logger = None):
    """Main scheduler loop"""
    if logger is None:
        logger = setup_logging()
    
    logger.info(f"Scheduler started (interval: {interval}s, once: {once})")
    
    # Update PID in registry
    registry = load_registry()
    registry["schedulerPid"] = os.getpid()
    save_registry(registry)
    
    def check_and_run():
        registry = load_registry()
        
        for task in registry.get("tasks", []):
            if is_task_due(task):
                task_id = task.get("id")
                logger.info(f"Task {task_id} is due, executing...")
                
                success = execute_task(task, logger)
                update_task_after_run(registry, task_id, success)
                
                # Reload registry after update
                registry = load_registry()
    
    if once:
        check_and_run()
        logger.info("Single check completed, exiting")
        return
    
    # Continuous loop
    try:
        while True:
            check_and_run()
            time.sleep(interval)
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user")
    finally:
        # Clear PID on exit
        registry = load_registry()
        registry["schedulerPid"] = None
        save_registry(registry)


def daemonize():
    """Run the scheduler as a background daemon (Unix-like systems)"""
    if sys.platform == "win32":
        # Windows: use subprocess to run in background
        script_path = Path(__file__).resolve()
        subprocess.Popen(
            [sys.executable, str(script_path), "--interval", "60"],
            creationflags=subprocess.CREATE_NO_WINDOW,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print("Scheduler started in background")
        return
    
    # Unix: fork to background
    try:
        pid = os.fork()
        if pid > 0:
            print(f"Scheduler started in background (PID: {pid})")
            sys.exit(0)
    except OSError as e:
        print(f"Fork failed: {e}")
        sys.exit(1)
    
    # Decouple from parent environment
    os.setsid()
    os.umask(0)
    
    # Second fork
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError:
        sys.exit(1)
    
    # Redirect standard file descriptors
    sys.stdout.flush()
    sys.stderr.flush()
    
    with open("/dev/null", "r") as null_in:
        os.dup2(null_in.fileno(), sys.stdin.fileno())
    
    log_file = get_base_dir() / "logs" / "scheduler.log"
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(log_file, "a") as log_out:
        os.dup2(log_out.fileno(), sys.stdout.fileno())
        os.dup2(log_out.fileno(), sys.stderr.fileno())
    
    run_scheduler()


def main():
    parser = argparse.ArgumentParser(description="Scheduled Task Scheduler")
    parser.add_argument("--daemon", "-d", action="store_true",
                        help="Run as background daemon")
    parser.add_argument("--once", action="store_true",
                        help="Check and run due tasks once, then exit")
    parser.add_argument("--interval", "-i", type=int, default=60,
                        help="Check interval in seconds (default: 60)")
    
    args = parser.parse_args()
    
    if args.daemon:
        daemonize()
    else:
        logger = setup_logging()
        run_scheduler(interval=args.interval, once=args.once, logger=logger)


if __name__ == "__main__":
    main()
