from operator import itemgetter

bonus = 0
score = 0

def compute_score(myride):
    global score
    global bonus
    score += myride.duration
    if(myride.isearly):
        score += bonus

class car:

    def __init__(self, end):

        self.courses=[]
        self.remainingsteps=None
        self.available_times = []
        self.available_times.append([[0,0],0,end])
        

class ride:
    done = False
    def __init__(self,number,start_position,end_position,earliest_departure,latest_arrival):
        self.number=number
        self.start_position=start_position
        self.end_position=end_position
        self.earliest_departure=earliest_departure
        self.latest_arrival=latest_arrival
        self.duration=distance(self.start_position, self.end_position)
        self.isearly=False

def init_cars(car_nb, end):
    cars = []
    for i in range(car_nb):
        cars.append(car(end))
    return cars

def init_rides(ride_list, end):
    rides = []
    ride_possible = 0
    early_rides_possible = 0
    for r in ride_list:
        ride_number = r[0]
        start_position = r[1]
        end_position = r[2]
        earliest_start = r[3]
        latest_arrival = r[4]
        ride_duration = distance(start_position, end_position)
        distance_to_start = distance([0,0], start_position)
        full_distance = distance_to_start + ride_duration
        if full_distance <= latest_arrival and full_distance <= end :
            rides.append(ride(ride_number, start_position, end_position, earliest_start, latest_arrival))
            ride_possible+=1
            
            if distance_to_start <= earliest_start :
                early_rides_possible += 1  
                
    #print("number of possible rides: " + str(ride_possible))
    #print("number of earliest ride possible: "+str(early_rides_possible))        
    return rides


def car_data(myride, car_pos, time):
    earliest_time = False
    ride_start = myride.start_position
    ride_end = myride.end_position
    early_time = myride.earliest_departure
    latest_time = myride.latest_arrival
    car_to_ride = distance(car_pos, ride_start)
    ride_to_end = distance(ride_start, ride_end)
    earliest_arrival_time = int(time) + int(car_to_ride)
    if(time + car_to_ride <= early_time):
        earliest_time = True
    real_start = max(earliest_arrival_time, early_time)
    real_end = real_start + ride_to_end
    return latest_time, real_end, real_start, earliest_time

def best_ride_possible(mycar, ridelist, end, is_earliest):
    
    bestride = None
    mintime = 1000000
    bestavail = None
    no_better_cpt = 0

    for myride in ridelist:
        for avail_time in mycar.available_times:
               
            car_pos = avail_time[0]
            start_time = avail_time[1]
            end_time = avail_time[2]
            
            ride_start = myride.earliest_departure
            ride_duration = distance(myride.start_position, myride.end_position)
            time_to_arrive_start = distance(car_pos, myride.start_position)
            time_at_start = start_time + time_to_arrive_start
            better_start = max(ride_start, time_at_start)

            
            if(is_earliest and time_at_start > myride.earliest_departure):
                continue
            
            
            time_at_arrival =better_start + ride_duration
            if(time_at_arrival > end or time_at_arrival > myride.latest_arrival or time_at_arrival > end_time):
                continue

            if better_start < mintime:
                mintime = better_start
                bestavail = avail_time
                bestride = myride
            else:
                no_better_cpt += 1
        if(no_better_cpt > 5 and is_earliest ):
            break

    if(is_earliest and bestride != None):
        bestride.isearly = True
                   
    return bestride, bestavail

def distance(start, end):
    return abs(end[0] - start[0]) + abs(end[1] - start[1])


