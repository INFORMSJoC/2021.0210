# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 10:41:45 2020

Order dispatch optimization: minimize the total pick-up distance

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
    
class OrderDispatch_I:
    def __init__(self):
        self.model = Model("Minimize_TotalDistance")
        
    def setup_model(self, setting, rider_dict, driver_dict):
        # clears the model of all modeling objects.
        self.model.clear()
        
        self.model.rider_dict = rider_dict
        self.model.driver_dict = driver_dict
        self.model.setting = setting
        
        self.model.riders_set = set()
        self.model.drivers_set = set()
        self.model.available_drivers_set = set()
        self.model.on_trip_drivers_set = set()
        self.model.distances = {}  
        
        self.model.rider_consumed_time = {}
        for i in self.model.setting['riders']:
            if self.model.setting['riders'][i] == 1:
                self.model.rider_consumed_time[i] = self.model.setting['match_time'] - self.model.rider_dict[i][0]
                
        for i in self.model.setting['riders']:
            if self.model.setting['riders'][i] == 1:
                self.model.riders_set.add(i)
            
        
        if len(self.model.setting['available_drivers']) > 0:
            for i in self.model.setting['riders']:
                for j in self.model.setting['available_drivers']:
                    if self.model.setting['riders'][i] == 1 and self.model.setting['available_drivers'][j] == 1:
                        dx = self.model.rider_dict[i][2][0] - self.model.driver_dict[j][2][0]
                        dy = self.model.rider_dict[i][2][1] - self.model.driver_dict[j][2][1]
                        d2 = sqrt(dx*dx + dy*dy)
                        self.model.distances[i, j] = d2 
                        self.model.available_drivers_set.add(j)

        
        if len(self.model.setting['on_trip_drivers']) > 0:
            for i in self.model.setting['riders']:
                for j in self.model.setting['on_trip_drivers']:
                    if self.model.setting['riders'][i] == 1 and self.model.setting['on_trip_drivers'][j] == 1:
                        dx = self.model.rider_dict[i][2][0] - self.model.driver_dict[j][2][0]
                        dy = self.model.rider_dict[i][2][1] - self.model.driver_dict[j][2][1]
                        d2 = sqrt(dx*dx + dy*dy)
                        d_re = self.model.driver_dict[j][4]
                        self.model.distances[i, j] = d2 + d_re
                        self.model.on_trip_drivers_set.add(j)
                    
        #print("Distance:"+ str(self.model.distances))          
        #print("available_drivers_set:"+str(self.model.available_drivers_set))
        #print("on_trip_drivers_set:"+str(self.model.on_trip_drivers_set))
        self.model.drivers_set = self.model.available_drivers_set|self.model.on_trip_drivers_set
        
        #print("riders_set:"+str(self.model.riders_set))
        #print("drivers_set:"+str(self.model.drivers_set))
        #print("available_drivers_set:"+str(self.model.available_drivers_set))
        #print("on_trip_drivers_set:"+str(self.model.on_trip_drivers_set))


        self.model.ID = setting['ID']
        self.model.N = len(self.model.riders_set)
        self.model.M = len(self.model.available_drivers_set)
        self.model.B = len(self.model.on_trip_drivers_set)
        self.model.A = len(self.model.drivers_set)
        
        if self.model.N > 0 or self.model.A > 0:
            self.setup_variables()
            self.setup_constraints()
            self.setup_objective()
            
            self.model.sol = {}
        
    def setup_variables(self):
        # decision variables is a 2d-matrix
        self.model.x = self.model.binary_var_matrix(self.model.riders_set, self.model.drivers_set, lambda ij: "x_%d_%d" %(ij[0], ij[1]))    
        
    def setup_constraints(self):
        
        if len(self.model.riders_set) <= len(self.model.drivers_set):
            # one rider one driver
            self.model.add_constraints(self.model.sum(self.model.x[i,j] for j in self.model.drivers_set) == 1 for i in self.model.riders_set)
            self.model.add_constraints(self.model.sum(self.model.x[i,j] for i in self.model.riders_set) <= 1 for j in self.model.drivers_set)
        else:
            self.model.add_constraints(self.model.sum(self.model.x[i,j] for i in self.model.riders_set) == 1 for j in self.model.drivers_set)
            self.model.add_constraints(self.model.sum(self.model.x[i,j] for j in self.model.drivers_set) <= 1 for i in self.model.riders_set)
        
    def setup_objective(self):
        # minimize total displacement
        self.model.minimize( self.model.sum(self.model.distances[i,j] * self.model.x[i,j] 
                                            for i in self.model.riders_set for j in self.model.drivers_set) )
        
        

    def solve(self): # return the results
        if self.model.N > 0 or self.model.A > 0:
            assert self.model.solve(), "!!! Solve of the model fails"         
            return orderRealizationStats.make_performance_stats(self.model)
        else:
            return {}
    