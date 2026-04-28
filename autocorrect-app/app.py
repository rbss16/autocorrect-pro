from flask import Flask, render_template, request, jsonify
from autocorrect import get_corrections

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/suggest', methods=['POST'])
def suggest():
    data = request.get_json()
    if not data or 'word' not in data:
        return jsonify({'suggestions': []}), 400
    
    word = data['word']
    if not word.strip():
        return jsonify({'suggestions': []})
    
    suggestions = get_corrections(word)
    return jsonify({'suggestions': suggestions})

if __name__ == '__main__':
    app.run(debug=True)
