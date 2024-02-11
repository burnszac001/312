import matplotlib.pyplot as plt
import numpy as np

times_10 = [0, 0, 0, 0, 0]
times_100 = [0.002, 0.001, 0.001, 0.001, 0.001]
times_1_000 = [0.009, 0.008, 0.009, 0.008, 0.009]
times_10_000 = [0.037, 0.037, 0.037, 0.037, 0.037]
times_100_000 = [0.369, 0.357, 0.360, 0.371, 0.371]
times_1_000_000 = [4.421, 4.408, 4.444, 4.594, 4.428]

# Calculate the mean times
mean_times = [
    sum(times_10) / len(times_10),
    sum(times_100) / len(times_100),
    sum(times_1_000) / len(times_1_000),
    sum(times_10_000) / len(times_10_000),
    sum(times_100_000) / len(times_100_000),
    sum(times_1_000_000) / len(times_1_000_000)
]
print(mean_times)

# Define the number of points
num_points = [10, 100, 1000, 10000, 100000, 1000000]

log_points = [10, 100, 1000, 10000, 50000, 100000, 200000, 300000, 400000, 500000, 600000, 700000, 800000, 900000, 1000000]

nlogn = [0.00000032 * (n * np.log(n)) for n in log_points]

# Plot the graph
plt.plot(mean_times, num_points, marker='o', label="Convex Hull")
plt.plot(nlogn, num_points, marker='o', label=r'$3.2\times10^{-7}(x\log(x))$')
plt.xlabel('Mean Run Time (seconds)')
plt.ylabel('Number of Points')
plt.title('Number of Points vs Mean Run Time')
plt.yscale('log')  # Use logarithmic scale for x-axis
plt.legend()
plt.grid(True)
plt.show()