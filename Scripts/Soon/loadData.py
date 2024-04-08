# -*- coding: utf-8 -*-
"""
Created on Nov  25 12:21:26 2020
Prepare the data for multi-periods simulation input with Time Horizon T

@author: Meilin Zhang
"""
# Import packages
import pandas as pd
import numpy as np
import random

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
    
    scenario = {}
    
    scenario['ID'] = parameters['ID']
    scenario['T'] = parameters['T']
    scenario['mu_Driver'] = parameters['mu_Driver']
    scenario['mu_Rider'] = parameters['mu_Rider']
    scenario['OPT_Interval'] = parameters['OPT_Interval']
    
     # the coordinate system x, y range where x in [0, xmax], y in [0, ymax]
    scenario['o_xmax'] = parameters['X_axis_max']
    scenario['o_ymax'] = parameters['Y_axis_max']   
    
    scenario['travel_speeds'] = np.arange(driver_info['LB_minPerKm'], driver_info['UB_minPerKm']-0.1, -0.5).tolist() 
    scenario['delta_t'] = parameters['Delta_t']
    #scenario['distance_remain_max'] = 2*scenario['OPT_Interval']/driver_info['UB_minPerKm']
    scenario['distance_remain_max'] = scenario['delta_t']/driver_info['UB_minPerKm']
    scenario['delta_distance'] = 2 * scenario['delta_t']/(driver_info['LB_minPerKm'] + driver_info['UB_minPerKm'])

    setup_riders_info(scenario, rider_info, parameters) 
    setup_drivers_info(scenario, driver_info, parameters)
    setup_arriving_list(scenario)
          
    scenario['travel_speeds_lnCDF'] = np.log(np.arange(1, 0, -1/len(scenario['travel_speeds']))).tolist()
    scenario['travel_speeds_CDF'] = np.arange(1, 0, -1/len(scenario['travel_speeds'])).tolist()
    
    #print("scenario['travel_speeds_lnCDF']:",scenario['travel_speeds_lnCDF'])
    return scenario


def setup_riders_info(scenario, rider_info, parameters):
    #p = np.array([0.01, 0.01, 0.01, 0.01, 0.01, 0.05, 0.10, 0.10, 0.60, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01])
    wait_thresholds = np.arange(rider_info['LB_waiting'], rider_info['UB_waiting']+0.1, 0.5).tolist()
    # Setting p value, so the pth percentile of waiting derived from the waiting distribution
    # The generated targeted pick-up time for each rider
    alpha = parameters['Alpha']
    pi_p = np.percentile(wait_thresholds, float(100-parameters['Percentile'])) 
            
    order_rewards = range(rider_info['LB_reward'], rider_info['UB_reward'] + 2, 5)
   
    # Dictionary set for arriving riders
    rider_dict = {}
    temp_time_r = np.random.exponential(1.0/scenario['mu_Rider'], 1).item()#The interval of arrival time follows an exponential distribution
    i = 1
    while temp_time_r < scenario['T']:
        arrival_time = temp_time_r
        #rider_coords = (np.random.uniform() * scenario['o_xmax'], np.random.uniform() * scenario['o_ymax'])
        rider_coords = (np.random.uniform(1/4 * scenario['o_xmax'], 3/4 * scenario['o_xmax']), np.random.uniform(1/4 * scenario['o_ymax'], 3/4 * scenario['o_ymax']))
        #p = np.array([0.01, 0.01, 0.01, 0.02, 0.05, 0.05, 0.10, 0.15, 0.5, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01])
        rider_wait = random.sample(wait_thresholds, 1)[0]
        #rider_wait = np.random.choice(wait_thresholds, p= p.ravel())
        rider_reward = random.sample(order_rewards, 1)[0]
        #rider_targetPickup = pi_p * (random.sample(order_rewards, 1)[0])**alpha

        r_star = 12
        rider_targetPickup = pi_p * (r_star/rider_reward)**alpha
        
        rider_dict[i] = (arrival_time, rider_wait, rider_coords, rider_reward, rider_targetPickup)
        temp_time_r += np.random.exponential(1.0/scenario['mu_Rider'], 1).item() 
        i += 1     
    
    scenario['rider_dict'] = rider_dict
    #print('rider_dict:'+str(scenario['rider_dict']))


def setup_drivers_info(scenario, driver_info, parameters):           
    # Dictionary set for arriving drivers
    #p_1 = np.array([0.111, 0.111, 0.111, 0.111, 0.111, 0.111, 0.111, 0.111, 0.111, 0, 0, 0.001])
    p_1 = np.array([1/11, 1/11, 1/11, 1/11, 1/11, 1/11, 1/11, 1/11, 1/11, 1/11, 1/11])
    #p_1 = np.array([1/7, 1/7, 1/7, 1/7, 1/7, 1/7, 1/7])
    driver_wait = driver_info['Wait']
    driver_dict = {}
    temp_time_d = np.random.exponential(1.0/scenario['mu_Driver'], 1).item() 
    j = 1
    while temp_time_d < scenario['T']:
        arrival_time = temp_time_d
        driver_speed = np.random.choice(scenario['travel_speeds'], p=p_1.ravel())
        driver_coords = (np.random.uniform() * scenario['o_xmax'], np.random.uniform() * scenario['o_ymax'])
        #driver_distance_re = np.random.uniform() * scenario['distance_remain_max']
        driver_distance_re = np.random.uniform(-1, 1) * scenario['distance_remain_max']
        driver_dict[j] = (arrival_time, driver_speed, driver_coords, driver_wait, driver_distance_re)
        temp_time_d += np.random.exponential(1.0/scenario['mu_Driver'], 1).item() 
        j += 1
    
    scenario['driver_dict'] = driver_dict
    #print('driver_dict:'+str(scenario['driver_dict']))   

def setup_arriving_list(scenario):
    #arriving_list[index]={[index, 'Rider'or'Driver', 'pos_i'or'pos_j', 'arrival_time']}
    arriving_list = {} 
    pos_i = 1
    pos_j = 1
    index = 1
    while pos_i <= len(scenario['rider_dict']) or pos_j <= len(scenario['driver_dict']):
        if pos_j > len(scenario['driver_dict']):
            arriving_list[index]=(index, 'Rider', pos_i, scenario['rider_dict'][pos_i][0])
            pos_i += 1            
        elif pos_i > len(scenario['rider_dict']):
            arriving_list[index]=(index, 'Driver',pos_j, scenario['driver_dict'][pos_j][0])
            pos_j += 1 
        elif scenario['rider_dict'][pos_i][0] <= scenario['driver_dict'][pos_j][0]:
            arriving_list[index]=(index, 'Rider', pos_i, scenario['rider_dict'][pos_i][0])
            pos_i += 1
        else:
            arriving_list[index]=(index, 'Driver', pos_j, scenario['driver_dict'][pos_j][0])
            pos_j += 1          
        index += 1   
        
    scenario['arriving_list'] = arriving_list
    #print('arriving_list:'+str(scenario['arriving_list']))
    
if __name__ == '__main__':
    # test function "load_data"
    dict_dataLoader = load_data("C:/Users/RDL/Desktop/Forward-looking DynamicOrderDispatch/前瞻/scenario 2.800/")
    
    df_parameters = dict_dataLoader['para']
    df_riders = dict_dataLoader['rider']
    df_drivers = dict_dataLoader['driver']   
    
    print(df_parameters.iloc[0])
    print(type(df_parameters.iloc[0]))
    print(df_riders.head())
    print(df_drivers.head())
    print(df_parameters.head())