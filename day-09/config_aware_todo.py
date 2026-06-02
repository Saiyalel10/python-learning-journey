import json
import os
import sys
from typing import List, Dict, Any

# --- 1️⃣ CONFIGURATION LAYER ---

DEFAULT_CONFIG: Dict[str, Any] = {
    "filepath": "tasks.json",
    "prompt": "Command (add/done/clear/quit): ",
    "max_tasks": 50
}


def load_config() -> Dict[str, Any]:
    """Load config.json, merge with defaults. Failsafe: never crashes."""
    config = DEFAULT_CONFIG.copy()  # Start with defaults
    if os.path.exists("config.json"):
        try:
            with open("config.json", "r") as f:
                file_config = json.load(f)
                if isinstance(file_config, dict):
                    config.update(file_config)  # File overrides defaults
        except Exception:
            pass  # Corrupt/missing config? Stick to defaults
    return config


# --- 2️⃣ CLI ARGUMENT PARSER ---

def parse_cli_args() -> Dict[str, Any]:
    """Parse command-line flags. Returns overrides dictionary."""
    overrides: Dict[str, Any] = {}

    if "--help" in sys.argv:
        print("Usage: python config_aware_todo.py [--file <path>]")
        sys.exit(0)

    if "--file" in sys.argv:
        try:
            idx = sys.argv.index("--file")
            if idx + 1 < len(sys.argv):
                overrides["filepath"] = sys.argv[idx + 1]
        except Exception:
            pass  # Malformed flag? Ignore safely

    return overrides


# --- 3️⃣ EXISTING STATIONS (UNCHANGED LOGIC) ---

def load_tasks(filepath: str) -> List[Dict]:
    """📥 Load tasks from disk. Failsafe: returns [] on missing/corrupt file."""
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []


def save_tasks(filepath: str, tasks: List[Dict]) -> None:
    """💾 Persist current state to disk. Silent fail on I/O errors."""
    try:
        with open(filepath, "w") as f:
            json.dump(tasks, f, indent=4)
    except Exception:
        pass


def parse_command(raw: str) -> Dict[str, str]:
    """Translate messy input into a structured instruction ticket."""
    parts = raw.split(" ", 1)
    action = parts[0].strip().lower()
    payload = parts[1].strip() if len(parts) > 1 else ""
    return {"action": action, "payload": payload}


def update_state(tasks: List[Dict], action: str, payload: str) -> List[Dict]:
    """🔄 Modify the clipboard based on the command. Returns updated state."""
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


def format_state(tasks: List[Dict]) -> str:
    """📊 Translate data state into a human-readable string."""
    if not tasks:
        return "📑 No tasks yet. Use 'add <task>'"
    lines = []
    for t in tasks:
        icon = "✔" if t["status"] == "completed" else "⬜"
        lines.append(f"{icon} {t['task']}")
    return "\n".join(lines)


def run_tests() -> None:
    """Verify contracts before ignition."""
    assert update_state([], "add", "buy milk") == [{"task": "buy milk", "status": "pending"}]
    assert update_state([{"task": "coffee", "status": "pending"}], "done", "coffee") == [
        {"task": "coffee", "status": "completed"}]
    assert update_state([{"task": "x", "status": "pending"}], "clear", "") == []

    # Config merge test
    assert load_config().get("max_tasks") == 50  # Default fallback
    print("✔ Day 9 Tests Passed!")


# --- 4️⃣ MAIN CONDUCTOR ---

def main() -> None:
    """👔 Entry point. Routes data, manages loop, handles I/O & config."""
    # 🔧 Load & Merge Configuration
    config = load_config()
    cli_overrides = parse_cli_args()

    # Hierarchy: CLI > Config File > Defaults
    filepath = cli_overrides.get("filepath", config["filepath"])
    prompt = config["prompt"]
    max_tasks = config["max_tasks"]

    # 📥 Load State
    tasks = load_tasks(filepath)
    print(format_state(tasks))

    # 🔄 Main Loop
    while True:
        raw = input(prompt).strip()
        if not raw:
            continue

        cmd = parse_command(raw)

        if cmd["action"] == "quit":
            print(" Goodbye!")
            break

        if cmd["action"] == "add" and not cmd["payload"]:
            print("🛑 Provide task: 'add <name>'")
            print(format_state(tasks))
            continue

        # 🛡️ NEW: State Guard (Max Tasks)
        if cmd["action"] == "add" and len(tasks) >= max_tasks:
            print(f" Task limit reached ({max_tasks}). Clear some first.")
            print(format_state(tasks))
            continue

        tasks = update_state(tasks, cmd["action"], cmd["payload"])
        save_tasks(filepath, tasks)  # 💾 Persist immediately
        print(format_state(tasks))


if __name__ == "__main__":
    run_tests()
    main()