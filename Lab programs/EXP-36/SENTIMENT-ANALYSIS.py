# Experiment 36: Sentiment Analysis using NLP Techniques

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Training text corpus
reviews = [
    "This product is amazing and works perfectly!",
    "Great quality, fast shipping, highly recommended.",
    "Decent item for the price, satisfied with purchase.",
    "Terrible product, broke after one day of use.",
    "Awful customer service and bad experience overall.",
    "Horrible quality, completely useless product."
]
# Labels: 1 = Positive, 0 = Negative
labels = [1, 1, 1, 0, 0, 0]

# TF-IDF Feature Extraction
vectorizer = TfidfVectorizer(stop_words='english')
X_train = vectorizer.fit_transform(reviews)

# Naive Bayes Classifier
clf = MultinomialNB()
clf.fit(X_train, labels)

# Test Sentences
test_reviews = [
    "The item is wonderful and shipping was fast!",
    "Worst quality ever, totally disappointed.",
    "Very satisfied with the product performance."
]

X_test = vectorizer.transform(test_reviews)
predictions = clf.predict(X_test)
probs = clf.predict_proba(X_test)

print("=== NLP SENTIMENT ANALYSIS ===")
for text, pred, prob in zip(test_reviews, predictions, probs):
    sentiment = "POSITIVE" if pred == 1 else "NEGATIVE"
    confidence = max(prob) * 100
    print(f"Input Text: \"{text}\"")
    print(f"  -> Predicted Sentiment: {sentiment} (Confidence: {confidence:.2f}%)\n")
