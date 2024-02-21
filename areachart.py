import math
import sys
import random
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
def calculate_euclidean_distance(point1, point2):
    #kenza
    
    # Calculate the square of the differences in coordinates
    delta_x = point1[0] - point2[0]
    delta_y = point1[1] - point2[1]

    # Calculate the square of the Euclidean distance
    distance_squared = delta_x**2 + delta_y**2

    # Calculate the Euclidean distance by taking the square root
    distance = distance_squared**0.5

    return distance

def select_solution_not_in_tabuu(bestsol,tabu_list):
    if bestsol not in tabu_list:
        return bestsol
    return None

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
def calculate_absolute_distance(point1, point2):
    delta_x = point1[0] - point2[0]
    delta_y = point1[1] - point2[1]

    # Calculate the absolute difference for each coordinate
    absolute_distance_x = abs(delta_x)
    absolute_distance_y = abs(delta_y)

    return (absolute_distance_x, absolute_distance_y)
def flight_ri(flight,ri):
    result = []
   
    for i in range(len(flight)):
        
        result.append((flight[i][0]* ri, flight[i][ 1] * ri))
    return result                  
def porsuite_equation(old,result,suivi):
    new = []
    for i in range(len(old)):
       if old[i][0]<suivi[i][0] and old[i][1]<suivi[i][1]:
          sum = (old[i][0] + result[i][0], old[i][1] + result[i][1])
       elif old[i][0]>suivi[i][0] and old[i][1]>suivi[i][1]  :
          sum = (old[i][0] - result[i][0], old[i][1] - result[i][1]) 
       elif old[i][0]<suivi[i][0] and old[i][1]>suivi[i][1]  :
          sum = (old[i][0] + result[i][0], old[i][1] - result[i][1]) 
       elif old[i][0]>suivi[i][0] and old[i][1]<suivi[i][1]  :
          sum = (old[i][0] - result[i][0], old[i][1] + result[i][1]) 
       elif old[i][0]==suivi[i][0] and old[i][1]>suivi[i][1]  :
          sum = (old[i][0] + result[i][0], old[i][1] - result[i][1])  
       elif old[i][0]>suivi[i][0] and old[i][1]==suivi[i][1]  :
          sum = (old[i][0] - result[i][0], old[i][1] + result[i][1])        
       else : 
          sum = (old[i][0] + result[i][0], old[i][1] + result[i][1])               
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
        #print(all_sensor_positions)
        #print(all_coverage_rates)

        print("----------------------------------------------")
        print("----------------------------------------------")
         
        
        all_distances=[]
        pourcentage=0.3
        cutt=round(pourcentage*len(all_sensor_positions))
        all_new=[]
        all_suivi=[]
        all_ri=[]
        all_old=[]
        new_coverages=[]
        
