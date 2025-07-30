from collections import Counter
import re

def analyze_repeats(translated_titles):
    all_words = " ".join(translated_titles).lower()
    words = re.findall(r'\b\w+\b', all_words)
    counter = Counter(words)

    print("\n🔁 Repeated Words (more than 2 times):")
    for word, count in counter.items():
        if count > 2:
            print(f"{word}: {count}")
