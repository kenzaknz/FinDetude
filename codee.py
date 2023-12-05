import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import numpy as np

# Generate 15 random data points
total=15

x_values = np.random.randint(0, 20, size=total)
y_values = np.random.randint(0, 20, size=total)

#background image
image_path = 'map.jpg'
img = plt.imread(image_path)
# Calculate the size for each category
size_per_category = total // 3

# Create an array of sizes with equal numbers of each category
sizes = np.concatenate([np.full(size_per_category, 700),
                        np.full(size_per_category, 1200),
                        np.full(size_per_category, 1700)])


#random _ size
#_sizes_per_category = 5
#_sizes =np.random.choice([700,1000, 1400],sizes_per_category)
marker_sizes = sizes 



# Specify colors corresponding to each size
size_colors = {700: 'red', 1200: 'green', 1700: 'blue'}
colors = [size_colors[original_size] for original_size in sizes]

# Create a scatter plot with squares
# code by kenza
plt.scatter(x_values, y_values, color=colors,edgecolors='black', linewidths=1, marker='o',s=marker_sizes,zorder=15)

# Display the image as the background
plt.imshow(img, extent=[min(x_values), max(x_values), min(y_values), max(y_values)], aspect='auto', alpha=1)

# Add a background grid
plt.grid(True,alpha=0.5)

# Add labels and title
plt.xlabel('X ')
plt.ylabel('Y')
plt.title(' 15 Sensors in map')

# Add a legend
plt.legend()

# Display the chart
plt.show()