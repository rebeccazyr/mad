import matplotlib.pyplot as plt
import json

with open("true_false_retrieved_evidence.json", "r") as f:
    data = json.load(f)

# Create a figure and axis
fig, ax = plt.subplots()

# Plot red vertical lines for the first list
for x in data[0]:
    ax.axvline(x=x, color='red', linestyle='-', label='True' if x == data[0][0] else "")

# Plot blue vertical lines for the second list
for x in data[1]:
    ax.axvline(x=x, color='blue', linestyle='-', label='False' if x == data[1][0] else "")

# Add legend to distinguish the two lists
ax.legend()

# Set title and axis labels (optional)
ax.set_title('Vertical Lines from Two Lists')
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')

# Display the plot
plt.savefig("vertical_lines_plot.png")  # Save the figure instead of showing it
print("Plot saved as vertical_lines_plot.png")