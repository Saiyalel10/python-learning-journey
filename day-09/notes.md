# Day 9 - Configuration Hierarchy & CLI Awareness
**Date:** [Insert Today's Date]

## What I Built
- Added `load_config()` to merge defaults + `config.json` safely
- Added `parse_cli_args()` to read `sys.argv` and handle `--file` / `--help` flags
- Implemented override hierarchy: CLI Flags → Config File → Defaults
- Added `max_tasks` state guard to prevent unbounded list growth

## Key Concepts
- **Configuration Management:** Settings live outside logic. Hardcoded strings are technical debt.
- **`sys.argv` as a List:** Terminal arguments arrive as `["script.py", "--file", "path.json"]`. Safe indexing prevents `IndexError`.
- **Defensive Merging:** `config.update()` + `try/except` ensures corrupt/missing config never crashes the app.
- **State Guards:** `if len(tasks) >= max_tasks:` enforces limits before mutation happens.

## Challenges
- Visualizing `sys.argv` as a plain list instead of "magic CLI variables"
- Wiring `.get("filepath", fallback)` correctly so CLI overrides config, but config overrides defaults
- Ensuring `parse_cli_args()` returns `{}` when no flags are typed

## Engineering Win
The app is now portable. Same code runs with different paths/prompts/limits via CLI flags or config files. Zero hardcoded values in business logic.