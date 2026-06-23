import json
import os
import sys
import requests
import logging
from typing import List, Dict, Any


# --- 0️⃣ SETUP LOGGER (The Black Box) ---
def setup_logger() -> logging.Logger:
    """Configure diagnostic trail."""
    logger = logging.getLogger(__name__)

    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()  # ✅ FIX 1: Added () to instantiate the object
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


# --- 1️⃣ CONFIGURATION LAYER ---
DEFAULT_CONFIG: Dict[str, Any] = {
    "filepath": "weather_log.json",
    "prompt": "Command(weather/clear/quit)",
    "max_logs": 50,
    "api_key": "c61b50c6090f10f3d389393c2447be78"
}


# --- 2️⃣ LOAD CONFIGS ---
def load_config(logger: logging.Logger) -> Dict[str, Any]:
    """This station reads from disk and loads it to the live RAM, merges the dictionary and returns an updated config."""
    config = DEFAULT_CONFIG.copy()  # creating a whiteboard

    if os.path.exists("config.json"):  # checking if file exists
        try:  # error handling
            with open("config.json", "r") as f:  # open it as file
                data = json.load(f)  # this is where the loading is happening
                if not isinstance(data, dict):  # check valid format
                    logger.warning("Invalid file format, using defaults.")  # diagnostic trail
                else:
                    config.update(data)  # surviving path
                    logger.info("File loaded successfully!")
        except Exception as e:  # trail errors as well
            logger.error(f"file could not load: {e}. Using defaults")

    return config  # what comes out at the end of the tunnel


# --- 3️⃣ PARSE CLI ARGS (The Receptionist) ---
def parse_cli_args() -> Dict[str, Any]:
    """Parse command line flags. Returns overrides dictionary."""
    overrides: Dict[str, Any] = {}

    if "--help" in sys.argv:
        print("Usage: python weather_api.py [--file <path>]")
        sys.exit(0)

    if "--file" in sys.argv:
        try:
            idx = sys.argv.index("--file")
            if idx + 1 < len(sys.argv):
                overrides["filepath"] = sys.argv[idx + 1]
        except Exception:
            pass

    return overrides


# --- 6️⃣ LOAD STATE (Formerly load_tasks) ---
def load_state(filepath: str, logger: logging.Logger) -> List[Dict]:
    """Pulls file from disk and reads it to the RAM"""
    if not os.path.exists(filepath):
        logger.info(f"The file on {filepath} does not exist. Starting afresh.")
        return []

    try:
        with open(filepath, "r") as f:
            data = json.load(f)

            # ✅ FIX 2: Removed 'not' - if it IS a list, return it
            if isinstance(data, list):
                logger.info(f"Loaded {len(data)} entries from {filepath}.")
                return data
            else:
                logger.warning(f"{filepath} is not a valid list. Starting fresh.")
                return []

    except json.JSONDecodeError as e:
        logger.warning(f"Failed to parse {filepath}: {e}. Starting afresh.")
        return []

    except Exception as e:
        logger.error(f"Failed to read {filepath} : {e}. Starting afresh.")  # ✅ Fixed: was logging.error
        return []


# --- 🚚 4️⃣ THE COURIER (fetch_weather) ---
def fetch_weather(city: str, api_key: str, logger: logging.Logger) -> Dict:
    """Drives to Open Weather and gets huge Json box."""
    # 1️⃣ BUILD THE ADDRESS (Pure Logic - String manipulation in RAM)
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()

        else:
            logger.error(f"The request failed with status {response.status_code} for city: {city}")  # ✅ Fixed error message
            return {}

    except Exception as e:
        logger.error(f"Courier failed to reach API: {e}")
        return {}


# --- 🧹 3️⃣ PARSE COMMAND ---
def parse_command(raw: str) -> Dict[str, str]:
    """Cleans, splits and lowercases the string. Returns a dictionary."""
    words = raw.split()

    if not words:
        return {"action": "", "payload": ""}

    action = words[0].lower()

    # ✅ FIX 3: Changed > 0 to > 1, and added space in join
    if len(words) > 1:
        payload = " ".join(words[1:])  # ✅ Added space separator
    else:
        payload = ""

    return {"action": action, "payload": payload}


