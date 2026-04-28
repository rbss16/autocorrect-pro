document.addEventListener("DOMContentLoaded", () => {
    const textarea = document.getElementById("text-input");
    const suggestionBox = document.getElementById("suggestion-box");
    let typingTimer;
    const doneTypingInterval = 300; // 300ms debounce delay
    
    // Listen for input event to handle real-time detection
    textarea.addEventListener("input", () => {
        clearTimeout(typingTimer);
        const text = textarea.value;
        const lastWord = extractLastWord(text);
        
        if (lastWord.length > 0) {
            typingTimer = setTimeout(() => {
                fetchSuggestions(lastWord);
            }, doneTypingInterval);
        } else {
            hideSuggestions();
        }
    });
    
    function extractLastWord(text) {
        // Extract the last alphabetical word that is currently being typed
        // Matches letters at the end of the input string
        const match = text.match(/([a-zA-Z]+)$/);
        return match ? match[1] : "";
    }
    
    async function fetchSuggestions(word) {
        try {
            const response = await fetch("/suggest", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ word: word })
            });
            
            if (response.ok) {
                const data = await response.json();
                
                // Show suggestions if we have any, and if the first suggestion isn't exactly the word itself
                if (data.suggestions && data.suggestions.length > 0) {
                    const isExactMatch = data.suggestions.length === 1 && data.suggestions[0].toLowerCase() === word.toLowerCase();
                    if (!isExactMatch) {
                        displaySuggestions(data.suggestions, word);
                    } else {
                        hideSuggestions();
                    }
                } else {
                    hideSuggestions();
                }
            }
        } catch (error) {
            console.error("Error fetching suggestions:", error);
            hideSuggestions();
        }
    }
    
    function displaySuggestions(suggestions, originalWord) {
        suggestionBox.innerHTML = ""; // Clear old suggestions
        
        suggestions.forEach(suggestion => {
            // Don't show the exact same word as a suggestion
            if (suggestion.toLowerCase() === originalWord.toLowerCase()) return;
            
            const btn = document.createElement("button");
            btn.className = "suggestion-btn";
            btn.textContent = suggestion;
            btn.onclick = () => replaceLastWord(suggestion);
            suggestionBox.appendChild(btn);
        });
        
        // Only show if we actually added buttons
        if (suggestionBox.children.length > 0) {
            suggestionBox.style.display = "flex";
        } else {
            hideSuggestions();
        }
    }
    
    function hideSuggestions() {
        suggestionBox.style.display = "none";
        suggestionBox.innerHTML = "";
    }
    
    function replaceLastWord(newWord) {
        const text = textarea.value;
        // Replace the last alphabetical word at the end of the string
        textarea.value = text.replace(/([a-zA-Z]+)$/, newWord);
        textarea.focus();
        hideSuggestions();
    }
});
