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
def bubble_sort_descending_four(T1, T2, T3, T4):
    n = len(T1)

    # Traverse through all elements in T1
    for i in range(n - 1):
        # Last i elements are already sorted, so we don't need to check them
        for j in range(0, n - i - 1):
            # Swap if the element found is smaller than the next element in T1
            if T1[j] < T1[j + 1]:
                T1[j], T1[j + 1] = T1[j + 1], T1[j]
                T2[j], T2[j + 1] = T2[j + 1], T2[j]
                T3[j], T3[j + 1] = T3[j + 1], T3[j]
                T4[j], T4[j + 1] = T4[j + 1], T4[j]



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
def matrix_multiply(t1, t2):
    result = []

    for i in range(len(t1)):
        row = []
        for j in range(len(t2[0])):
            value = 0
            for k in range(len(t1[0])):
                value += t1[i][k] * t2[k][j]
            row.append(value)
        result.append(tuple(row))

    return result               

def porsuite_equation(old,result,suivi):
    new = []
    for i in range(len(old)):
       
          sum = (old[i][0] + result[i][0], old[i][1] + result[i][1])
                     
          new.append(sum)
    return new      
def porsuite_equation_random(old,randomx,randomy,rangee):
    new = []
    for i in range(len(old)):
       
          sum = (old[i][0] + randomx*rangee, old[i][1] + randomy*rangee)
          #sum = (old[i][0] + randomx*rangee ,old[i][1]  + randomy*rangee)
                     
          new.append(sum)
    return new                   
def comparison(list1, list2,sollist1,sollist2,cutt):
    nbr=len(list1)-cutt
    last_seven_list1 = list1[-(nbr):]
    last_seven_sol1=sollist1[-(nbr):]
    new__m_cvrgs = []
    new__m_sol=[]
    for i in range(nbr):
        if last_seven_list1[i] > list2[i]:
            new__m_cvrgs.append(last_seven_list1[i])
            new__m_sol.append(last_seven_sol1[i])
        else:
            new__m_cvrgs.append(list2[i])
            new__m_sol.append(sollist2[i])
    new_m_cvrgs = list1[:cutt] + new__m_cvrgs
    new_m_sol = sollist1[:cutt] + new__m_sol

    return new_m_cvrgs,new_m_sol


