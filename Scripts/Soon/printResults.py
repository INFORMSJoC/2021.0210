# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 16:12:09 2020

Output the results into files

@author: Meilin Zhang
"""
import pandas as pd
from math import sqrt

def print_results(output_dir, dict_results):
    df_results = pd.DataFrame(dict_results, index = [0])
    df_results.to_csv(output_dir, mode = 'a', header=False)
    
    
# calculate the pick-up time for all rider driver assignments
def make_pickupTime_dict(opt_setting, rider_dict, driver_dict):
    time_dict = {}
    for i in opt_setting['orderDispatch_dict']:           
        time_dict[i] = opt_setting['orderPickupTime_dict'][i]
    return time_dict

# calculate the pick-up distance for all rider driver assignments
def make_pickupDistance_dict(opt_setting, rider_dict, driver_dict):
    pickupDistance_dict = {}
    for i in opt_setting['orderDispatch_dict']:
        pickupDistance_dict[i] = opt_setting['orderPickupDistance_dict'][i]                    
    return pickupDistance_dict

# calculate the order fulfillment status for all rider driver assignments
def make_total_order_fulfillment_dict(opt_setting, rider_dict, driver_dict):
    total_orderFulfillment_dict = {}
    for i in opt_setting['orderFulfill_dict']:
        j = opt_setting['orderFulfill_dict'][i]
        total_orderFulfillment_dict[i] = j
        
    return total_orderFulfillment_dict

def print_overall_performance(output_dir, setting, rider_dict, driver_dict):
    time_dict = make_pickupTime_dict(setting, rider_dict, driver_dict)
    pickupDistance_dict = make_pickupDistance_dict(setting, rider_dict, driver_dict)
    total_orderFulfillment_dict = make_total_order_fulfillment_dict(setting, rider_dict, driver_dict)
    
    # Calculate the average pick-up time
    if len(time_dict) > 0:
        avg_pickup_time = sum(time_dict.values())/len(time_dict)
    else:
        avg_pickup_time = 0
    
    # Calculate the average pick-up distance
    if len(pickupDistance_dict) > 0:
        avg_pickup_distance = sum(pickupDistance_dict.values())/len(pickupDistance_dict)
    else:
        avg_pickup_distance = 0
                

    #total order quantities
    total_order_quantities = 0
    for i in range(1, len(rider_dict)+1):
        if i in setting['riders']:
            total_order_quantities += 1
            
    
    #total input decision order quantities
    total_decision_order_quantities = 0
    for i in setting['riders']:
        if rider_dict[i][0] <= max(setting['orderDispatch_moment'].values()):
            total_decision_order_quantities += 1
            
             
    #total matched order quantities
    total_matched_order_quantities = len(setting['orderDispatch_dict'])

    #Calculate the total fulfill order quantities
    total_fulfill_order_quantities = 0
    for i in setting['orderDispatch_dict']:
        if setting['orderFulfill_dict'][i] == 1:
            total_fulfill_order_quantities += 1
    
    #print('orderDisptach_dict:'+str(setting['orderDisptach_dict']))
    # Calculate the order rewards of all orders
    total_orderValue = 0
    for i in range(1, len(rider_dict)+1):
        if i in setting['riders']:
            total_orderValue += rider_dict[i][3]
      

    #order value for decision orders   
    total_decision_orderValue = 0
    for i in range(1, len(rider_dict)+1): 
        if rider_dict[i][0] <= max(setting['orderDispatch_moment'].values()):
            total_decision_orderValue += rider_dict[i][3]
       
    # Calculate the order rewards all matched orders
    total_matched_orderValue = 0
    for i in setting['orderDispatch_dict'].keys():
        total_matched_orderValue += rider_dict[i][3]
    
    total_fulfillValue = 0
    for i in setting['orderDispatch_dict']:
        if setting['orderFulfill_dict'][i] == 1:
            total_fulfillValue += rider_dict[i][3]
    


    matched_order_fulfill_rate = sum(setting['orderFulfill_dict'].values())/total_matched_order_quantities
    decision_order_fulfill_rate = sum(setting['orderFulfill_dict'].values())/total_decision_order_quantities
    total_order_fulfill_rate = sum(setting['orderFulfill_dict'].values())/total_order_quantities


    ID = setting['ID']
    data_dir = output_dir + 'Model_'+ setting['model_type'] +'_Overall_Results.csv'
    
    
    print_results(data_dir, {'ID':ID,'total_order_quantities':total_order_quantities, 'total_matched_order_quantities':total_matched_order_quantities,
                             'total_fulfill_order_quantities':total_fulfill_order_quantities, 'avg_pickup_time': avg_pickup_time,
                             'avg_pickup_distance': avg_pickup_distance,'total_orderValue': total_orderValue, 
                             'total_decision_orderValue':total_decision_orderValue,
                             'total_matched_orderValue': total_matched_orderValue, 'total_fulfillValue': total_fulfillValue,
                             'matched_order_fulfill_rate': matched_order_fulfill_rate, 'decision_order_fulfill_rate':decision_order_fulfill_rate,
                             'total_order_fulfill_rate': total_order_fulfill_rate })
    
   

if __name__ == '__main__': 
    my_dict_1 = {'ID': 1, 'avg_time':3}
    my_dict_2 = {'ID': 2, 'avg_time':5}
    
    data_dir = "C:/Users/RDL/Desktop/20240504/T=60，乘客[1,10]分钟等待阈值/scenario 1.050/Test_Print_Results.csv"
    df_value_1 = pd.DataFrame(my_dict_1, index = [0])
    df_value_2 = pd.DataFrame(my_dict_2, index = [0])
    
    df_value_1.to_csv(data_dir, mode = 'a', header=False)
    df_value_2.to_csv(data_dir, mode = 'a', header=False)


