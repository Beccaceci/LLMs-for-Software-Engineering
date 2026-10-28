import os

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
from sklearn.metrics import auc


# Generate random dataset (100 vectors, each of 5 dimensions)
np.random.seed(42)  # For reproducibility
expected = np.random.uniform(0.0, 1.0, size=(100, 5))


# Perturbation factor
perturbation_factor = 0.4

# Actual vectors
actual = expected + np.random.uniform(-perturbation_factor, perturbation_factor, size=expected.shape)

# Print out the original and modified datasets for comparison
print("Expected (First 2 Vectors):")
print(expected[:2])
print("\nActual (First 2 Vectors):")
print(actual[:2])

# Comparisons can be made as usual through cosine similarity
cos_sim_matrix = cosine_similarity(actual, expected)

print("\nCosine Similarity Matrix:")
print(cos_sim_matrix)