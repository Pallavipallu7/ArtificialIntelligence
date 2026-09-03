# Experiment 34: Neural Network for Image Classification

import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load digit dataset (8x8 pixel images)
digits = load_digits()
X, y = digits.data, digits.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Deep Multi-Layer Perceptron Neural Network Architecture
mlp = MLPClassifier(
    hidden_layer_sizes=(64, 32),
    activation='relu',
    solver='adam',
    max_iter=300,
    random_state=42
)

mlp.fit(X_train, y_train)
y_pred = mlp.predict(X_test)
acc = accuracy_score(y_test, y_pred)

print("=== DEEP LEARNING NEURAL NETWORK FOR IMAGE CLASSIFICATION ===")
print(f"Input Features (Pixels): {X.shape[1]} (8x8 image resolution)")
print(f"Target Classes: {len(np.unique(y))} (Digits 0-9)")
print("Network Architecture: Input(64) -> Hidden1(64, ReLU) -> Hidden2(32, ReLU) -> Output(10, Softmax)")
print(f"Training Epochs Completed: {mlp.n_iter_}")
print(f"Final Training Loss: {mlp.loss_:.6f}")
print(f"TEST DATASET ACCURACY: {acc * 100:.2f}%")