# --- 🔪 5️⃣ THE PREP COOK (NEW SPECIALIST) ---
def extract_temperature(data: Dict) -> Dict:
    """Digs through the raw JSON box to find the temp and city."""
    if not data:
        return {}

    try:
        temp = data["main"]["temp"]
        city = data["name"]

        return {"city": city, "temp": temp}

    except KeyError as e:
        return {}


# --- 8️⃣ UPDATE STATE (Formerly update_tasks) ---
def update_state(state: List[Dict], weather_data: Dict) -> List[Dict]:
    """Append the new temperature reading to the log."""
    if not weather_data:
        return state

    state.append(weather_data)

    return state


# --- 7️⃣ SAVE STATE (Formerly save_tasks) ---
# ✅ FIX 5: Swapped parameters to match the call in main()
def save_state(state: List[Dict], filepath: str, logger: logging.Logger) -> None:
    """Put the updated Weather Log back in the freezer."""
    try:
        # ✅ FIX 4: Added 'as f' to name the pipe
        with open(filepath, "w") as f:
            json.dump(state, f, indent=2)

            logger.info(f"State saved to {filepath}")
    except Exception as e:
        logger.error(f"Failed to save to {filepath}: {e}")


# --- 9️⃣ FORMAT STATE ---
def format_state(state: List[Dict]) -> str:
    """Formats the city and temperature log into human-readable string."""
    # ✅ FIX 7: Matched the test expectation
    if not state:
        return "No weather data yet. Try 'weather <city>' to add some!"

    display = ""
    for entry in state:
        # ✅ FIX 6: Removed space from key
        city = entry["city"]
        temp = entry["temp"]
        display += f"🌍 {city}: {temp}°C\n"

    return display


# --- 🔟 10️⃣ THE PRE-FLIGHT CHECKLIST (run_tests) ---
def run_tests() -> None:
    """Verify pure logic contracts before ignition."""

    print("\n🧪 RUNNING PRE-FLIGHT TESTS...")

    # TEST 1: parse_command()
    result = parse_command("weather london")
    expected = {"action": "weather", "payload": "london"}
    if result == expected:
        print("✅ PASS: parse_command('weather london')")
    else:
        print(f"❌ FAIL: parse_command('weather london') returned {result}, expected {expected}")
        sys.exit(1)

    # TEST 2: parse_command() with empty input
    result = parse_command("")
    expected = {"action": "", "payload": ""}
    if result == expected:
        print("✅ PASS: parse_command('')")
    else:
        print(f"❌ FAIL: parse_command('') returned {result}, expected {expected}")
        sys.exit(1)

    # TEST 3: extract_temperature() with valid data
    result = extract_temperature({"main": {"temp": 15.2}, "name": "London"})
    expected = {"city": "London", "temp": 15.2}
    if result == expected:
        print("✅ PASS: extract_temperature(valid data)")
    else:
        print(f"❌ FAIL: extract_temperature(valid data) returned {result}, expected {expected}")
        sys.exit(1)

    # TEST 4: extract_temperature() with empty data
    result = extract_temperature({})
    expected = {}
    if result == expected:
        print("✅ PASS: extract_temperature({})")
    else:
        print(f"❌ FAIL: extract_temperature({{}}) returned {result}, expected {expected}")
        sys.exit(1)

    # TEST 5: update_state() with new entry
    result = update_state([], {"city": "London", "temp": 15.2})
    expected = [{"city": "London", "temp": 15.2}]
    if result == expected:
        print("✅ PASS: update_state([], new_entry)")
    else:
        print(f"❌ FAIL: update_state([], new_entry) returned {result}, expected {expected}")
        sys.exit(1)

    # TEST 6: update_state() with empty entry
    result = update_state([{"city": "Paris", "temp": 20}], {})
    expected = [{"city": "Paris", "temp": 20}]
    if result == expected:
        print("✅ PASS: update_state(state, {})")
    else:
        print(f"❌ FAIL: update_state(state, {{}}) returned {result}, expected {expected}")
        sys.exit(1)

    # TEST 7: format_state() with entries
    result = format_state([{"city": "London", "temp": 15.2}])
    expected = "🌍 London: 15.2°C\n"
    if result == expected:
        print("✅ PASS: format_state([entry])")
    else:
        print(f"❌ FAIL: format_state([entry]) returned {repr(result)}, expected {repr(expected)}")
        sys.exit(1)

    # TEST 8: format_state() with empty list
    result = format_state([])
    expected = "No weather data yet. Try 'weather <city>' to add some!"
    if result == expected:
        print("✅ PASS: format_state([])")
    else:
        print(f"❌ FAIL: format_state([]) returned {result}, expected {expected}")
        sys.exit(1)

    print("✅ ALL TESTS PASSED. IGNITION SEQUENCE STARTING...\n")


