# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 12:21:26 2020
Prepare the data for modeling input

@author: Meilin Zhang
"""
# Import packages
import pandas as pd
from math import sqrt
import random
import numpy as np

# return data parameters pandas dataframe
def load_data(data_dir): 
    # define the data file paths
    parameter_dir = data_dir + 'Parameters.csv'
    rider_dir = data_dir + 'Rider_Related.csv'
    driver_dir = data_dir + 'Driver_Related.csv'
    
    df_para = pd.read_csv(parameter_dir, sep =',', header = 0)
    df_rider = pd.read_csv(rider_dir, sep =',', header = 0)
    df_driver = pd.read_csv(driver_dir, sep =',', header = 0)
    
    return {'para': df_para, 'rider': df_rider, 'driver': df_driver}


# return the single simulation scenario, scenario
# arc: dict_setting is a tuple (pd.series, pd.series, pd.series)
def get_data_scenarios(dict_setting):
    parameters = dict_setting[0]
    rider_info = dict_setting[1]
    driver_info = dict_setting[2]
    
    ID = parameters['ID']
    N = parameters['N']
    M = parameters['M']

    # riders and drivers are indexed from 1 to N/M
    rider_range = range(1, N+1)
    #rider_range_I = range(1,int(N/2)+1)
    #rider_range_II = range(int(N/2)+1,N+1)
    
    driver_range = range(1, M+1) 
    #driver_range_I = range(1,int(M/2)+1)
    #driver_range_II = range(int(M/2)+1,M+1) 
    
     # the coordinate system x, y range where x in [0, xmax], y in [0, ymax]
    o_xmax = parameters['X_axis_max']
    o_ymax = parameters['Y_axis_max']   
    
    # driver's travelling speed set, e.g., minutes/km
    # travel_speeds = range(driver_info['LB_minPerKm'], driver_info['UB_minPerKm']-1, -1)
    travel_speeds = np.arange(driver_info['LB_minPerKm'], driver_info['UB_minPerKm']-0.1, -0.5).tolist()
    #travel_speeds.append(0.5)
    #print("travel_speeds:",travel_speeds)
    #print("driver_info['UB_minPerKm']:",driver_info['UB_minPerKm'])

    # riders' waiting threshold set
    # wait_thresholds = range(rider_info['LB_waiting'], rider_info['UB_waiting']+1, 1)
    wait_thresholds = np.arange(rider_info['LB_waiting'], rider_info['UB_waiting']+0.1, 0.5).tolist()
    
    # riders' order reward set
    order_rewards = range(rider_info['LB_reward'], rider_info['UB_reward'] + 1, 5) 
    
    # Define GLOBAL scenario parameters
    #riders_coords = {i: (random.random()*o_xmax, random.random()* o_ymax) for i in rider_range}
    riders_coords = {i:(random.uniform(1/4 * o_xmax, 3/4 * o_xmax), random.uniform(1/4 * o_ymax, 3/4 * o_ymax)) for i in rider_range}
    #riders_coords.update({i:(random.random()*o_xmax, random.random()* o_ymax) for i in rider_range_II})

    drivers_coords = {j: (random.random()*o_xmax, random.random()*o_ymax) for j in driver_range}
    #drivers_coords = {j: (random.uniform(0, 1/2 * o_xmax ), random.uniform(0, 1/2 * o_ymax)) for j in driver_range_I}
    #drivers_coords.update({j:(random.random()*o_xmax, random.random()* o_ymax) for j in driver_range_II})
    
    
    
    p = np.array([0.005, 0.005, 0.02, 0.04, 0.06, 0.08, 0.09, 0.10, 0.50, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01])
    #p = np.array([0.005, 0.005, 0.02, 0.03, 0.44, 0.03, 0.03, 0.03, 0.41])
    riders_wait = {i: np.random.choice(wait_thresholds, p = p.ravel())for i in rider_range}
    #riders_wait = {i: random.sample(wait_thresholds, 1)[0] for i in rider_range}
    #print("riders_wait:", riders_wait )
    

    #p_1 = np.array([0.045, 0.045, 0.10, 0.10, 0.30, 0.15, 0.10, 0.10, 0.05, 0.005, 0.005])
    #v\in[3,8]
    #p_1 = np.array([0.001, 0.001, 0.050, 0.150, 0.350, 0.150, 0.100, 0.100, 0.050, 0.024, 0.024])
    #drivers_speed = {j: np.random.choice(travel_speeds, p = p_1.ravel()) for j in driver_range}
    drivers_speed = {j: random.sample(travel_speeds, 1)[0] for j in driver_range}
    #print("drivers_speed:",drivers_speed)
    
    riders_reward = {i: random.sample(order_rewards, 1)[0] for i in rider_range} 
    #print("riders_reward:", riders_reward)
    
    # The mean of riders_reward
    #r_star = np.mean(list(riders_reward.values()))
    #r_star = np.median(list(riders_reward.values()))
    r_star = np.percentile(list(riders_reward.values()), 35)
    #print("r_star:",r_star)

    # The distance matrix from rider i to driver j
    distances = {}
    for i in rider_range:
        for j in driver_range:
            dx = riders_coords[i][0] - drivers_coords[j][0]
            dy = riders_coords[i][1] - drivers_coords[j][1]
            d2 = sqrt(dx*dx + dy*dy)
            distances[i, j] = d2
    #print("distances:",distances)

    # Setting p value, so the pth percentile of waiting derived from the waiting distribution
    # The generated targeted pick-up time for each rider
    alpha = parameters['Alpha']
    a = []
    for i in riders_wait.keys():
        a.append(riders_wait[i])       
    pi_p = np.percentile(a, float(100-parameters['Percentile'])) 
    #print("The value of pi_p = {}".format(pi_p))     


    riders_targetPickup = {i: pi_p * (r_star/riders_reward[i])**alpha for i in rider_range}
    #riders_targetPickup = {i: 5.5 * (r_star/riders_reward[i])**alpha for i in rider_range}
    #print("riders_targetPickup:", riders_targetPickup)
    
    
    riders_targetPickup_updated = riders_targetPickup   
    #print("riders_targetPickup__updated:", riders_targetPickup_updated)
    
    
    distances_min = {}
    for i in rider_range:
        distances_min[i] = 10000
        for j in driver_range:
            if distances[i,j] < distances_min[i]:
                distances_min[i] = distances[i,j]                
        if distances_min[i] * driver_info['UB_minPerKm'] >= riders_targetPickup_updated[i]:
            riders_targetPickup_updated[i] += 2
            
    #print("distances_min:", distances_min)
    #print("riders_targetPickup_updated:", riders_targetPickup_updated)
            
    
    
    
    # print(np.arange(1, 0, -1/len(travel_speeds)))
    
    travel_speeds_lnCDF = np.log(np.arange(1, 0, -1/len(travel_speeds))).tolist()
    travel_speeds_CDF = np.arange(1, 0, -1/len(travel_speeds)).tolist()
    
    
    #travel_speeds_CDF = [1.00, 0.955, 0.910, 0.810, 0.710, 0.410, 0.260, 0.160, 0.060, 0.010, 0.005]
    #travel_speeds_lnCDF = [0, -0.046, -0.094, -0.211, -0.342, -0.892, -1.347, -1.833, -2.813, -4.605, -5.298]
    
    
    # F_[3,8] & LnF_{3,8}
    #travel_speeds_CDF = [1.00, 0.999, 0.998, 0.948, 0.798, 0.448, 0.298, 0.198, 0.098, 0.048, 0.024]
    #travel_speeds_lnCDF = [0, -0.001, -0.002, -0.053, -0.226, -0.803, -1.211, -1.619, -2.323, -3.037, -3.730]
    def return_position(arr, val):
        i = 0
        while i < len(arr) and arr[i] > val:
            i += 1
        return i

    # define the new model's lnF(tau_i/s_ij)
    LARGE_NEG = -10000
    weight_edge_lnCDF = {}
    for i in rider_range:
        for j in driver_range:
            val = riders_targetPickup_updated [i]/distances[i,j]
            #print(val)
            position = len(travel_speeds) - return_position(travel_speeds, val)
            #print(position)
            index = len(travel_speeds)-position
            if index < len(travel_speeds):
                weight_edge_lnCDF[i,j] = travel_speeds_lnCDF[index]
            else:
                weight_edge_lnCDF[i,j] = LARGE_NEG
            #print(weight_edge_lnCDF[i,j])
    
    return {'ID': ID, 'N': N, 'M': M, 'distanceMatrix': distances, 'travel_speeds': travel_speeds,
            'ridersWait': riders_wait, 'driversSpeed': drivers_speed, 'ridersReward': riders_reward,
            'ridersTargetPickup': riders_targetPickup, 'travelSpeedLnCDF': travel_speeds_lnCDF,
            'travelSpeedCDF': travel_speeds_CDF, 'weight_edge_lnCDF': weight_edge_lnCDF, 
            'drivers_speed':drivers_speed}

           
if __name__ == '__main__':
    # test function "load_data"
    dict_dataLoader = load_data("C:/Users/18640/Desktop/组会文件/第一篇论文第三轮修改/New simulation/Table 1/")
    
    df_parameters = dict_dataLoader['para']
    df_riders = dict_dataLoader['rider']
    df_drivers = dict_dataLoader['driver']   
    
    print(df_parameters.iloc[0]['N'])
    print(type(df_parameters.iloc[0]))
    print(df_riders.head())
    print(df_drivers.head())
    print(df_parameters.head())