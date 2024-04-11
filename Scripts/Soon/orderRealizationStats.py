# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 14:19:46 2020

Order realization and summary statistics

@author: Meilin Zhang
"""
import sys
from math import sqrt


# calculate the pick-up distance for all rider driver assignments
def make_pickupDistance_dict(model):
    pickupDistance_dict = {}
    for i in model.riders_set:
        if i in model.sol:
            if model.sol[i] >= 0.5:
                j = model.sol[i]
                if j in model.available_drivers_set:
                    pickupDistance_dict[i] = model.distances[i,j]
                elif j in model.on_trip_drivers_set:  
                    pickupDistance_dict[i] = model.distances[i,j]
                model.setting['orderPickupDistance_dict'][i] = pickupDistance_dict[i]

    return pickupDistance_dict

# calculate the pick-up time for all rider driver assignments
def make_pickupTime_dict(model):
    time_dict = {}
    for i in model.riders_set:
        if i in model.sol:
            if model.sol[i] >= 0.5:
                j = model.sol[i]
                if j in model.available_drivers_set:
                    time_dict[i] = model.distances[i,j] * model.driver_dict[j][1]
                elif j in model.on_trip_drivers_set:
                    time_dict[i] = model.distances[i,j] * model.driver_dict[j][1] + 0.5
                model.setting['orderPickupTime_dict'][i] = time_dict[i]
            
    return time_dict


# calculate the order fulfillment status for all rider driver assignments
def make_orderFulfill_dict(model):
    orderFulfill_dict = {}
    for i in model.riders_set:
        if i in model.sol:
            if model.sol[i] >= 0.5:
                j = model.sol[i]
                if j in model.available_drivers_set:
                    if model.setting['match_time'] + model.time_dict[i] <= model.rider_dict[i][0] + model.rider_dict[i][1]:
                        orderFulfill_dict[i] = 1
                        model.setting['orderFulfill_dict'][i] = 1
                    else:
                        orderFulfill_dict[i] = 0
                        model.setting['orderFulfill_dict'][i] = 0
                elif j in model.on_trip_drivers_set:
                   if model.setting['match_time'] + model.time_dict[i] <= model.rider_dict[i][0] + model.rider_dict[i][1]:
                        orderFulfill_dict[i] = 1
                        model.setting['orderFulfill_dict'][i] = 1
                   else:
                        orderFulfill_dict[i] = 0
                        model.setting['orderFulfill_dict'][i] = 0
            else:
                orderFulfill_dict[i] = 0
                model.setting['orderFulfill_dict'][i] = 0
                 
    return orderFulfill_dict

def make_solution_dict(model):
    sol = {}
    for i in model.riders_set:
        for j in model.drivers_set:
            if model.x[i,j].solution_value >= 0.5:
                sol[i] = j
                model.setting['orderDispatch_dict'][i] = j
                model.setting['orderDispatch_moment'][i] = model.setting['match_time']
                break            
    for i in model.riders_set:
        if i not in sol:
            sol[i] = 0
        
    return sol

def update_setting(model):
    # change the status code for all assigned pairs of rider and drivers
    for i in model.riders_set:
        if model.sol[i] >= 0.5:
            model.setting['riders'][i] = 0 
            j = model.sol[i]
            model.setting['drivers'][j] = 0
            if j in model.available_drivers_set:
                model.setting['available_drivers'][j] = 0
            elif j in model.on_trip_drivers_set:
                model.setting['on_trip_drivers'][j] = 0
                
def make_performance_stats(model):
    
    model.sol = make_solution_dict(model)
    
    update_setting(model)
            
    model.time_dict = make_pickupTime_dict(model)
    model.pickupDistance_dict = make_pickupDistance_dict(model)
    model.orderFulfill_dict = make_orderFulfill_dict(model)
    
    
    
    #print('orderDispatch_dict:', model.setting['orderDispatch_dict'])
    #print('orderDispatch_moment', model.setting['orderDispatch_moment'])
    #print('orderFulfill_dict', model.orderFulfill_dict)
    
    # Calculate the average pick-up time
    if len(model.time_dict) > 0:
        avg_pickup_time = sum(model.time_dict.values())/len(model.time_dict)
    else:
        avg_pickup_time = 0
    
    # Calculate the average pick-up distance
    if len(model.pickupDistance_dict) > 0:
        avg_pickup_distance = sum(model.pickupDistance_dict.values())/len(model.pickupDistance_dict)
    else:
        avg_pickup_distance = 0
    
    # Calculate the order rewards
    total_orderValue = 0
    for i in model.riders_set:
        total_orderValue += model.rider_dict[i][3]
    
    total_matched_orderValue = 0
    for i in model.riders_set:
        if i in model.sol:
            total_matched_orderValue += model.rider_dict[i][3]
    
    
    total_fulfillValue = 0
    for i in model.sol:
        if model.orderFulfill_dict[i] == 1:
            total_fulfillValue += model.rider_dict[i][3]

    
    # Calculate the order fulfill rate
    order_fulfill_rate = sum(model.orderFulfill_dict.values()) / len(model.orderFulfill_dict)
    
    return {'ID':model.ID,'avg_pickup_time': avg_pickup_time, 'avg_pickup_distance': avg_pickup_distance,
            'total_orderValue': total_orderValue, 'total_matched_orderValue':total_matched_orderValue,
            'total_fulfillValue': total_fulfillValue, 'order_fulfill_rate': order_fulfill_rate}
        
    

if __name__ == '__main__':
    # test function above
    print("* pickup time: ")
    print("* pickup distance:")
    print("* rider's wait threshold:")
    print("* order fulfill status:")