def simulate_cars(end, ride_list, car_list, cpt):
    length = len(car_list)
    #k = 0

    for mycar in car_list:

        #print("finding the best rides for car number : "+str(k))
        #k = k +1
        
        bestride, bestavail = best_ride_possible(mycar, ride_list, end, True)
        while(bestride != None):
            mycar.courses.append(bestride)
            ride_temp = []
            for myride in ride_list:
                if (myride.number != bestride.number):
                    ride_temp.append(myride)
            ride_list = ride_temp
            
            avail_temp = []
            for myavail in mycar.available_times:
                if (myavail[0] != bestavail[0] or myavail[1] != bestavail[1] or myavail[2] != bestavail[2]):
                    avail_temp.append(myavail)
                else:
                    car_pos = myavail[0]
                    start_time = myavail[1]
                    end_time = myavail[2]
                    
                    time_to_go = distance(car_pos, bestride.start_position)
                    min_time_at_start = start_time + time_to_go
                    #margin_at_start = bestride.earliest_departure - min_time_at_start
                    #if(margin_at_start > 50):
                    #    avail_time_1 = [car_pos, start_time, start_time + margin_at_start]
                    #    avail_temp.append(avail_time_1)

                    time_of_arrival = max(min_time_at_start, bestride.earliest_departure) + distance(bestride.start_position, bestride.end_position)
                    if(end_time - time_of_arrival > 5):
                        avail_time_2 = [bestride.end_position, time_of_arrival, end_time]
                        avail_temp.append(avail_time_2)
                        
                    mycar.available_times = avail_temp
            bestride, bestavail = best_ride_possible(mycar, ride_list, end, True)

    for mycar in car_list:  

        #print("finding the best rides for car number : "+str(k))
        #k = k +1
        
        bestride, bestavail = best_ride_possible(mycar, ride_list, end, False)
        while(bestride != None):
            mycar.courses.append(bestride)
            ride_temp = []
            for myride in ride_list:
                if (myride.number != bestride.number):
                    ride_temp.append(myride)
            ride_list = ride_temp
            
            avail_temp = []
            for myavail in mycar.available_times:
                if (myavail[0] != bestavail[0] or myavail[1] != bestavail[1] or myavail[2] != bestavail[2]):
                    avail_temp.append(myavail)
                else:
                    car_pos = myavail[0]
                    start_time = myavail[1]
                    end_time = myavail[2]
                    
                    time_to_go = distance(car_pos, bestride.start_position)
                    min_time_at_start = start_time + time_to_go
                    #margin_at_start = bestride.earliest_departure - min_time_at_start
                    #if(margin_at_start > 50):
                    #    avail_time_1 = [car_pos, start_time, start_time + margin_at_start]
                    #    avail_temp.append(avail_time_1)

                    time_of_arrival = max(min_time_at_start, bestride.earliest_departure) + distance(bestride.start_position, bestride.end_position)
                    if(end_time - time_of_arrival > 5):
                        avail_time_2 = [bestride.end_position, time_of_arrival, end_time]
                        avail_temp.append(avail_time_2)
                        
                    mycar.available_times = avail_temp
            bestride, bestavail = best_ride_possible(mycar, ride_list, end, False)        
                                
            
    
def nice_print(tab):    
    for row in tab:
        print(row)

def read_input(input_file):
    with open('input/' + input_file + '.in', "r") as f:
        
        values = f.readline().strip().split(' ')
        row_nb = int(values[0])
        col_nb = int(values[1])
        car_nb = int(values[2])
        ride_nb = int(values[3])
        bonus_nb = int(values[4])
        step_nb = int(values[5])

        ride_tab = []
        cpt = 0
        for line in f:
            values = line.strip().split(" ")
            start_pt = [int(values[0]), int(values[1])]
            end_pt = [int(values[2]), int(values[3])]
            earliest = int(values[4])
            latest = int(values[5])
            ride_tab.append([cpt, start_pt, end_pt, earliest, latest])
            cpt += 1

    return row_nb, col_nb, car_nb, ride_nb, bonus_nb, step_nb, ride_tab

def write_output(input_file, car_list):
    ride_number = 0
    early_rides = 0
    with open('output/' + input_file + '.out', 'w+') as f:
        for mycar in car_list:
            courses_list = sorted(mycar.courses, key=lambda ride:ride.earliest_departure)
            f.write(str(len(courses_list)))
            for mycourse in courses_list:    
                ride_number += 1
                if mycourse.isearly:
                    early_rides += 1
                f.write(' ' + str(mycourse.number))
                compute_score(mycourse)
            f.write('\n')
        #print("Number of rides takent into account: "+str(ride_number))
        #print("Number of early rides takent into account: "+str(early_rides))

def result(input_file):
    row_nb, col_nb, car_nb, ride_nb, bonus_nb, step_nb, ride_tab = read_input(input_file)
    global bonus
    bonus+=bonus_nb
    ride_per_car = round(ride_nb/car_nb)
    sorted_ride_tab = sorted(ride_tab, key = itemgetter(3))
    car_list = init_cars(car_nb, step_nb)
    ride_list = init_rides(sorted_ride_tab, step_nb)
    simulate_cars(step_nb, ride_list, car_list, ride_per_car)
    write_output(input_file, car_list)
   
def run_fifth_scenario():
    print("fifth scenario: high bonus")
    result("e_high_bonus")
    print("The score is: "+str(score)+" for the scenario e")
    return score
