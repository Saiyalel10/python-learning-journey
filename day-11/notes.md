- **CLI:** Volatile, read ONCE before app starts, strongest authority
- **Config:** Persistent, editable without touching code, middle authority
- **Defaults:** Hardcoded, weakest authority, fallback of last resort

### 3. Pure Logic vs I/O: The Most Important Boundary
- **Pure Logic:** Only manipulates data already in RAM (no internet, no disk, no screen)
- **I/O:** Crosses boundaries to the Outside World (internet, disk, terminal, keyboard)
- **The Unplug Test:** If you unplug the computer from the internet and delete the hard drive, does this function still work?
  - If YES → Pure Logic
  - If NO → I/O

### 4. The Physical Reality of Data
- **RAM (Kitchen Counter):** Live Python objects (Lists, Dicts, Strings) that the CPU can work on
- **Disk (Warehouse):** Dumb text (JSON) that must be translated before use
- **The Translation Layer:**
  - `json.load(f)` → Disk to RAM (read file, translate to Python object)
  - `json.loads(s)` → String to RAM (translate JSON string to Python object)
  - `json.dump(obj, f)` → RAM to Disk (translate Python object, write to file)
  - `json.dumps(obj)` → RAM to String (translate Python object to JSON string)

### 5. Dependency Injection: The Logger Pattern
- **The Problem:** I/O stations need a logger, but they shouldn't build it themselves
- **The Solution:** Pass the logger as a parameter (inject the dependency)
- **The Flow:**
  1. `setup_logger()` builds the logger once
  2. `main()` holds the logger
  3. I/O stations receive the logger as a parameter
  4. Pure Logic stations don't need the logger (no I/O = no logging)

### 6. The Factory Metaphor: Stations and Contracts
- **Stations:** Individual functions with one job (Pure Logic or I/O)
- **Contracts:** IN (what the function receives) and OUT (what it returns)
- **The Conveyor Belt:** The `while True:` loop in `main()` that orchestrates the workflow
- **The Pre-Flight Checklist:** Unit tests that verify Pure Logic stations before integration

### 7. The Safety Net Pattern
- **The Rule:** Never crash the app. Always return a safe default.
- **Examples:**
  - Empty dict `{}` instead of `None`
  - Empty list `[]` instead of `None`
  - `try/except` blocks that catch errors and return defaults
- **Why:** The Manager (`main()`) can check `if not data:` and handle it gracefully

---

## 🔧 CLOSING THE SYNTAX TRANSLATION GAP

### The Problem
Analogies (restaurant, factory, warehouse) are perfect for **architecture** but fail at **syntax translation**. When you try to map a "sticky note" to `sys.argv.index()`, your brain short-circuits.

### The Solution: The Action-to-Tool Matrix
For every physical action, map it to:
1. **Where is the data?** (RAM, Disk, Internet, Terminal)
2. **What Python verb does this?** (method, operator, function)
3. **What's the gotcha/trap?** (edge case, common mistake)

### Key Syntax Translations

#### String Manipulation (Pure Logic)
```python
# Chop a sentence into words
words = user_input.split()  # Splits at whitespace, returns List

# Stitch words back together
payload = " ".join(words[1:])  # Joins with space separator

# Find a keyword in a list
if "--file" in sys.argv:  # Returns True/False

# Find the address of a keyword
idx = sys.argv.index("--file")  # Returns the index (first match only)

# Grab the next word
sys.argv[idx + 1]  # Math on the index