# Experiment 42: K-Means Clustering Algorithm

import numpy as np
from sklearn.cluster import KMeans

# 2D Data points
X = np.array([
    [1, 2], [1.5, 1.8], [5, 8], [8, 8],
    [1, 0.6], [9, 11], [8, 2], [10, 2], [9, 3]
])

# Initialize K-Means with 3 clusters
k = 3
kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
kmeans.fit(X)

labels = kmeans.labels_
centroids = kmeans.cluster_centers_

print(f"=== K-MEANS CLUSTERING ALGORITHM (K={k}) ===")
print("Learned Cluster Centroids:")
for i, center in enumerate(centroids):
    print(f"  Cluster {i}: Center = [{center[0]:.2f}, {center[1]:.2f}]")

print("\nData Point Assignments:")
for i, pt in enumerate(X):
    print(f"  Point {pt} -> Assigned to Cluster {labels[i]}")

print(f"\nInertia (Within-Cluster Sum of Squares): {kmeans.inertia_:.4f}")
