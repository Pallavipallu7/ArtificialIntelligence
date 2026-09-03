# Experiment 39: Principal Component Analysis (PCA) for Dimensionality Reduction

import numpy as np
from sklearn.decomposition import PCA
from sklearn.datasets import load_iris

# Load High-Dimensional Dataset (4 Features)
iris = load_iris()
X = iris.data

# Apply PCA to reduce dimensions from 4 to 2
pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X)

exp_var = pca.explained_variance_ratio_

print("=== PRINCIPAL COMPONENT ANALYSIS (PCA) ===")
print(f"Original Feature Dimension: {X.shape[1]} (Sepal/Petal Length & Width)")
print(f"Reduced Feature Dimension: {X_reduced.shape[1]} (PC1, PC2)")
print(f"Explained Variance Ratio per Component: {exp_var}")
print(f"Total Retained Variance: {np.sum(exp_var) * 100:.2f}%")

print("\nFirst 5 Samples (Original vs Reduced):")
for i in range(5):
    print(f"  Sample {i+1}: {X[i]} -> PC Coordinates: [{X_reduced[i][0]:.4f}, {X_reduced[i][1]:.4f}]")
