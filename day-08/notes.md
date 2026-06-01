# Day 8 - Persistence & Defensive I/O
**Date:** [Today's Date]

## What I Built
- Added `load_tasks()` to read from JSON file
- Added `save_tasks()` to persist state after every change
- Tasks now survive terminal restarts

## Key Concepts
- **Serialization:** Converting Python objects ↔ JSON text
- **Defensive Programming:** `try/except` wraps all file I/O
- **Fallback Pattern:** Missing/corrupt file → return `[]`
- **Contract Headers:** Every function declares exact input/output types

## Challenges
- Fixed `json.dump()` argument order: `dump(data, file)` not `dump(file)`
- Ensured `load_tasks()` validates data is actually a list
- Added `save_tasks()` call inside the loop (not just at quit)

## Engineering Win
File operations are unpredictable. My app never crashes on I/O errors anymore.