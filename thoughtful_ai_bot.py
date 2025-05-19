import streamlit as st
import json
import re
import os
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from difflib import get_close_matches

# Try loading qa.json from current directory
qa_json = None
qa_file = "qa.json"
if os.path.exists(qa_file):
    try:
        with open(qa_file, "r", encoding="utf-8") as f:
            qa_json = json.load(f)
    except Exception as e:
        print(f"Failed to load {qa_file}, using fallback. Error: {e}")

# Fallback QA data
if not qa_json:
    qa_json = {
        "questions": [
            {
                "question": "What does the eligibility verification agent (EVA) do?",
                "answer": "EVA automates the process of verifying a patient's eligibility and benefits information in real-time, eliminating manual data entry errors and reducing claim rejections."
            },
            {
                "question": "What does the claims processing agent (CAM) do?",
                "answer": "CAM streamlines the submission and management of claims, improving accuracy, reducing manual intervention, and accelerating reimbursements."
            },
            {
                "question": "How does the payment posting agent (PHIL) work?",
                "answer": "PHIL automates the posting of payments to patient accounts, ensuring fast, accurate reconciliation of payments and reducing administrative burden."
            },
            {
                "question": "Tell me about Thoughtful AI's Agents.",
                "answer": "Thoughtful AI provides a suite of AI-powered automation agents designed to streamline healthcare processes. These include Eligibility Verification (EVA), Claims Processing (CAM), and Payment Posting (PHIL), among others."
            },
            {
                "question": "What are the benefits of using Thoughtful AI's agents?",
                "answer": "Using Thoughtful AI's Agents can significantly reduce administrative costs, improve operational efficiency, and reduce errors in critical processes like claims management and payment posting."
            }
        ]
    }

# Build a dictionary from the JSON
qa_pairs = {q["question"].lower(): q["answer"] for q in qa_json["questions"]}

# Fallback response
fallback = "I'm not sure about that. Please refer to the Thoughtful AI documentation or website for more information."

# Function to normalize user input using sklearn's stop words
stop_words = ENGLISH_STOP_WORDS

def normalize_input(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)  # remove punctuation
    words = text.split()
    filtered_words = [word for word in words if word not in stop_words]
    return ' '.join(filtered_words)

# Dynamically extract abbreviation mappings from questions
def extract_abbreviations(qa_json):
    abbr_map = {}
    pattern = re.compile(r"(.*?)\((\w+)\)")
    for q in qa_json["questions"]:
        match = pattern.search(q["question"])
        if match:
            full_form = match.group(1).strip()
            abbr = match.group(2).lower().strip()
            abbr_map[abbr] = full_form
    return abbr_map

abbreviation_map = extract_abbreviations(qa_json)

def expand_abbreviations(text):
    words = text.lower().split()
    expanded = [abbreviation_map.get(word, word) for word in words]
    return ' '.join(expanded)

# Normalize QA keys for improved matching
normalized_qa = {normalize_input(k): v for k, v in qa_pairs.items()}

def get_response(user_input):
    cleaned = normalize_input(user_input)
    expanded_input = expand_abbreviations(cleaned)
    match = get_close_matches(expanded_input, normalized_qa.keys(), n=1, cutoff=0.6)
    return normalized_qa[match[0]] if match else fallback


# Streamlit UI
st.title("Thoughtful AI Assistant")
st.write("Ask about EVA, CAM, PHIL, or Thoughtful AI's automation solutions.")

user_input = st.text_input("Enter your question below:")

if user_input:
    response = get_response(user_input)
    st.markdown(f"**Response:** {response}")
