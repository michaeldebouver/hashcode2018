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
    """A simple example class"""

    def __init__(self, end):

        self.courses=[]
        self.remainingsteps=None
        self.available_times = []
        self.available_times.append(availability([0,0],0,end))
        
class availability:
    """A simple example class"""

    def __init__(self, pos, start, end):

        self.pos=pos
        self.start=start
        self.end=end

class ride:
    done = False
    def __init__(self,number,start_position,end_position,earliest_departure,latest_arrival):
        self.number=number
        self.start_position=start_position
        self.end_position=end_position
        self.earliest_departure=earliest_departure
        self.latest_arrival=latest_arrival
        self.isearly = False
        self.time_of_actual_start = 0
        self.time_of_actual_arrival = 0
        self.duration = distance(end_position, start_position)

def init_cars(car_nb, end):
    cars = []
    for i in range(car_nb):
        cars.append(car(end))
    return cars

def init_rides(ride_list):
    rides = []
    ride_possible = 0
    early_rides_possible = 0
    sum_dist = 0
    av_pos_x = 0
    av_pos_y = 0
    for r in ride_list:
        distance_init = distance(r[1], r[2])
        if(distance_init <= r[4] - r[3]):
            sum_dist += distance_init
            av_pos_x += r[1][0]
            av_pos_y += r[1][1]
            rides.append(ride(r[0], r[1], r[2], r[3], r[4]))
            ride_possible+=1
            
            if distance([0,0], r[1]) - r[3] < 0:
                early_rides_possible += 1          
                
    av = round(sum_dist / len(ride_list))  
    av_pos_x = round(av_pos_x / len(ride_list))
    av_pos_y = round(av_pos_y / len(ride_list))       
    #print("nb rides total : "+ str(len(ride_list)))
    #print("nb rides possible : "+ str(ride_possible))
    #print("nb rides early possible : "+ str(early_rides_possible))
    #print("average of distance for each ride : "+str(av))
    #print("average position of start : "+str(av_pos_x)+","+str(av_pos_y))
    return rides, av, [av_pos_x, av_pos_y]



def best_ride_possible(mycar, ridelist, end, is_earliest, av, av_pos):
    
    bestride = None
    mintime = 10000000000
    bestavail = None
    no_better_cpt = 0
    is_early = False
    for myride in ridelist:
        myride.isearly = False
        
        for avail_time in mycar.available_times:
               
            car_pos = avail_time.pos
            start_time = avail_time.start
            end_time = avail_time.end
            
            ride_start = myride.earliest_departure
            ride_duration = distance(myride.start_position, myride.end_position)
            time_to_arrive_start = distance(car_pos, myride.start_position)
            time_at_start = start_time + time_to_arrive_start
            better_start = max(ride_start, time_at_start)
            if(time_at_start < myride.earliest_departure):
                ride_duration += bonus
                myride.isearly = True
            
            
            time_at_arrival = max(ride_start, time_at_start) + ride_duration
            if(time_at_arrival > end or time_at_arrival > myride.latest_arrival or time_at_arrival > end_time):
                continue
            
            
            
            #score = time_at_arrival + log(1+time_to_arrive_start)
            distance_from_average = distance(myride.end_position, av_pos)
            
            if avail_time.start <= 0.80 * end:
                score = better_start + ( distance_from_average + ride_duration ) * 0.01
            else:
                score = better_start + (ride_duration) * 0.03
            
            if score < mintime:
                mintime = score
                bestavail = avail_time
                bestride = myride
                bestride.isearly = is_early
            else:
                no_better_cpt = no_better_cpt + 1
        if(no_better_cpt > 50 and is_earliest ):
            break
                
    return bestride, bestavail

def distance(start, end):
    return abs(end[0] - start[0]) + abs(end[1] - start[1])


def simulate_cars(end, ride_list, car_list, cpt, av, av_pos):
        
    car_temp = []   
    while len(car_list) > 0:
        print("number of remaining cars: "+str(len(car_list)))
        print("number of remaining rides: "+str(len(ride_list)))
        
            
        for mycar in car_list:
            bestride, bestavail = best_ride_possible(mycar, ride_list, end, False, av, av_pos)
            if(bestride == None):
                car_list.remove(mycar)
                car_temp.append(mycar)
            else:   
                mycar.courses.append(bestride)
                ride_temp = []
                for myride in ride_list:
                    if (myride.number != bestride.number):
                        ride_temp.append(myride)
                ride_list = ride_temp
                
                avail_temp = []
                for myavail in mycar.available_times:
                    if (myavail.pos != bestavail.pos or myavail.start != bestavail.start or myavail.end != bestavail.end):
                        avail_temp.append(myavail)
                    else:
                        car_pos = myavail.pos
                        start_time = myavail.start
                        end_time = myavail.end
                        
                        time_to_go = distance(car_pos, bestride.start_position)
                        min_time_at_start = start_time + time_to_go
                        margin_at_start = bestride.earliest_departure - min_time_at_start
                        if(margin_at_start > 5):
                            avail_temp.append(availability(car_pos,start_time, start_time + margin_at_start))

    
                        time_of_arrival = max(min_time_at_start, bestride.earliest_departure) + distance(bestride.start_position, bestride.end_position)
                        if(end_time - time_of_arrival > 5):
                            avail_temp.append(availability(bestride.end_position, time_of_arrival, end_time))
                            
                        mycar.available_times = avail_temp
                        
                                
    return ride_list, car_temp
        
    
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
            ride_tab.append([cpt, start_pt, end_pt, earliest, latest, distance(end_pt, start_pt)])
            cpt += 1

    return row_nb, col_nb, car_nb, ride_nb, bonus_nb, step_nb, ride_tab

def write_output(input_file, car_list):
    cpt = 0
    with open('output/' + input_file + '.out', 'w+') as f:
        for mycar in car_list:
            courses_list = mycar.courses
            f.write(str(len(courses_list)))
            for mycourse in courses_list:
                cpt = cpt + 1
                f.write(' ' + str(mycourse.number))
                compute_score(mycourse)
            f.write('\n')
    print("nb courses prises en compte : " + str(cpt))
    print("mon score est de : "+ str(score))

def result(input_file):
    global bonus
    row_nb, col_nb, car_nb, ride_nb, bonus_nb, step_nb, ride_tab = read_input(input_file)
    bonus += bonus_nb
    ride_per_car = round(ride_nb/car_nb)
    sorted_ride_tab = sorted(ride_tab, key = itemgetter(3))
    car_list = init_cars(car_nb, step_nb)
    ride_list, av, av_pos = init_rides(sorted_ride_tab)
    ride_list, car_list = simulate_cars(step_nb, ride_list, car_list, ride_per_car, av, av_pos)
    write_output(input_file, car_list)
    
def run_fourth_scenario():
    print("fourth scenario: metropolis")
    result("d_metropolis")
    print("The score is: "+str(score)+" for the scenario d")
    return score
