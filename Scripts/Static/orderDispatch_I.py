# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 11:09:27 2020

Order dispatch optimization: Minimizing Total Pickup Distance (MTPD)

@author: Meilin Zhang
"""
import sys
import time

try:
    import docplex.mp
except:
    raise Exception('Please install docplex')   
    
from docplex.mp.model import Model
import orderRealizationStats
    
class OrderDispatch_I:
    def __init__(self):
        self.model = Model("Minimize_TotalDistance")
        
    def setup_model(self, scenario):
        # clears the model of all modeling objects.
        self.model.clear()
        
        self.distances = scenario['distanceMatrix']
        self.ID = scenario['ID']
        self.N = scenario['N']
        self.M = scenario['M']
        
        self.rider_range = range(1, self.N+1)
        self.driver_range = range(1, self.M+1) 
        self.drivers_speed = scenario['driversSpeed']
        self.riders_wait = scenario['ridersWait']
        self.riders_reward = scenario['ridersReward']
        
        self.setup_variables()
        self.setup_constraints()
        self.setup_objective()
        
    def setup_variables(self):
        # decision variables is a 2d-matrix
        self.x = self.model.binary_var_matrix(self.rider_range, self.driver_range, lambda ij: "x_%d_%d" %(ij[0], ij[1]))    
        
    def setup_constraints(self):
        # one rider one driver
        #self.model.add_constraints(self.model.sum(self.x[i,j] for j in self.driver_range) == 1 for i in self.rider_range)
        #self.model.add_constraints(self.model.sum(self.x[i,j] for i in self.rider_range) == 1 for j in self.driver_range)
        if self.N > self.M:
            self.model.add_constraints(self.model.sum(self.x[i,j] for j in self.driver_range) <= 1 for i in self.rider_range)
            self.model.add_constraints(self.model.sum(self.x[i,j] for i in self.rider_range) == 1 for j in self.driver_range)
        elif self.N == self.M:
            self.model.add_constraints(self.model.sum(self.x[i,j] for j in self.driver_range) == 1 for i in self.rider_range)
            self.model.add_constraints(self.model.sum(self.x[i,j] for i in self.rider_range) == 1 for j in self.driver_range)
        else:
            self.model.add_constraints(self.model.sum(self.x[i,j] for j in self.driver_range) == 1 for i in self.rider_range)
            self.model.add_constraints(self.model.sum(self.x[i,j] for i in self.rider_range) <= 1 for j in self.driver_range)
        
        
    def setup_objective(self):
        # minimize total displacement
        self.model.minimize( self.model.sum(self.distances[i,j] * self.x[i,j] 
                                            for i in self.rider_range for j in self.driver_range) )
  
        self.start = time.clock()
    def solve(self): # return the results
        assert self.model.solve(), "!!! Solve of the model fails"
        self.end = time.clock()
        self.solution_time = self.end-self.start        
        return orderRealizationStats.make_performance_stats(self)


        
        
        
        
    
    