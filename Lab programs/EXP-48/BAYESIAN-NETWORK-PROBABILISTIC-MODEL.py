# Experiment 48: Bayesian Network for Probabilistic Relationship Modeling

import numpy as np

# Bayesian Network Modeling Medical Diagnosis: Flu -> Fever & Cough
# Prior P(Flu = True)
P_Flu = 0.1

# Conditional Probability Tables (CPTs)
# P(Fever = True | Flu)
P_Fever_given_Flu = {True: 0.8, False: 0.1}

# P(Cough = True | Flu)
P_Cough_given_Flu = {True: 0.9, False: 0.2}

# Compute Posterior P(Flu = True | Fever = True, Cough = True) using Bayes Rule
P_Fever_Cough_given_Flu = P_Fever_given_Flu[True] * P_Cough_given_Flu[True]
P_Fever_Cough_given_noFlu = P_Fever_given_Flu[False] * P_Cough_given_Flu[False]

P_Evidence = (P_Fever_Cough_given_Flu * P_Flu) + (P_Fever_Cough_given_noFlu * (1 - P_Flu))
P_Posterior_Flu = (P_Fever_Cough_given_Flu * P_Flu) / P_Evidence

print("=== BAYESIAN NETWORK PROBABILISTIC MODEL ===")
print(f"Prior Probability P(Flu=True): {P_Flu:.2f}")
print("Conditional Probability Tables (CPTs):")
print("  P(Fever=True | Flu=True) = 0.80  |  P(Fever=True | Flu=False) = 0.10")
print("  P(Cough=True | Flu=True) = 0.90  |  P(Cough=True | Flu=False) = 0.20")

print(f"\nBayesian Probabilistic Inference Query:")
print(f"  P(Flu=True | Fever=True, Cough=True) = {P_Posterior_Flu * 100:.2f}%")