# porsuite et les nouveaux couvertures
        for i in range(cutt, len(all_sensor_positions)):
                   distancee=[]
                   random_nbr=random.randint(0,cutt-1)
                   ri=random.uniform(0.9,1)
                   
                   for j in range(num_sensors):
                       old =all_sensor_positions[i]
                       suivi=all_sensor_positions[random_nbr]
                       distance = calculate_absolute_distance(old[j],suivi[j] )
                       distancee.append(distance)
                       
                       
                   all_ri.append(ri)
                   all_suivi.append(all_suivi)
                   all_old.append(old)
                   new_sensors=porsuite_equation(old,flight_ri(distancee,ri),suivi) 
                   cvrgs=probability_multiplesensors_multipoints(M, N,new_sensors , sensing_range)  
                   new_coverages.append(cvrgs)
                   all_distances.append(distancee)
                   
                   all_new.append(new_sensors)
        
                   
                   
                  
        all_coverages = new_coverages +all_coverage_rates
        all_positions= all_new + all_sensor_positions
        bubble_sort_descending(all_coverages, all_positions)
        print("________________________________________________________") 
        #print("all coverage")    
        #print(all_coverages)
        print("________________________________________________________")  
        #print("all positions")    
        #print(all_positions)
        print("________________________________________________________")  
        print("best 10 solutions")   
        the_best_10_solution1=[]
        the_best_10_couverages1=[]
         
        for i in range (10):
               the_best_10_solution1.append(all_positions[i])
               the_best_10_couverages1.append(all_coverages[i])
        print(the_best_10_couverages1)
        print(the_best_10_solution1)  
        
        
        nbr_voisin=15#10
        iterations=30
        #20
        the10Voisins=[]
        the10Covvoisin=[]
        #len(the_best_10_solution1)
        bes_sol_after_20iter=[]
        best_cov_after20iter=[]
        tabu_list=[]
        tabu_list_max_size=10
        
        for i in range(len(the_best_10_solution1)):#10
            bestsol=the_best_10_solution1[i]
            bestCov=the_best_10_couverages1[i]
            #the liste li fiha the best coverages in every iteration(20)
            best_sol_every_iteration=[]
            best_cov_every_iteration=[]
            
            
            for w in range(iterations):#20
              
                the10Voisins=[]
                the10Covvoisin=[]
                randomxx=[]
                randomyy=[]
                
            
                for x in range(nbr_voisin):#10
                    randomX=sensing_range*(random.uniform(-0.5,0.5))
                    randomY=sensing_range*(random.uniform(-0.5,0.5))
                    voisin=[]
                    
                    for j in range(len(bestsol)):#70
                         randomX=sensing_range*(random.uniform(-0.5,0.5))
                         randomY=sensing_range*(random.uniform(-0.5,0.5))
                         voisin.append((bestsol[j][0]+randomX,bestsol[j][1]+randomY))
                    #randomxx.append(randomX)  
                    #randomyy.append(randomY)  
                    the10Voisins.append(voisin)
                    CovVoisin=probability_multiplesensors_multipoints(M, N,voisin , sensing_range) 
                    the10Covvoisin.append(CovVoisin)
                    
                    


                bubble_sort_descending(the10Covvoisin, the10Voisins)
                bestsol=the10Voisins[0]
                bestCov=the10Covvoisin[0]
                #print("voisins ",the10Voisins)
                #print("cov ",the10Covvoisin)

                bestsolution=select_solution_not_in_tabuu(bestsol,tabu_list)

                if bestsolution is None:
                    bestsol=the10Voisins[1]
                    bestCov=the10Covvoisin[1]
                    best_sol_every_iteration.append(bestsol)
                    best_cov_every_iteration.append(bestCov)
                    tabu_list.append(bestsol)
                    if len(tabu_list) > tabu_list_max_size:
                         tabu_list.pop(0)
                    
                    
                    
                else:
                    tabu_list.append(bestsol)
                    best_sol_every_iteration.append(bestsol)
                    best_cov_every_iteration.append(bestCov)
                    if len(tabu_list) > tabu_list_max_size:
                         tabu_list.pop(0)




                #best_sol_every_iteration.append(bestsol)
                #best_cov_every_iteration.append(bestCov)
                #print("************************************")
                #print("i ",i)
                #print("w ",w)
                #print("randomx ",randomxx)
                #print("randomy ",randomyy)
                
                # Select the best solution not in the Tabu list
                
            #print('tabu_list')
            #print(tabu_list)


            bubble_sort_descending(best_cov_every_iteration, best_sol_every_iteration)  
            bes_sol_after_20iter.append(best_sol_every_iteration[0])
            best_cov_after20iter.append(best_cov_every_iteration[0])
        print("*********************")
        print("bes_sol_after_20iter",bes_sol_after_20iter)
        print("best_cov_after20iter",best_cov_after20iter)
        bubble_sort_descending(best_cov_after20iter,bes_sol_after_20iter)

        




        #print("the seven vectors of distance") 
        #print(all_distances)    
        print("_______________________________________________________")  
        #print("capteurs suivis ",suivi)
        print("_________________________________________________________")  
        #print("old",all_old)
        print("_______________________________________________________")  
        #print(" ri",all_ri)
        print("____________________________________________________________")  
        #print("new sensor")    
        #print(all_new)
        print("____________________________________________________________")  
        #print("new coverages")    
        #print(new_coverages)

        

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
        #print("Best Sensor positions:",best_sensor_positions )
        #print("The best Coverage:",probability_multiplesensors_multipoints(M, N,best_sensor_positions, sensing_range) )
        print("Best Sensor positions:",bes_sol_after_20iter[0])
        print("The best Coverage:",probability_multiplesensors_multipoints(M, N,bes_sol_after_20iter[0], sensing_range) )
         
        
        #for x, y in new_sensors:
        #for x, y in the_best_10_solution1[0]:
        for x, y in  bes_sol_after_20iter [0]: 
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

