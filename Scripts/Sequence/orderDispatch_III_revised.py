# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 17:58:05 2020

Order dispatch optimization: Satisficing Approach(SA)
(Maximize the joint target oriented probability)

@author: Meilin Zhang
"""
import sys
from math import sqrt
try:
    import docplex.mp
except:
    raise Exception('Please install docplex')   
    
from docplex.mp.model import Model
import orderRealizationStats
import orderDispatch_I
    
class OrderDispatch_III:
    def __init__(self):
        self.model = Model("Maximize the targets oriented probability")
        
    def setup_model(self, setting, rider_dict, driver_dict):
        # clears the model of all modeling objects.
        self.model.clear()
        
        self.model.rider_dict = rider_dict
        self.model.driver_dict = driver_dict
        self.model.setting = setting

        self.model.riders_set = set()
        self.model.drivers_set = set()
        self.model.distances = {}
        for i in setting['riders']:
            for j in setting['drivers']:
                if setting['riders'][i] == 1 and setting['drivers'][j] == 1:
                    dx = rider_dict[i][2][0] - driver_dict[j][2][0]
                    dy = rider_dict[i][2][1] - driver_dict[j][2][1]
                    d2 = sqrt(dx*dx + dy*dy)
                    self.model.distances[i, j] = d2 
                    self.model.riders_set.add(i)
                    self.model.drivers_set.add(j)
        
        self.model.ID = setting['ID']
        self.model.N = len(self.model.riders_set)
        self.model.M = len(self.model.drivers_set)         
        
        self.riders_targetPickup_updated = {}        
        for i in self.model.riders_set:
            self.riders_targetPickup_updated[i] = self.model.rider_dict[i][4]
            
            
        distances_min = {}
        for i in self.model.riders_set:
            distances_min[i] = 10000
            for j in self.model.drivers_set:
                if self.model.distances[i,j] < distances_min[i]:
                    distances_min[i] = self.model.distances[i,j]                
            if distances_min[i] * 1 >= self.riders_targetPickup_updated[i]:
                 self.riders_targetPickup_updated[i] += 2
                
        
        if self.model.N > 0 or self.model.M > 0:
            self.travel_speeds_lnCDF = setting['travel_speeds_lnCDF']
            
            self.travel_range = range(1, len(self.travel_speeds_lnCDF)+1)
            self.travel_speeds = setting['travel_speeds']
            self.travel_bar = max(self.travel_speeds)

            def return_position(arr, val):
                i = 0
                while i < len(arr) and arr[i] > val:
                    i += 1
                return i

            LARGE_NEG = -10000
            self.weight_edge_lnCDF = {}
            for i in self.model.riders_set:
                for j in self.model.drivers_set:
                    val = (self.riders_targetPickup_updated[i] - (self.model.setting['match_time'] - self.model.rider_dict[i][0])) / self.model.distances[i, j]
                    #val = self.riders_targetPickup_updated[i] / self.model.distances[i, j]
                    # print(val)
                    position = len(self.travel_speeds) - return_position(self.travel_speeds, val)
                    # print(position)
                    index = len(self.travel_speeds) - position
                    if index < len(self.travel_speeds):
                        self.weight_edge_lnCDF[i, j] = self.travel_speeds_lnCDF[index]
                    else:
                        self.weight_edge_lnCDF[i, j] = LARGE_NEG

            self.setup_variables()
            self.setup_constraints()
            self.setup_objective()
            
            self.model.sol = {}
        
    def setup_variables(self):
        # decision variables of dispatching
        self.model.x = self.model.binary_var_matrix(self.model.riders_set, self.model.drivers_set, lambda ij: "x_%d_%d" %(ij[0], ij[1]))

    def setup_constraints(self):
        # one rider one driver
        if len(self.model.riders_set) <= len(self.model.drivers_set):
            # one rider one driver
            self.model.add_constraints(self.model.sum(self.model.x[i,j] for j in self.model.drivers_set) == 1 for i in self.model.riders_set)
            self.model.add_constraints(self.model.sum(self.model.x[i,j] for i in self.model.riders_set) <= 1 for j in self.model.drivers_set)
        else:
            self.model.add_constraints(self.model.sum(self.model.x[i,j] for i in self.model.riders_set) == 1 for j in self.model.drivers_set)
            self.model.add_constraints(self.model.sum(self.model.x[i,j] for j in self.model.drivers_set) <= 1 for i in self.model.riders_set)

    def setup_objective(self):
                
        joint_probability = self.model.sum(self.model.x[i,j] * self.weight_edge_lnCDF[i,j] for i in self.model.riders_set for j in self.model.drivers_set)
        total_pickupDistance = self.model.sum(self.model.distances[i,j] * self.model.x[i,j] *(-1.0) for i in self.model.riders_set for j in self.model.drivers_set) 
                
        # maximize the joint probability
        #self.model.maximize(joint_probability)
        self.model.maximize_static_lex([joint_probability, total_pickupDistance])

    # return the results
    def solve(self): 
        if self.model.N > 0 or self.model.M > 0:
            try:
                assert self.model.solve(), "!!! Solve of the model fails"
            except AssertionError:
                model_temp = orderDispatch_I.OrderDispatch_I()
                model_temp.setup_model(self.model.setting, self.model.rider_dict, self.model.driver_dict) 
                return model_temp.solve()
            else:
                return orderRealizationStats.make_performance_stats(self.model)
        else:
            return {}
