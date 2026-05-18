def find_significant_drops():
    print("🌦 Temperature Drop Analyzer")

    raw = input("Enter temperatures (comma-separated): ").strip()
    if not raw:
        print("❌ No data provided.")
        return

    try:
        temps = [float(item.strip()) for item in raw.split(",")]
    except ValueError:
        print("❌ Invalid number format.")
        return

    if len(temps) < 2:
        print("📊 Need at least 2 days to compare.")
        return

    try:
        threshold = float(input("Enter drop threshold: ").strip())
    except ValueError:
        print("❌ Invalid threshold format.")
        return

    temp_drop = False
    for i in range(len(temps) - 1):
        current_day = temps[i]
        next_day = temps[i + 1]
        drop = current_day - next_day

        if drop >= threshold:
            print(f"📉 Day {i+1}→{i+2}: {current_day} → {next_day} (Drop: {drop:.1f}°)")
            temp_drop = True

    if not temp_drop:
        print("✅ No drops met the threshold.")


def main():
    while True:
        find_significant_drops()
        again = input("Run analyzer again? (yes/no): ").strip().lower()
        if again != "yes":
            print("👋 Analyzer closing out!")
            break


if __name__ == "__main__":
    main()