import math
import sys
import random
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
def calculate_euclidean_distance(point1, point2):
    #abdessamed 
    #kenza
    
    # Calculate the square of the differences in coordinates
    delta_x = point1[0] - point2[0]
    delta_y = point1[1] - point2[1]

    # Calculate the square of the Euclidean distance
    distance_squared = delta_x**2 + delta_y**2

    # Calculate the Euclidean distance by taking the square root
    distance = distance_squared**0.5

    return distance
def probability_singlepoint_singlesensor(point_coordinates, sensor_coordinates, sensor_range):
    
    
    # Calculate the Euclidean distance between the sensor and the target point
    distance = calculate_euclidean_distance(point_coordinates, sensor_coordinates)

    # Check if the distance is less than or equal to the sensing range
    if distance <= sensor_range:
        return 1
    else:
        return 0

# Assume you have defined the calculate_euclidean_distance function separately

def probability_multiplesensors_singlepoint(num_sensors, point_coordinates, sensor_coordinates, sensor_range):
    
    # Calculate the product of (1 - probability_singlepoint_singlesensor) for each sensor
    product = 1
    for i in range(num_sensors):
        product *= 1 - probability_singlepoint_singlesensor(point_coordinates, sensor_coordinates[i], sensor_range)

    # Calculate the overall probability of coverage
    probability_coverage = 1 - product

    return probability_coverage    
def probability_multiplesensors_multipoints(M, N, sensor_coordinates, sensor_range):
    
    # Calculate the sum of probabilities for each point
    total_probability = 0
    #coverage_rates=[]
    for xt in range(1, M ):
        for yt in range(1, N ):
            point_coordinates = (xt, yt)
            total_probability += probability_multiplesensors_singlepoint(len(sensor_coordinates), point_coordinates, sensor_coordinates, sensor_range)
    coverage_rate = total_probability / (M * N)
    #coverage_rates.append(coverage_rate)
    return coverage_rate

def bubble_sort_descending(T1, T2):
    n = len(T1)

    # Traverse through all elements in T1
    for i in range(n - 1):
        # Last i elements are already sorted, so we don't need to check them
        for j in range(0, n - i - 1):
            # Swap if the element found is smaller than the next element in T1
            if T1[j] < T1[j + 1]:
                T1[j], T1[j + 1] = T1[j + 1], T1[j]
                T2[j], T2[j + 1] = T2[j + 1], T2[j]
def flight_ri(flight,ri):
    result = []
   
    for elem in flight:
         result.append(elem * ri)
    return result                  
def porsuite_equation(old,result):
    new = []
    for i in range(len(old)):
       sum = (old[i][0] + result[i], old[i][1] + result[i])
       new.append(sum)
    return new                  
