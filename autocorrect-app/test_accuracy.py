import time
from autocorrect import get_corrections

# A professional-grade benchmark dataset of common human misspellings
test_data = {
    'access': ['acess', 'acces'],
    'accommodation': ['accomodation', 'acommodation'],
    'address': ['adres', 'addres'],
    'because': ['becuase', 'becasue', 'bcause'],
    'believe': ['beleive', 'belive'],
    'definitely': ['definitly', 'definately'],
    'environment': ['enviroment'],
    'necessary': ['necesary', 'neccessary'],
    'receive': ['recieve'],
    'separate': ['seperate', 'separet'],
    'until': ['untill'],
    'which': ['wich'],
    'spelling': ['speling', 'spelng'],
    'correct': ['corect', 'tcerroc', 'crrect'],
    'awesome': ['awsm', 'awsome', 'aweosme'],
    'random': ['rndm', 'ranom'],
    'algorithm': ['algoritm', 'algorthm'],
    'intelligence': ['inteligence', 'intellegence'],
    'processing': ['procesing', 'processng'],
    'language': ['langage', 'languge']
}

def test_model():
    print("Running NLP Benchmark. Evaluating Model Accuracy...")
    total_tests = 0
    top1_correct = 0
    top3_correct = 0
    
    start_time = time.time()
    
    for correct_word, misspellings in test_data.items():
        for typo in misspellings:
            total_tests += 1
            # Ask the engine for the top 3 suggestions
            suggestions = get_corrections(typo, top_n=3)
            
            # Convert to lowercase to check accuracy
            suggestions = [s.lower() for s in suggestions]
            
            if suggestions and suggestions[0] == correct_word:
                top1_correct += 1
                top3_correct += 1
                print(f"[+] PERFECT MATCH: '{typo}' -> {suggestions[0]}")
            elif correct_word in suggestions:
                top3_correct += 1
                print(f"[~] IN TOP 3: '{typo}' -> {suggestions} (Expected: '{correct_word}')")
            else:
                print(f"[-] FAILED: '{typo}' -> AI Suggested: {suggestions} (Expected: '{correct_word}')")

    end_time = time.time()
    
    print("\n" + "="*30)
    print("🏆 FINAL ACCURACY RESULTS 🏆")
    print("="*30)
    print(f"Total Words Tested : {total_tests}")
    print(f"Top-1 Accuracy     : {(top1_correct / total_tests) * 100:.1f}% (Correct word was the #1 choice)")
    print(f"Top-3 Accuracy     : {(top3_correct / total_tests) * 100:.1f}% (Correct word was in the drop-down)")
    print(f"Processing Speed   : {(end_time - start_time) / total_tests:.4f} seconds per word")
    print("="*30)

if __name__ == '__main__':
    test_model()
