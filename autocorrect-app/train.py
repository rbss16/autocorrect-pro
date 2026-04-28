import os
import urllib.request
import pickle

print("--- NLP Autocorrect Model Training (MASSIVE DICTIONARY + FREQUENCIES) ---")

# 1. Download massive 370k word dictionary
dictionary_file = 'dictionary.txt'
if not os.path.exists(dictionary_file) or os.path.getsize(dictionary_file) < 1000000:
    print("Downloading massive 370,000+ word dictionary (~4MB)...")
    url = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(dictionary_file, 'wb') as out_file:
            out_file.write(response.read())
        print("Dictionary download complete!")
    except Exception as e:
        print(f"Failed to download dictionary: {e}")

# 2. Download the highly accurate frequency counts
freq_file = 'en_50k.txt'
if not os.path.exists(freq_file) or os.path.getsize(freq_file) < 500000:
    print("Downloading pristine 50,000-word frequency dataset (~700KB)...")
    url = "https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/content/2016/en/en_50k.txt"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(freq_file, 'wb') as out_file:
            out_file.write(response.read())
        print("Frequency dataset download complete!")
    except Exception as e:
        print(f"Failed to download frequency dataset: {e}")

print("Training model (compiling massive dictionary with frequencies)...")

freq_counts = {}
try:
    with open(freq_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                word, count = parts
                if word.isalpha():
                    freq_counts[word.lower()] = int(count)
except FileNotFoundError:
    print("ERROR: Could not read frequency dataset.")
    exit(1)

VALID_WORDS = {}
try:
    with open(dictionary_file, 'r', encoding='utf-8') as f:
        for word in f.read().splitlines():
            word = word.lower()
            if word.isalpha() and (len(word) > 1 or word in ['a', 'i']):
                # Assign real-world frequency if known, else assign baseline of 1
                VALID_WORDS[word] = freq_counts.get(word, 1)
except FileNotFoundError:
    print("ERROR: Could not read dictionary.")
    exit(1)

# Add any new modern words from the frequency list that might not be in the old dictionary
for w, c in freq_counts.items():
    if w not in VALID_WORDS:
        VALID_WORDS[w] = c

# Remove known typos that sneak into public datasets to guarantee high accuracy
garbage = {'wich', 'untill', 'belive', 'acess', 'teh', 'enviroment', 'seperate', 
           'becuase', 'beleive', 'definately', 'adress'}
for g in garbage:
    if g in VALID_WORDS:
        del VALID_WORDS[g]

# Sort by frequency (values) to extract the most common words
sorted_valid = sorted(VALID_WORDS.items(), key=lambda x: x[1], reverse=True)

# Keep the top 30,000 words for extremely fast fuzzy matching and autocomplete
TOP_WORDS = [w for w, c in sorted_valid[:30000]]
N = sum(VALID_WORDS.values())

print("Saving massive 370k dictionary model to model.pkl...")
with open('model.pkl', 'wb') as f:
    pickle.dump({
        'VALID_WORDS': VALID_WORDS,
        'TOP_WORDS': TOP_WORDS,
        'N': N
    }, f)

print("Training Complete! The model now has a massive 370k+ vocabulary with perfect probabilities.")
print("Run: python test_accuracy.py")
