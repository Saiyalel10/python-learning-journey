import json
import os
from typing import List, Dict


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
    """ Translate messy input into a structured instruction ticket."""
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
    """ Verify contracts before ignition."""
    assert update_state([], "add", "buy milk") == [{"task": "buy milk", "status": "pending"}]
    assert update_state([{"task": "coffee", "status": "pending"}], "done", "coffee") == [
        {"task": "coffee", "status": "completed"}]
    assert update_state([{"task": "x", "status": "pending"}], "clear", "") == []

    save_tasks("test_tasks.json", [{"task": "temp", "status": "pending"}])
    assert load_tasks("test_tasks.json") == [{"task": "temp", "status": "pending"}]
    os.remove("test_tasks.json")

    print("✔ Day 8 Tests Passed!")


def main() -> None:
    """👔 Entry point. Routes data, manages loop, handles I/O."""
    filepath = "tasks.json"
    tasks = load_tasks(filepath)
    print(format_state(tasks))

    while True:
        raw = input("Command (add/done/clear/quit): ").strip()
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

        tasks = update_state(tasks, cmd["action"], cmd["payload"])
        save_tasks(filepath, tasks)  # 💾 Persist immediately
        print(format_state(tasks))


if __name__ == "__main__":
    run_tests()
    main()