import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


# First set of x and y values (same length)
x1 = [1, 2, 3, 4, 5]
y1 = [2, 4, 1, 8, 7]

# Second set of x and y values (same length)
x2 = [1, 2, 3, 4, 5]
y2 = [1, 3, 5, 4, 6]

# Plot first dataset as a line graph
plt.plot(x1, y1, marker="o", label="Line 1")

# Plot first dataset as a scatter plot
plt.scatter(x1, y1, color="red", label="Scatter 1")

# Add second dataset as a line graph
plt.plot(x2, y2, marker="s", linestyle="--", label="Line 2")

# Add title and axis labels
plt.title("Simple Line and Scatter Visualization")
plt.xlabel("X Values")
plt.ylabel("Y Values")
plt.legend()
plt.grid(True, linestyle=":", alpha=0.6)
plt.tight_layout()
plt.savefig("Ex2_plot.png")
print("Visualization created: Ex2_plot.png")
