import os
import re
import difflib
import pickle
import sys
from collections import Counter

def words(text): 
    return re.findall(r'\w+', text.lower())

# Load the pre-trained NLP model
model_path = 'model.pkl'
if not os.path.exists(model_path):
    print("ERROR: Model not found. Please run 'python train.py' first to train the model.", file=sys.stderr)
    sys.exit(1)

with open(model_path, 'rb') as f:
    model_data = pickle.load(f)

VALID_WORDS = model_data['VALID_WORDS']
TOP_WORDS = model_data['TOP_WORDS']
N = model_data['N']

def P(word): 
    "Probability of `word`."
    return VALID_WORDS.get(word, 0) / N if N > 0 else 0

def get_corrections(word, top_n=3):
    "Get top N corrections for word using a multi-engine approach."
    original_word = word
    word = word.lower()
    
    if not word.isalpha():
        return [original_word]
    
    cands = []
    seen = set()
    
    def add_cands(source_list):
        for w in source_list:
            if w not in seen and w != word: # Don't suggest the typo itself
                cands.append(w)
                seen.add(w)

    if word in VALID_WORDS:
        # If the word is fully correct, suggest it first
        cands.append(word)
        seen.add(word)
        # But also provide autocomplete if they are mid-sentence (e.g. "int" -> "into", "interesting")
        if len(word) >= 2:
            autocomplete = [w for w in TOP_WORDS if w.startswith(word) and w != word]
            add_cands(sorted(autocomplete, key=P, reverse=True)[:2])
    else:
        # 1. Anagram Solver (Exact letter matches)
        sorted_word = "".join(sorted(word))
        anagrams = [w for w in TOP_WORDS if len(w) == len(word) and "".join(sorted(w)) == sorted_word]
        
        # 2. Norvig Edit Distance 1 & 2 (Sorted by frequency)
        e1 = sorted(list(known(edits1(word))), key=P, reverse=True)
        e2 = sorted(list(known(edits2(word))), key=P, reverse=True)
        
        # 3. Fuzzy Matching (Handles missing vowels and messy typos)
        fuzzy = difflib.get_close_matches(word, TOP_WORDS, n=8, cutoff=0.45)
        
        # 4. Autocomplete (Prefix matching)
        autocomplete = sorted([w for w in TOP_WORDS if w.startswith(word)], key=P, reverse=True)
        
        # 5. SMS-style Missing Vowels Matcher
        vowels_stripped = re.sub(r'[aeiouy]', '', word)
        sms_matches = []
        if len(vowels_stripped) >= 2:
            # Must share the same starting letter to ensure relevance
            sms_matches = [w for w in TOP_WORDS if w.startswith(word[0]) and re.sub(r'[aeiouy]', '', w) == vowels_stripped]
            sms_matches = sorted(sms_matches, key=P, reverse=True)
        
        # --- SMART MERGING ALGORITHM ---
        add_cands(sms_matches[:2])   # 1. SMS-style abbreviation (e.g. 'awsm' -> 'awesome')
        add_cands(anagrams[:2])      # 2. Exact letter scrambles (e.g. 'tcerroc' -> 'correct')
        add_cands(e1[:3])            # 3. Minor 1-character typos 
        add_cands(fuzzy[:3])         # 4. General fuzzy matching (Highest human-intuition accuracy)
        add_cands(autocomplete[:3])  # 5. Unfinished words
        add_cands(e2[:2])            # 6. 2-character typos (Noisiest)

    # Format candidates based on original casing
    result = []
    for cand in cands[:top_n]:
        if original_word.istitle():
            result.append(cand.title())
        elif original_word.isupper():
            result.append(cand.upper())
        else:
            result.append(cand)
            
    return result

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in VALID_WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))
