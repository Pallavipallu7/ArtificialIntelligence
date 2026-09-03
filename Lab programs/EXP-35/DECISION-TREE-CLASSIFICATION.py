# Experiment 35: Decision Tree Algorithm for Simple Classification

import numpy as np
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.datasets import load_iris

# Load sample dataset
iris = load_iris()
X, y = iris.data, iris.target

# Decision Tree Classifier with Gini Impurity
dt_clf = DecisionTreeClassifier(criterion='gini', max_depth=3, random_state=42)
dt_clf.fit(X, y)

tree_rules = export_text(dt_clf, feature_names=iris.feature_names)

print("=== DECISION TREE CLASSIFICATION ===")
print("Generated Decision Tree Rules:")
print(tree_rules)
print("Feature Importances:")
for name, imp in zip(iris.feature_names, dt_clf.feature_importances_):
    print(f"  {name}: {imp:.4f}")

sample = np.array([[5.1, 3.5, 1.4, 0.2], [6.5, 3.0, 5.2, 2.0]])
preds = dt_clf.predict(sample)
print("\nSample Predictions:")
for i, p in enumerate(preds):
    print(f"  Sample {i+1} -> Predicted Class: {iris.target_names[p]}")
