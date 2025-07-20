import matplotlib.pyplot as plt
import json
import seaborn as sns

# Load data
with open("true_false_retrieved_evidence.json", "r") as f:
    data = json.load(f)

# Determine list1 and list2 from dict or list
if isinstance(data, dict):
    keys = list(data.keys())
    list1 = data[keys[0]]
    list2 = data[keys[1]]
else:
    list1 = data[0]
    list2 = data[1]

# Sort the values (optional, for neatness)
list1 = sorted(list1)
list2 = sorted(list2)

# Plot KDE
sns.kdeplot(list1, color='red', label='True', fill=True)
sns.kdeplot(list2, color='blue', label='False', fill=True)

plt.title("Value Distribution (KDE)")
plt.xlabel("Value")
plt.ylabel("Density")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("kde_distribution_plot.png")
print("Plot saved as kde_distribution_plot.png")