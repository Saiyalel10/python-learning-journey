def find_first_duplicate():
    print("🔄Duplicate Word Finder!")

    raw_text = input("Enter Text: ").strip().lower()
    if not raw_text:
        print("❌No text entered!")
        return

    word_list = raw_text.split()
    seen = set()
    dup_found = False

    for word in word_list:
        if word in seen:
            print(f"✔Duplicate Word Found: {word}")
            dup_found = True
            break
        else:
            seen.add(word)

    if dup_found is False:
        print("✔No Duplicates Found!")

def main():
    while True:
        find_first_duplicate()
        again= input("Run the Duplicate Word Finder again?(yes/no): ").strip().lower()
        if again!="yes":
            print("👋Goodbye!")
            break

if __name__ == "__main__":
    main()


