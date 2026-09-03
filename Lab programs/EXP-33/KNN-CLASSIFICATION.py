# Experiment 33: K-Nearest Neighbors Algorithm for Classification

import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report

# Feature dataset: [Age, Estimated Salary ($1k)]
X_train = np.array([
    [22, 20], [25, 28], [20, 22], [35, 60], 
    [40, 80], [45, 110], [52, 130], [58, 140]
])
# Target labels: 0 = Low Spending, 1 = High Spending
y_train = np.array([0, 0, 0, 0, 1, 1, 1, 1])

# Initialize KNN Classifier with K=3
k = 3
knn = KNeighborsClassifier(n_neighbors=k)
knn.fit(X_train, y_train)

# Test Data
X_test = np.array([[23, 25], [48, 120], [38, 75], [55, 135]])
y_test = np.array([0, 1, 1, 1])

y_pred = knn.predict(X_test)
acc = accuracy_score(y_test, y_pred)

print(f"=== K-NEAREST NEIGHBORS (KNN) CLASSIFICATION (K={k}) ===")
print("Training Data Samples:", len(X_train))
print("Test Predictions:")
for i, test_pt in enumerate(X_test):
    print(f"  Sample {i+1} [Age: {test_pt[0]}, Salary: ${test_pt[1]}k] -> Class: {y_pred[i]} (Actual: {y_test[i]})")

print(f"\nMODEL ACCURACY SCORE: {acc * 100:.2f}%")
