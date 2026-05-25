from typing import List, Dict


def parse_command(raw: str) -> Dict[str, str]:
    """Split raw input into action and payload. Returns a labeled pair."""
    parts = raw.split(" ", 1)  # Split only at the FIRST space
    action = parts[0].strip().lower()
    payload = parts[1].strip() if len(parts) > 1 else ""
    return {"action": action, "payload": payload}


def update_state(tasks: List[Dict], action: str, payload: str) -> List[Dict]:
    """Modify task list based on action. Returns the updated list."""
    if action == "add":
        if payload:  # Only add if a task name was provided
            tasks.append({"task": payload, "status": "pending"})
    elif action == "done":
        for t in tasks:
            if t["task"] == payload:
                t["status"] = "completed"
                break  # Stop after finding the match
    elif action == "clear":
        tasks.clear()  # Empties the list in place
    # Unknown actions do nothing; list stays unchanged
    return tasks


def format_state(tasks: List[Dict]) -> str:
    """Convert task list into a readable string. Returns formatted text."""
    if not tasks:
        return "📋 No tasks yet. Use 'add <task>'"

    lines = []
    for t in tasks:
        icon = "✅" if t["status"] == "completed" else ""
        lines.append(f"{icon} {t['task']}")
    return "\n".join(lines)


def run_tests() -> None:
    """Automated verification. Runs before manual input."""
    # Test 1: Add a task
    t1 = update_state([], "add", "buy milk")
    assert t1 == [{"task": "buy milk", "status": "pending"}]

    # Test 2: Mark done
    t2 = update_state([{"task": "buy milk", "status": "pending"}], "done", "buy milk")
    assert t2 == [{"task": "buy milk", "status": "completed"}]

    # Test 3: Clear all
    t3 = update_state([{"task": "x", "status": "pending"}], "clear", "")
    assert t3 == []

    print("✅ All automated tests passed.")


def main() -> None:
    """CLI entry point. Orchestrates the pipeline."""
    tasks = []  # Start with an empty checklist
    while True:
        raw = input("Command (add/done/clear/quit): ").strip()
        if not raw:
            continue  # Skip empty Enter presses

        cmd = parse_command(raw)  # 🧼 Prep: shape the input

        if cmd["action"] == "quit":
            print(" Goodbye!")
            break

        # Validation feedback (kept in main, not in logic)
        if cmd["action"] == "add" and not cmd["payload"]:
            print("⚠️ Please provide a task: 'add <name>'")
            print(format_state(tasks))
            continue

        tasks = update_state(tasks, cmd["action"], cmd["payload"])  # 📊 Logic: update state
        print(format_state(tasks))  # 📝 Format: display result


if __name__ == "__main__":
    run_tests()
    main()