def comparison_sol(list1, list2,best_sol_every_iteration,all_new,cutt):
    nbr=len(list1)-cutt
    last_seven_list1 = list1[-(nbr):]
    new__m_cvrgs = []
    new__m_sol=[]
    for i in range(nbr):
        if last_seven_list1[i] > list2[i]:
            new__m_cvrgs.append(last_seven_list1[i])
            new__m_sol.append(best_sol_every_iteration[i])
        else:
            new__m_cvrgs.append(list2[i])
            new__m_sol.append(all_new[i])
    new_m_cvrgs = list1[:cutt] + new__m_cvrgs
    new_m_sol = list1[:cutt] + new__m_sol

    return new_m_sol

                 
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
        M0=0
        N0=0
        Mm0=[M0,M/2,M0,M/2]
        Nn0=[N0,N0,N/2,N/2]
        Mm=[M/2,M,M/2,M]
        Nn=[N/2,N/2,N,N]
        num_sensors = 80
        num_sensorss=[num_sensors/4,num_sensors/4,num_sensors/4,num_sensors/4]
        sensing_range=9
        for iteration in range(num_itr):
            # Randomly generate the positions of sensors
            
            sensor_positions = [(random.uniform(1+M0+sensing_range, M-sensing_range), random.uniform(1+N0+sensing_range, N-sensing_range)) for _ in range(num_sensors)]
            
            coverages=probability_multiplesensors_multipoints(M, N,sensor_positions , sensing_range)  
            all_coverage_rates.append(coverages)
            all_sensor_positions.append(sensor_positions)
            bubble_sort_descending(all_coverage_rates, all_sensor_positions)
            
            sensor_positions_with_coverage.append((sensor_positions, coverages))
            
            if coverages > maxCov :
              maxCov = coverages

        print("*********************************    First 10 coverages ****************************")
        print(all_coverage_rates)

              
        nbr_voisin=10#10
        iterations=30
        #20
        the10Voisins=[]
        the10Covvoisin=[]
        #len(the_best_10_solution1)
        bes_sol_after_20iter=[]
        best_cov_after20iter=[]
        tabu_list=[]
        tabu_list_max_size=10
        
        for i in range(len(all_sensor_positions)):#10
            bestsol=all_sensor_positions[i]
            bestCov=all_coverage_rates[i]
            #the liste li fiha the best coverages in every iteration(20)
            best_sol_every_iteration=[]
            best_cov_every_iteration=[]
            
            
            for w in range(iterations):#20
              
                the10Voisins=[]
                the10Covvoisin=[]
                
                
            
                for x in range(nbr_voisin):#10
                    
                    voisin=[]
                    
                    for j in range(len(bestsol)):#70
                         randomX=sensing_range*(random.uniform(-0.5,0.5))
                         randomY=sensing_range*(random.uniform(-0.5,0.5))
                         X=bestsol[j][0]+randomX
                         Y=bestsol[j][1]+randomY
                         if   X  > M - sensing_range  :
                              X = M - sensing_range
                         if Y > N - sensing_range  :
                             Y = N- sensing_range
                         if X <  M0+sensing_range:
                             X =  M0+sensing_range
                         if Y <  N0+sensing_range:
                             Y =  N0+sensing_range

                         voisin.append((X,Y))
                    
                
                    
                    the10Voisins.append(voisin)
                    CovVoisin=probability_multiplesensors_multipoints(M, N,voisin , sensing_range) 
                    the10Covvoisin.append(CovVoisin)
                    
                    


                bubble_sort_descending(the10Covvoisin, the10Voisins)
                bestsol=the10Voisins[0]
                bestCov=the10Covvoisin[0]
                

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

            bubble_sort_descending(best_cov_every_iteration, best_sol_every_iteration)  
            bes_sol_after_20iter.append(best_sol_every_iteration[0])
            best_cov_after20iter.append(best_cov_every_iteration[0])
        print("*********************************    Matrice M after Tabou list *********************************")
        #bubble_sort_descending(all_coverage_rates, all_sensor_positions)

        
       # print("bes_sol_after_20iter (matrice M)",bes_sol_after_20iter)
        
        print("best_cov_after20iter (de M)",best_cov_after20iter)
        
        
      



        #***********************************************************************************************************************
        #***********************************************************************************************************************
        #porsuite
        #***********************************************************************************************************************
        #***********************************************************************************************************************
    
    # porsuite et les nouveaux couvertures
        print("*********************************************************************************************") 
        print("****************************** Sensors after porsuite*****************************************")  
        print("*********************************************************************************************") 
        
        iteration=200
        for u in range(iteration):
            all_distances=[]
            pourcentage=0.3
            cutt=round(pourcentage*len(all_sensor_positions))
            all_new=[]
            all_suivi=[]
            all_ri=[]
            all_old=[]
            new_coverages=[]
            APi=random.uniform(-0.003,0.003)

            for i in range(cutt, len(all_sensor_positions)):
                   flight=[]
                   distanceM_X=[]
                   random_nbr=random.randint(0,cutt-1)
                   ri=random.uniform(-0.003,0.003)
                   old =all_sensor_positions[i]
                   suivi=all_sensor_positions[random_nbr]
                   matriceM=bes_sol_after_20iter[i]
                   riX=random.uniform(-0.5,0.5)
                   riY=random.uniform(-0.5,0.5)
                   
                   for j in range(num_sensors):
                       new_sensors2=[]
                       
                       distance = calculate_absolute_distance(old[j],suivi[j] )
                       distancee=calculate_absolute_distance(old[j],matriceM[j])

                       distanceM_X.append(distancee)
                       flight.append(distance)
                       
                       
                   all_ri.append(ri)
                   all_suivi.append(all_suivi)
                   all_old.append(old)
                   #new_sensors=porsuite_equation(old,flight_ri(flight,ri),suivi) 
                   if APi <= ri:
                       new_sensors=porsuite_equation(old,matrix_multiply(flight_ri(flight,ri), distanceM_X),suivi) 
                   else :
                       new_sensors=porsuite_equation_random(old,riX,riY,sensing_range) 
                   for k in range(len(new_sensors)):#70
                         X=new_sensors[k][0]
                         Y=new_sensors[k][1]
                         if   X  > M - sensing_range  :
                              X = M - sensing_range
                         if Y > N - sensing_range  :
                             Y = N- sensing_range
                         if X <  M0+sensing_range:
                             X =  M0+sensing_range
                         if Y <  N0+sensing_range:
                             Y =  N0+ sensing_range

                         new_sensors2.append((X,Y))   
                   new_sensors=new_sensors2      
                   cvrgs=probability_multiplesensors_multipoints(M, N,new_sensors , sensing_range)  
                   new_coverages.append(cvrgs)
                   all_distances.append(flight)
                   
                   all_new.append(new_sensors)
                   #bubble_sort_descending(new_coverages, all_new)
            #print("**********************************************")         
            #print("new_coverages") 
            #print(new_coverages)
            new__cov=[]
            new__sol=[]
            new__cov_M=[]
            new__sol_M=[]
            
            #new_m_cov=comparison(best_cov_after20iter, new_coverages , bes_sol_after_20iter,all_new)
            new__cov,new__sol=comparison(all_coverage_rates, new_coverages , all_sensor_positions,all_new,cutt)
            new__cov_M,new__sol_M=comparison(best_cov_after20iter, new_coverages , bes_sol_after_20iter,all_new,cutt)
            best_cov_after20iter=new__cov_M          
            bes_sol_after_20iter=new__sol_M
            all_coverage_rates=new__cov        
            all_sensor_positions=new__sol
            bubble_sort_descending_four(all_coverage_rates,all_sensor_positions,best_cov_after20iter,bes_sol_after_20iter)
            
            
            max_value = max(best_cov_after20iter)
            max_valuee = max(all_coverage_rates)
            
            #print(" max de M:",max_value)
            #print(" les couverures after comparison :",all_coverage_rates)
            #print("*****************************************",u)
        print(" les couverures after porsuite :",all_coverage_rates)    
        
        print("after porsuite (de M)",best_cov_after20iter)
        
                   
       
        #***********************************************************************************************************************
        #***********************************************************************************************************************
        #porsuite
        #***********************************************************************************************************************
        #***********************************************************************************************************************
        print("*********************************************************************************************") 
        print("****************************** Sensors after EVASION *****************************************")  
        print("*********************************************************************************************")
        itr_evasion=500
        evasion_cov_after_all_itr=[]
        evasion_sol_after_all_itr=[]

        for j in range (itr_evasion):
            all_10voisins_evasion=[]
            all_10cov_evasion=[]
                
            for i in range(len(all_sensor_positions)):#10 sol
                    voisin_Evasion=[]
                    every_sensor=all_sensor_positions[i]
                    random_sensing_range=random.randint(1,sensing_range)
                     
                    for j in range(len(every_sensor)):#70 points
            
                         ##### hna
                         random_X_evasion=random_sensing_range*(random.uniform(-7.5,7.5)) 
                         random_Y_evasion=random_sensing_range*(random.uniform(-7.5,7.5))
                         X=every_sensor[j][0]+random_X_evasion
                         Y=every_sensor[j][1]+random_Y_evasion
                         if   X  > M - sensing_range  :
                              X = M - sensing_range
                         if Y > N - sensing_range  :
                             Y = N- sensing_range
                         if X <  M0+sensing_range:
                             X =  M0+sensing_range
                         if Y <  N0+sensing_range:
                             Y =  N0+sensing_range

                         voisin_Evasion.append((X,Y))#1
                    cov_evasion=probability_multiplesensors_multipoints(M, N,voisin_Evasion, sensing_range)
                    all_10cov_evasion.append(cov_evasion) 
                    all_10voisins_evasion.append(voisin_Evasion) 
            #print(all_10cov_evasion) #10  
            evasion_cov_after_all_itr.append(all_10cov_evasion)
            evasion_sol_after_all_itr.append(all_10voisins_evasion)
                    
        cov=all_coverage_rates
        sol=all_sensor_positions
        best_cov1=evasion_cov_after_all_itr
        best_sol1=evasion_sol_after_all_itr
        Mcov=best_cov_after20iter
        Msol=bes_sol_after_20iter

        for j in range(len(all_sensor_positions)):
            best_cov2=[]
            best_sol2=[]
            for i in range(len(best_cov1)):
                best_cov2.append(best_cov1[i][j])
                best_sol2.append(best_sol1[i][j])
    
            paired_values = zip(best_cov2, best_sol2)
            max_value = max(paired_values)
            max_value_cov, max_value_sol = max_value
    
            if max_value_cov>cov[j]:
               cov[j]=max_value_cov
               sol[j]=max_value_sol  

            if max_value_cov>Mcov[j]:
              Mcov[j]=max_value_cov
              Msol[j]=max_value_sol    
    
        print("*******************sol,cov after mis a jour de evasion***************")
        #print(sol)
        print(cov)  
        print("***************sol M,cov M after evasion ******************************")
        #print(Msol)
        bubble_sort_descending(Mcov,Msol)
        print(Mcov) 
            
              










        

        
        #print("Best Sensor positions:",bes_sol_after_20iter[0])
        #print("The best Coverage:",probability_multiplesensors_multipoints(M, N,bes_sol_after_20iter[0], sensing_range) )
         
        

        

        
        

       
        for x, y in  Msol[0]: 
             
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