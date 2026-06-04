# Day 10 - Logging, Graceful Recovery & The Architect's Funnel
**Date:** June 6, 2026

## What I Built
- Replaced silent `pass` blocks with a professional `logging` setup.
- Injected the `logger` dependency into I/O stations (`load_config`, `load_tasks`, `save_tasks`).
- Strictly separated User UI (`print`) from Developer Diagnostics (`logging`).

## The "Meta-Bug" Breakthrough
- **The Trap:** I was cramming the 20% (syntax) and ignoring the 80% (architecture/orchestration).
- **The Fix:** The **Architect's Funnel**. 
  1. Napkin (Analogy/Constants)
  2. Reverse Trace (Data Contracts)
  3. Comment-First (Logic in English)
  4. Syntax (Translation)
- **The 4 Universal Constants:** State, I/O, Control Flow, Abstraction. Every program is just a rearrangement of these.

## Engineering Win
I stopped looking at code as "scary syntax" and started seeing it as a system of workers passing a clipboard. The cognitive load dropped massively.