# Experiment 38: Support Vector Machine (SVM) for Binary Classification

import numpy as np
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix

# Binary Feature Dataset
X = np.array([
    [1.5, 2.0], [2.0, 3.0], [1.8, 1.5], [2.5, 2.8],  # Class 0
    [6.0, 7.0], [7.5, 8.0], [6.8, 6.5], [8.0, 7.2]   # Class 1
])
y = np.array([0, 0, 0, 0, 1, 1, 1, 1])

# Initialize Support Vector Classifier with Linear Kernel
svm_model = SVC(kernel='linear', C=1.0)
svm_model.fit(X, y)

# Predictions
X_test = np.array([[2.1, 2.2], [6.5, 7.1], [1.0, 1.2], [7.8, 8.2]])
y_test = np.array([0, 1, 0, 1])
y_pred = svm_model.predict(X_test)

print("=== SUPPORT VECTOR MACHINE (SVM) BINARY CLASSIFICATION ===")
print("Kernel Type: Linear | Regularization Parameter (C): 1.0")
print(f"Number of Support Vectors: {len(svm_model.support_vectors_)}")
print("Support Vectors Matrix:")
print(svm_model.support_vectors_)

print("\nTest Set Predictions:")
for i, pt in enumerate(X_test):
    print(f"  Point {pt} -> Predicted Class: {y_pred[i]} (True Label: {y_test[i]})")

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))
