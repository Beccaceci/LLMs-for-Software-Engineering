# 100 thresholds in [0, 1], plus endpoints that predict none/all as positive.
# Cosine scores may be negative, so a threshold of zero alone need not give FPR=1.
thresholds = np.r_[np.inf, np.linspace(1.0, 0.0, 100), -np.inf]
tprs = []
fprs = []
for threshold in thresholds:
    tpr, fpr = compute_tpr_fpr(expected, actual, threshold)
    tprs.append(tpr)
    fprs.append(fpr)

plt.figure(figsize=(8, 6))
plt.plot(fprs, tprs, color="blue", label="ROC curve (100-point grid plus endpoints)")
plt.plot([0, 1], [0, 1], color="red", linestyle="--", label="Random classifier")
plt.title("ROC Curve")
plt.xlabel("False Positive Rate (FPR)")
plt.ylabel("True Positive Rate (TPR)")
plt.legend(loc="lower right")
plt.grid(True)
plt.show()
roc_auc = auc(fprs, tprs)
print(f"Area Under the ROC Curve (AUC), threshold-grid approximation: {roc_auc:.6f}")

# An exact ranking AUC provides a check independent of the chosen threshold grid.
from sklearn.metrics import roc_auc_score
pair_labels = np.eye(len(expected), dtype=int).ravel()
pair_scores = cosine_similarity(expected, actual).ravel()
print(f"Exact ranking AUC: {roc_auc_score(pair_labels, pair_scores):.6f}")