class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PySide6 Matplotlib Example")
        self.setGeometry(100, 100, 1050, 600)

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout(main_widget)

        # Create a Matplotlib figure
        self.figure = Figure(figsize=(9, 8), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Add an image to the background
        img_path = 'mapdbtt.jpg'
        img = plt.imread(img_path)

        # Create a new plot
        ax = self.figure.add_subplot(111)

        # Display the image as the background with 'none' interpolation
        ax.imshow(img, extent=[0, 150, 0, 85], aspect='auto', alpha=1)

        # Add homogeneous sensors with the same size (light blue points) and same color
        #sensor_size =3710 #8
        sensor_size =4200 #9



        sensor_color = '#add8e6'  # Light Blue

       

        

        # Set labels and title
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        ax.set_title('the area of interest')

        # Generate different placements of sensors 10 times
        all_coverage_rates = []
        #all_sensor_positions = []
        best_sensor_positions = None
        maxCov = float('-inf')  
        sensor_positions_with_coverage = []
        all_sensor_positions = []
        num_itr=10
        M=150
        N=85
        sensing_range=9
        for iteration in range(num_itr):
            # Randomly generate the positions of sensors
            num_sensors = 80
            sensor_positions = [(random.uniform(1+sensing_range, M-sensing_range), random.uniform(1+sensing_range, N-sensing_range)) for _ in range(num_sensors)]
            
            coverages=probability_multiplesensors_multipoints(M, N,sensor_positions , sensing_range)  
            all_coverage_rates.append(coverages)
            all_sensor_positions.append(sensor_positions)
            bubble_sort_descending(all_coverage_rates, all_sensor_positions)
            # Display the coordinates without plotting
            #print(f"Iteration {iteration + 1}: Sensor Positions - {sensor_positions} : coverage - {coverages}")
             # Update the list of sensor positions with their coverage
            sensor_positions_with_coverage.append((sensor_positions, coverages))
            
            if coverages > maxCov :
              maxCov = coverages
              best_sensor_positions = sensor_positions
        # Sort the list of sensor positions with their coverage by coverage in descending order
        sorted_sensor_positions_with_coverage = sorted(sensor_positions_with_coverage, key=lambda x: x[1], reverse=True)
        
        print("----------------------------------------------")
        print("----------------------------------------------")
        # Print the sorted sensor positions with their coverage
        print("Sorted Sensor Positions with Coverage:")
        #for sensor_positions, coverage in sorted_sensor_positions_with_coverage:
         #print(f"Sensor Positions - {sensor_positions} : Coverage - {coverage}")
        print(all_sensor_positions)
        print(all_coverage_rates)

        print("----------------------------------------------")
        print("----------------------------------------------")
         
        
        all_distances=[]
        pourcentage=0.3
        cutt=round(pourcentage*len(all_sensor_positions))
        all_new=[]
        all_random_nbr=[]
        all_ri=[]
        all_old=[]
        new_coverages=[]
        
# porsuite et les nouveaux couvertures
        for i in range(cutt, len(all_sensor_positions)):
                   distancee=[]
                   old=[]
                   
                   random_nbr=random.randint(0,cutt-1)
                   ri=random.uniform(0,1)
                   
                   for j in range(num_sensors):
                   
                       distance = calculate_euclidean_distance(all_sensor_positions[i][j],all_sensor_positions[random_nbr][j] )
                       distancee.append(distance)
                       old=all_sensor_positions[i]
                       
                       

                   all_ri.append(ri)
                   all_random_nbr.append(random_nbr)
                   new_sensors=porsuite_equation(old,flight_ri(distancee,ri)) 
                   cvrgs=probability_multiplesensors_multipoints(M, N,new_sensors , sensing_range)  
                   new_coverages.append(cvrgs)
                   all_distances.append(distancee)
                   all_old.append(old)
                   all_new.append(new_sensors)
        
                   
                   
                  

        print("the seven vectors of distance") 
        print(all_distances)    
        print("_______________________________________________________")  
        print("random number",all_random_nbr)
        print("_________________________________________________________")  
        print("old",all_old)
        print("_______________________________________________________")  
        print(" ri",all_ri)
        print("____________________________________________________________")  
        print("new sensor")    
        print(all_new)
        print("____________________________________________________________")  
        print("new coverages")    
        print(new_coverages)

        #sorted_coverage_rates = sorted(all_coverage_rates)
        #print(sorted_coverage_rates)
        #print("Sorted Coverage Rates:",sorted(all_coverage_rates, reverse=True))
        # Get the three maximum coverage rates
        #max_three_coverage_rates = sorted_coverage_rates[-3:]

           # Get the last seven minimum coverage rates
        #min_seven_coverage_rates = sorted_coverage_rates[:7]

        print("----------------------------------------------")
        print("----------------------------------------------")
        

        #print("Three Maximum Coverage Rates:", max_three_coverage_rates)
       
        #print("Last Seven Minimum Coverage Rates:", min_seven_coverage_rates)
        
        #print("Sorted Coverage Rates:",sorted(all_coverage_rates, reverse=True))
        print("----------------------------------------------")
        print("----------------------------------------------")
        print("Best Sensor positions:",best_sensor_positions )
        print("The best Coverage:",probability_multiplesensors_multipoints(M, N,best_sensor_positions, sensing_range) )
         
        
        for x, y in new_sensors:
        #for x, y in best_sensor_positions:       
            # Add sensors
               ax.scatter(x, y, s=sensor_size, c=sensor_color, alpha=0.8, edgecolors='black')

            # Add a black "X" at the center for precision
               ax.text(x, y, 'X', color='black', ha='center', va='center', fontsize=7, alpha=1)    
        # Add grid lines
        ax.grid(True,linestyle='--' , alpha=1, color='black')
  
        # Refresh canvas
        self.canvas.draw()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec())

