import json
import os
import sys
import logging
from typing import List, Dict, Any


# --- 0️⃣ LOGGING SETUP (The Black Box) ---
def setup_logger() -> logging.Logger:
    """Configure diagnostic trail. Separates dev logs from user UI."""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger


# --- 1️ CONFIGURATION LAYER (Now logs failures) ---
DEFAULT_CONFIG: Dict[str, Any] = {
    "filepath": "tasks.json",
    "prompt": "Command (add/done/clear/quit): ",
    "max_tasks": 50
}


def load_config(logger: logging.Logger) -> Dict[str, Any]:
    """Load config.json, merge with defaults. Logs issues instead of silencing them."""
    config = DEFAULT_CONFIG.copy()
    if not os.path.exists("config.json"):
        logger.warning("config.json not found. Using defaults.")
        return config

    try:
        with open("config.json", "r") as f:
            file_config = json.load(f)
            if isinstance(file_config, dict):
                config.update(file_config)
                logger.info("Configuration loaded successfully.")
            else:
                logger.warning("config.json is not a valid dictionary. Using defaults.")
    except Exception as e:
        logger.error(f"Failed to read config.json: {e}. Using defaults.")
    return config


# --- 2️ CLI ARGUMENT PARSER (Unchanged) ---
def parse_cli_args() -> Dict[str, Any]:
    """Parse command line flags. Returns overrides dictionary."""
    overrides: Dict[str, Any] = {}
    if "--help" in sys.argv:
        print("Usage: python logging_recovery.py [--file <path>]")
        sys.exit(0)

    if "--file" in sys.argv:
        try:
            idx = sys.argv.index("--file")
            if idx + 1 < len(sys.argv):
                overrides["filepath"] = sys.argv[idx + 1]
        except Exception:
            pass
    return overrides


# --- 3️⃣ LOAD TASKS (Now logs state) ---
def load_tasks(filepath: str, logger: logging.Logger) -> List[Dict]:
    """Load tasks from disk. Logs missing/corrupt files."""
    if not os.path.exists(filepath):
        logger.info(f"File '{filepath}' not found. Starting with empty list.")
        return []
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
            if isinstance(data, list):
                logger.info(f"Loaded {len(data)} tasks from '{filepath}'.")
                return data
            logger.warning(f"'{filepath}' contains invalid format. Starting fresh.")
            return []
    except Exception as e:
        logger.error(f"Failed to load tasks from '{filepath}': {e}")
        return []


# --- 4️⃣ SAVE TASKS (Now logs write failures) ---
def save_tasks(filepath: str, tasks: List[Dict], logger: logging.Logger) -> None:
    """Persist current state to disk. Logs errors instead of silencing."""
    try:
        with open(filepath, "w") as f:
            json.dump(tasks,f,indent=4)
        logger.info(f"State saved to '{filepath}'.")
    except Exception as e:
        logger.error(f"Failed to save tasks to '{filepath}': {e}")


# --- 5️ PARSE COMMAND (Pure Logic: No logging/printing) ---
def parse_command(raw: str) -> Dict[str, str]:
    """Translate messy input into a structured instruction ticket."""
    parts = raw.split(" ", 1)
    action = parts[0].strip().lower()
    payload = parts[1].strip() if len(parts) > 1 else ""
    return {"action": action, "payload": payload}


# --- 6️ UPDATE TASKS (Pure Logic: No logging/printing) ---
def update_tasks(tasks: List[Dict], action: str, payload: str) -> List[Dict]:
    """Modify the clipboard based on the command. Returns updated state."""
    if action == "add":
        if payload:
            tasks.append({"task": payload, "status": "pending"})
    elif action == "done":
        for t in tasks:
            if t["task"] == payload:
                t["status"] = "completed"
                break
    elif action == "clear":
        tasks.clear()
    return tasks


# --- 7️⃣ FORMAT STATE (Pure Logic: No logging/printing) ---
def format_state(tasks: List[Dict]) -> str:
    """Translate data state into a human-readable string."""
    if not tasks:
        return " No tasks yet: 'add <task>'"
    lines = []
    for t in tasks:
        icon = "✔" if t["status"] == "completed" else "⬜"
        lines.append(f"{icon} {t['task']}")
    return "\n".join(lines)


# --- 8️⃣ RUN TESTS (Logs will appear during tests; this is normal) ---
def run_tests() -> None:
    """Verify contracts before ignition."""
    assert update_tasks([], "add", "buy milk") == [{"task": "buy milk", "status": "pending"}]
    assert update_tasks([{"task": "buy milk", "status": "pending"}], "done", "buy milk") == [
        {"task": "buy milk", "status": "completed"}]
    assert update_tasks([{"task": "x", "status": "pending"}], "clear", "") == []
    print("✅ All simulated tests passed!")


# --- 9️⃣ MAIN CONDUCTOR (Injects logger into I/O stations) ---
def main() -> None:
    """Program entry point. Routes data, manages loop, handles I/O & config."""
    logger = setup_logger()  # Initialize black box

    config = load_config(logger)
    cli_overrides = parse_cli_args()

    filepath = cli_overrides.get("filepath", config["filepath"])
    prompt = config["prompt"]
    max_tasks = config["max_tasks"]

    tasks = load_tasks(filepath, logger)
    print(format_state(tasks))  # 🖥️ UI only

    while True:
        raw = input(prompt).strip()
        if not raw:
            continue

        cmd = parse_command(raw)
        if cmd["action"] == "quit":
            logger.info("User requested exit.")
            print("👋 Goodbye!")
            break
        if cmd["action"] == "add" and not cmd["payload"]:
            print("🛑 Provide task: 'add <name>'")
            print(format_state(tasks))
            continue
        if cmd["action"] == "add" and len(tasks) >= max_tasks:
            print(f"🚩 Task limit reached ({max_tasks}). Clear some first.")
            print(format_state(tasks))
            continue

        tasks = update_tasks(tasks, cmd["action"], cmd["payload"])
        save_tasks(filepath, tasks, logger)  # 💾 Logs on success/failure
        print(format_state(tasks))


# --- 🔟 ROOT ---
if __name__ == "__main__":
    run_tests()
    main()