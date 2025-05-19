# Thoughtful-AI-Technical-Screen
This project implements a simple AI-powered assistant that answers questions about Thoughtful AI’s healthcare automation agents. It uses a predefined set of Q&A pairs and performs fuzzy matching to return the most relevant answer.

## Requirements

- Python 3.7 or later
- Install dependencies with:

```bash
pip install streamlit scikit-learn
```

## How to Run (Streamlit)

To launch the web interface:
```bash
streamlit run thoughtful_ai_bot.py
```
This will open an interactive browser window where you can interacte with the assistant.

## About the Predefined Q&A Set

If a file named qa.json exists in the same directory, the assistant will automatically load it and use its content instead of the built-in Q&A list.
