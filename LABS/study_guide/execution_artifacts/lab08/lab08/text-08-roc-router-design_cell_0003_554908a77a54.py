# The row/column pairing is known in this synthetic example: i == j is positive.
def compute_tpr_fpr(expected_data, actual_data, threshold=0.9):
    expected_data = np.asarray(expected_data, dtype=float)
    actual_data = np.asarray(actual_data, dtype=float)
    if (expected_data.ndim != 2 or actual_data.shape != expected_data.shape
            or len(expected_data) == 0):
        raise ValueError("Expected equally sized, nonempty 2-D arrays of aligned vectors")
    cos_sim_matrix = cosine_similarity(expected_data, actual_data)
    tp = fp = tn = fn = 0
    for i in range(len(expected_data)):
        for j in range(len(actual_data)):
            ground_truth = i == j
            predicted = cos_sim_matrix[i, j] >= threshold
            if ground_truth and predicted:
                tp += 1
            elif not ground_truth and predicted:
                fp += 1
            elif not ground_truth and not predicted:
                tn += 1
            else:
                fn += 1
    tpr = tp / (tp + fn) if tp + fn else 0.0
    fpr = fp / (fp + tn) if fp + tn else 0.0
    return tpr, fpr

# Expected comes first, actual second, consistently with the function signature.
tpr, fpr = compute_tpr_fpr(expected, actual, threshold=0.95)
print(f"True Positive Rate (TPR): {tpr}")
print(f"False Positive Rate (FPR): {fpr}")