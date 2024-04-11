# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 11:09:27 2020

Order realization and summary statistics

@author: Meilin Zhang
"""

# calculate the pick-up time for all rider driver assignments
def make_pickupTime_vector(distance_matrix, speeds, sol_vec):
    N_riders = len(sol_vec)
    time_vec = [0]* N_riders
    for i in range(N_riders):
        j = sol_vec[i]
        time_vec[i] = distance_matrix[i+1,j] * speeds[j]
    return time_vec

# calculate the pick-up distance for all rider driver assignments
def make_pickupDistance_vector(distance_matrix, sol_vec):
    N_riders = len(sol_vec)
    distance_vec = [0]* N_riders
    for i in range(N_riders):
        j = sol_vec[i]
        distance_vec[i] = distance_matrix[i+1,j]
    return distance_vec

# calculate the order fulfillment status for all rider driver assignments
def make_orderFulfill_vector(riders_wait, time_vec):
    N_riders = len(time_vec)
    orderFulfill_vec = [0]*N_riders
    for i in range(N_riders):
        if riders_wait[i+1] >= time_vec[i]:
            orderFulfill_vec[i] = 1
    return orderFulfill_vec

def make_solution_vector(model):
    sol = [0]* model.N
    for i in model.rider_range:
        for j in model.driver_range:
            if model.x[i,j].solution_value >= 0.5:
                sol[i-1] = j
                break
    return sol

def make_performance_stats(model):
    
    model.sol = make_solution_vector(model)

            
    time_vec = make_pickupTime_vector(model.distances, model.drivers_speed, model.sol)
    distance_vec = make_pickupDistance_vector(model.distances, model.sol)
    orderFulfill_vec = make_orderFulfill_vector(model.riders_wait, time_vec)
    
    # Calculate the average pick-up time
    avg_pickup_time = sum(time_vec)/len(time_vec)
    
    # Calculate the average pick-up distance
    avg_pickup_distance = sum(distance_vec)/len(distance_vec)
    
    # Calculate the order rewards
    total_orderValue = sum(model.riders_reward.values())
    total_fulfillValue = 0
    for i in range(len(model.riders_reward)):
        if orderFulfill_vec[i] == 1:
            total_fulfillValue += model.riders_reward[i+1]
    
    # Calculate the order fulfill rate
    order_fulfill_rate = sum(orderFulfill_vec) / len(orderFulfill_vec)
    
    revenue_rate = total_fulfillValue/total_orderValue
    
    solve_time = model.solution_time
    
    return {'ID': model.ID, 'avg_pickup_time': avg_pickup_time, 'avg_pickup_distance': avg_pickup_distance, 
            'total_orderValue': total_orderValue, 'total_fulfillValue': total_fulfillValue, 
            'order_fulfill_rate': order_fulfill_rate, 'revenue_rate':revenue_rate, 'solve_time':solve_time}
        
    

if __name__ == '__main__':
    # test function above
    print("* pickup time: ")
    print("* pickup distance:")
    print("* rider's wait threshold:")
    print("* order fulfill status:")