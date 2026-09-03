# Experiment 49: Face Recognition using Pre-trained Model

import numpy as np

# Database of known user face embedding vectors (128-D representation simulated)
known_faces = {
    "Alice": np.array([0.15, 0.82, 0.33, 0.45]),
    "Bob":   np.array([0.77, 0.12, 0.91, 0.24]),
    "Charlie": np.array([0.05, 0.41, 0.88, 0.62])
}

# Simulated test face detected in image
test_face = np.array([0.16, 0.80, 0.35, 0.44])

# Compute Euclidean Distance to match identity
threshold = 0.3
best_match = "Unknown"
min_dist = float("inf")

print("=== FACE RECOGNITION USING PRE-TRAINED EMBEDDINGS ===")
print("Comparing Test Face Embedding against Database...")

for name, embedding in known_faces.items():
    dist = np.linalg.norm(test_face - embedding)
    print(f"  Distance to {name}: {dist:.4f}")
    if dist < min_dist and dist < threshold:
        min_dist = dist
        best_match = name

print("-" * 55)
print(f"RECOGNIZED IDENTITY: {best_match} (Match Confidence Distance: {min_dist:.4f})")
