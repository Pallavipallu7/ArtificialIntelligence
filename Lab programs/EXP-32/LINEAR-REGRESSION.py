# Experiment 32: Implement Linear Regression for Continuous Variable Prediction

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Dataset: House Size (in sq ft) -> House Price (in $1000s)
X = np.array([[850], [1100], [1400], [1700], [2000], [2300], [2600], [3000]])
y = np.array([210, 260, 310, 370, 420, 480, 530, 610])

# Initialize and train Linear Regression Model
model = LinearRegression()
model.fit(X, y)

# Predictions
y_pred = model.predict(X)

# Model parameters and evaluation metrics
slope = model.coef_[0]
intercept = model.intercept_
mse = mean_squared_error(y, y_pred)
r2 = r2_score(y, y_pred)

print("=== LINEAR REGRESSION ALGORITHM ===")
print(f"Learned Equation: Price = {slope:.4f} * Size + {intercept:.4f}")
print(f"Mean Squared Error (MSE): {mse:.4f}")
print(f"R-squared Score (R2): {r2:.4f}")
print("\n--- Sample Predictions ---")

sample_sizes = np.array([[1200], [1800], [2500]])
sample_preds = model.predict(sample_sizes)

for size, pred in zip(sample_sizes, sample_preds):
    print(f"House Size: {size[0]} sq ft -> Predicted Price: ${pred * 1000:,.2f}")