# --- 🎯 11️⃣ THE GRAND ORCHESTRATOR (main) ---
def main() -> None:
    """The General Manager. Wires all stations together."""

    # ============================================
    # PHASE 1: PRE-SHIFT SETUP (Happens ONCE)
    # ============================================

    # 1️⃣ Build the security cameras (I/O - Terminal)
    logger = setup_logger()

    # 2️⃣ Read the Chalkboard + Manual (I/O - Disk)
    config = load_config(logger)

    # 3️⃣ Read the Owner's Sticky Note (Pure Logic - RAM)
    cli_overrides = parse_cli_args()

    # 4️⃣ Apply the Override Hierarchy (Pure Logic - RAM)
    # CLI > Config > Defaults
    filepath = cli_overrides.get("filepath", config["filepath"])
    api_key = config["api_key"]

    # 5️⃣ Pull the Master Logbook from the Warehouse (I/O - Disk)
    state = load_state(filepath, logger)

    # 6️⃣ Run the pre-flight tests (Hybrid - Pure Logic + I/O)
    run_tests()

    print("\n🏭 FACTORY ONLINE. TYPE 'weather <city>', 'show', 'clear', OR 'quit'.\n")

    # ============================================
    # PHASE 2: THE CONVEYOR BELT (Happens REPEATEDLY)
    # ============================================

    while True:
        # 1️⃣ Listen to the Customer (I/O - Keyboard)
        user_input = input("Command: ")

        # 2️⃣ Parse the order (Pure Logic - RAM)
        cmd = parse_command(user_input)

        # 3️⃣ Check for QUIT (Control Flow)
        if cmd["action"] == "quit":
            print("👋 Goodbye!")
            break  # 💀 KILLS THE LOOP

        # 4️⃣ Check for CLEAR (Control Flow)
        if cmd["action"] == "clear":
            state = []  # Reset the logbook in RAM
            save_state(state, filepath, logger)  # Write empty list to disk
            print("🗑️ Logbook cleared!")
            continue  # ⏭️ Skip to next iteration

        # 5️⃣ Check for WEATHER (The main workflow)
        if cmd["action"] == "weather":
            city = cmd["payload"]

            # Validate the payload
            if not city:
                print("❌ Please specify a city: weather <city>")
                continue  # ⏭️ Skip to next iteration

            # Fetch the raw box (I/O - Internet)
            raw_box = fetch_weather(city, api_key, logger)

            # Extract the clean sticky note (Pure Logic - RAM)
            reading = extract_temperature(raw_box)

            # Check if the extraction failed
            if not reading:
                print(f"❌ City '{city}' not found or API error.")
                continue  # ⏭️ Skip to next iteration

            # Append to the logbook (Pure Logic - RAM)
            state = update_state(state, reading)

            # Save to disk (I/O - Disk)
            save_state(state, filepath, logger)

            # Print the result (I/O - Terminal)
            print(f"✅ Added: {reading['city']} - {reading['temp']}°C")
            continue  # ⏭️ Skip to next iteration

        # 6️⃣ Check for SHOW (Display the logbook)
        if cmd["action"] == "show":
            display = format_state(state)  # Pure Logic - RAM
            print(f"\n{display}")  # I/O - Terminal
            continue  # ⏭️ Skip to next iteration

        # 7️⃣ Unknown command
        print(f"❌ Unknown command: '{cmd['action']}'. Try 'weather', 'show', 'clear', or 'quit'.")


# --- 🔟 ROOT ---
# ✅ FIX 8: Removed duplicate run_tests() call
if __name__ == "__main__":
    main()