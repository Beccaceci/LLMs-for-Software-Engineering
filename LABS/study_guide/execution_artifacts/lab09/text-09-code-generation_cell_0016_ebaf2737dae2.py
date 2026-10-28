import matplotlib.pyplot as plt
import numpy as np


languages = list(overall_results.keys())  



cc_values = [overall_results[language]['CC'] for language in languages]
mi_values = [overall_results[language]['MI'] for language in languages]
loc_values = [overall_results[language]['LOC'] for language in languages]
comments_values = [overall_results[language]['Comments'] for language in languages]
functional_correctness = [overall_results[language]['FunctionalCorrectness'] for language in languages]

# Create a figure with subplots for each metric
fig, axs = plt.subplots(3, 2, figsize=(10, 8))

# Plotting CC values
axs[0, 0].bar(languages, cc_values, color='skyblue')
axs[0, 0].set_title('Cyclomatic Complexity (CC)')
axs[0, 0].set_ylabel('CC')

# Plotting MI values
axs[0, 1].bar(languages, mi_values, color='lightgreen')
axs[0, 1].set_title('Maintainability Index (MI)')
axs[0, 1].set_ylabel('MI')

# Plotting LOC values
axs[1, 0].bar(languages, loc_values, color='blue')
axs[1, 0].set_title('Lines of Code (LOC)')
axs[1, 0].set_ylabel('LOC')

# Plotting Comments values
axs[1, 1].bar(languages, comments_values, color='lightcoral')
axs[1, 1].set_title('Number of Comments')
axs[1, 1].set_ylabel('Comments')
axs[1, 1].set_ylim(0, max(comments_values + [1]) * 1.1)

#plotting functional correctness
axs[2, 0].bar(languages, functional_correctness, color='green')
axs[2, 0].set_title('Functional correctness')
axs[2, 0].set_ylabel('Passed / executed tests')
axs[2, 0].set_ylim(0, 1.05)
axs[2, 1].axis('off')

# Adjust layout and display the plot
plt.tight_layout()
Path("execution/figures").mkdir(parents=True,exist_ok=True)
fig.savefig("execution/figures/grade_code_metrics.png",dpi=160,bbox_inches="tight")
plt.show()
