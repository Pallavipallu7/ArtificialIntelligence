# Experiment 41: Simple Chatbot using Natural Language Processing

import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Knowledge base intents & responses
knowledge_base = {
    "hello": "Hello! How can I help you with AI today?",
    "what is artificial intelligence": "Artificial Intelligence is the simulation of human intelligence in machines.",
    "what is machine learning": "Machine Learning is a subset of AI that allows systems to learn from data.",
    "who created you": "I am a simple NLP Chatbot built for Lab Experiment 41.",
    "bye": "Goodbye! Have a great day!"
}

queries = list(knowledge_base.keys())
vectorizer = TfidfVectorizer().fit(queries)

def get_response(user_input):
    user_vec = vectorizer.transform([user_input.lower()])
    query_vecs = vectorizer.transform(queries)
    similarities = cosine_similarity(user_vec, query_vecs)[0]
    
    best_match_idx = similarities.argmax()
    if similarities[best_match_idx] > 0.2:
        return knowledge_base[queries[best_match_idx]]
    return "I'm sorry, I don't understand that query."

print("=== NLP CHATBOT INTERACTIVE SESSION ===")
sample_user_inputs = [
    "Hi hello there",
    "Tell me what is machine learning",
    "Who created you?",
    "What is the weather today?",
    "Bye!"
]

for user_msg in sample_user_inputs:
    bot_reply = get_response(user_msg)
    print(f"User: {user_msg}")
    print(f"Chatbot: {bot_reply}\n")
