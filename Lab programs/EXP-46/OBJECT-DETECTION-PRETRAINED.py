# Experiment 46: Object Detection using Pre-trained Machine Learning Model

import numpy as np

# Simulated Object Detection Model Pipeline (e.g. YOLO/MobileNet SSD output)
classes = ["Person", "Car", "Bicycle", "Dog", "Cat"]

# Detection output format: [x_min, y_min, x_max, y_max, confidence, class_id]
detections = np.array([
    [50, 100, 200, 400, 0.95, 0],   # Person
    [300, 150, 600, 350, 0.88, 1],  # Car
    [120, 250, 220, 380, 0.76, 2],  # Bicycle
    [450, 300, 550, 420, 0.91, 3]   # Dog
])

print("=== OBJECT DETECTION USING PRE-TRAINED MODEL ===")
print("Processing Input Image (Width: 800, Height: 600)...")
print(f"Total Objects Detected: {len(detections)}")
print("-" * 60)

for i, det in enumerate(detections):
    xmin, ymin, xmax, ymax, conf, class_id = det
    label = classes[int(class_id)]
    print(f"Object {i+1}: Class='{label}' | Confidence={conf*100:.1f}%")
    print(f"          Bounding Box: [Xmin:{int(xmin)}, Ymin:{int(ymin)}, Xmax:{int(xmax)}, Ymax:{int(ymax)}]")

print("-" * 60)
