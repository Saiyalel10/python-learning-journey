from typing import List, Dict, Tuple

def parse_input(raw: str) -> List[str]:
    """Clean raw text: lowercase, split, strip punctuation edges."""
    return [word.strip(".,!?;:\"'()") for word in raw.lower().split()]

def count_frequencies(words: List[str]) -> Dict[str, int]:
    """Count word occurrences. Skips empty strings from punctuation-only inputs."""
    freq: Dict[str, int] = {}
    for word in words:
        if not word:  # Defensive guard: ignore "", " ", etc.
            continue
        freq[word] = freq.get(word, 0) + 1
    return freq

def format_report(freq: Dict[str, int]) -> str:
    """Sort by frequency (descending) and return a formatted string."""
    if not freq:
        return "✅ No valid words found."

    # items() → [('the', 3), ('cat', 1), ...]
    sorted_items: List[Tuple[str, int]] = sorted(freq.items(), key=lambda x: x[1], reverse=True)

    lines = ["📈 Word Frequencies:"]
    for word, count in sorted_items:
        lines.append(f"  {word} ➡ {count}")
    return "\n".join(lines)

def run_tests() -> None:
    """Automated verification. Runs before any manual input."""
    assert count_frequencies(parse_input("The cat sat on the the!")) == {"the": 3, "cat": 1, "sat": 1, "on": 1}
    assert count_frequencies(parse_input(".,!? ...")) == {}
    assert count_frequencies(parse_input("   ")) == {}
    print("✅ All automated tests passed.")

def main() -> None:
    """CLI entry point. Orchestrates the pipeline."""
    raw = input("Enter text: ").strip()
    if not raw:
        print("❌ Raw text cannot be empty!")
        return

    # Data flows forward. No function touches input/print except this one.
    words = parse_input(raw)
    freq = count_frequencies(words)
    print(format_report(freq))

if __name__ == "__main__":
    run_tests()  # 🔍 Taste test before service
    main()       # 🍽️ Serve to user