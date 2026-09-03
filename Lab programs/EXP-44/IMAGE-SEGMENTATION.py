# Experiment 44: Image Segmentation using Computer Vision Techniques

import numpy as np
from sklearn.cluster import KMeans

# Simulate a 10x10 RGB Image with 2 regions (Background & Foreground object)
np.random.seed(42)
img_pixels = np.zeros((100, 3), dtype=np.uint8)
img_pixels[:50] = [30, 30, 30]    # Dark Background
img_pixels[50:] = [220, 50, 50]   # Red Foreground Object

# Segment Image using K-Means Clustering on Pixel RGB values
k = 2
kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
segment_labels = kmeans.fit_predict(img_pixels)

centroids = kmeans.cluster_centers_

print("=== COMPUTER VISION IMAGE SEGMENTATION ===")
print(f"Input Image Resolution: 10x10 (100 total pixels)")
print(f"Segment Clusters (K={k}):")
for i, center in enumerate(centroids):
    print(f"  Segment {i}: RGB Centroid = [{center[0]:.1f}, {center[1]:.1f}, {center[2]:.1f}]")

bg_count = np.sum(segment_labels == 0)
fg_count = np.sum(segment_labels == 1)

print(f"\nSegment Pixel Breakdown:")
print(f"  Segment 0 Pixel Count: {bg_count} pixels ({bg_count}% of image)")
print(f"  Segment 1 Pixel Count: {fg_count} pixels ({fg_count}% of image)")
