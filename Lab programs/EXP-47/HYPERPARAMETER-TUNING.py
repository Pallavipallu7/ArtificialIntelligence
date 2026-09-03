# Experiment 47: Hyperparameter Tuning for Machine Learning Model

import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.datasets import load_iris

# Load Dataset
iris = load_iris()
X, y = iris.data, iris.target

# Define Hyperparameter Search Grid
param_grid = {
    'C': [0.1, 1, 10],
    'gamma': [0.01, 0.1, 1],
    'kernel': ['linear', 'rbf']
}

# Grid Search with 5-Fold Cross Validation
grid = GridSearchCV(SVC(), param_grid, cv=5, scoring='accuracy')
grid.fit(X, y)

print("=== MACHINE LEARNING HYPERPARAMETER TUNING (GridSearchCV) ===")
print("Evaluated Hyperparameter Grid:")
print("  C:", param_grid['C'])
print("  gamma:", param_grid['gamma'])
print("  kernel:", param_grid['kernel'])

print(f"\nTotal Grid Combinations Tested: {len(grid.cv_results_['params'])}")
print(f"BEST HYPERPARAMETERS FOUND: {grid.best_params_}")
print(f"BEST CROSS-VALIDATION ACCURACY SCORE: {grid.best_score_ * 100:.2f}%")
