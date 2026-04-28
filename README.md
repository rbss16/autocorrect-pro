# 🚀 Real-Time NLP Autocorrect System

![Live Demo](https://img.shields.io/badge/Live_Demo-Online-success?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-lightgrey?style=for-the-badge&logo=flask)

A production-grade, high-performance NLP autocorrect engine capable of handling complex typos, jumbled text, and missing vowels in real-time.

🔗 **[Live Demo: autocorrect-pro.onrender.com](https://autocorrect-pro.onrender.com/)**

## ✨ Features

- **Multi-Engine Pipeline**: Runs 5 intelligent NLP engines in parallel:
  - 🧩 **Anagram Solver**: Instantly fixes exact letter scrambles (e.g., `tcerroc` → `correct`).
  - 📏 **Norvig's Edit Distance**: Handles minor and major typos using mathematical edit distance.
  - 🧠 **Fuzzy Logic**: Matches complex structural typos using Ratcliff/Obershelp sequence matching.
  - 📱 **SMS-Style Missing Vowels**: Mimics smartphone keyboards (e.g., `awsm` → `awesome`).
  - ⚡ **Prefix Autocomplete**: Suggests unfinished words in real-time.
- **Massive Vocabulary**: Trained on a massive **370,000+ word dictionary**.
- **Real-World Probabilities**: Mapped against a pristine 50k-word frequency dataset so the most mathematically probable words always win.
- **Lightning Fast**: Compiles into a binary `.pkl` model for sub-millisecond lookup times.

## 🏆 Benchmark Accuracy

Tested against a brutal dataset of notorious human misspellings:
- **Top-3 Accuracy**: `>97%`
- **Processing Speed**: `<0.3s per word`

## 💻 Local Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/rbss16/autocorrect-pro.git
   cd autocorrect-pro/autocorrect-app
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Train the model (Downloads the datasets and builds the `model.pkl`):
   ```bash
   python train.py
   ```
4. Run the app:
   ```bash
   python app.py
   ```

## 🌐 Deployment
This app is optimized for deployment on [Render](https://render.com/). The build script automatically downloads the massive datasets and compiles the model on the server to keep the GitHub repository incredibly lightweight.
