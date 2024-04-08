# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 11:09:27 2020

Order dispatch optimization: Maximize the joint target oriented probability

@author: Meilin Zhang
"""
import sys
import time


try:
    import docplex.mp
except:
    raise Exception('Please install docplex')   
    
from docplex.mp.model import Model
from docplex.mp.constants import ObjectiveSense
from docplex.util.environment import get_environment
import orderRealizationStats
import orderDispatch_I
    
class OrderDispatch_III_revised:
    def __init__(self):
        self.model = Model("Maximize the targets oriented probability")
        
    def setup_model(self, scenario):
        # clears the model of all modeling objects.
        self.model.clear()
        
        self.distances = scenario['distanceMatrix']
        self.ID = scenario['ID']
        self.N = scenario['N']
        self.M = scenario['M']
        
        self.rider_range = range(1, self.N+1)
        self.driver_range = range(1, self.N+1) 
        self.drivers_speed = scenario['driversSpeed']
        self.riders_wait = scenario['ridersWait']
        self.riders_reward = scenario['ridersReward']
        
        self.travel_speeds_lnCDF = scenario['travelSpeedLnCDF']
        self.weight_edge_lnCDF = scenario['weight_edge_lnCDF']
        self.riders_targetPickup = scenario['ridersTargetPickup']
        
        self.travel_range = range(1, len(self.travel_speeds_lnCDF)+1)
        self.travel_speeds = scenario['travel_speeds']
        self.travel_bar = max(self.travel_speeds)
        
        self.setup_variables()
        self.setup_constraints()
        self.setup_objective()
        
        self.scenario = scenario        
        
    def setup_variables(self):
        # decision variables of dispatching
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
        
        #self.model.maximize( self.model.sum(self.model.sum(self.x[i,j] * self.weight_edge_lnCDF[i,j] for i in self.rider_range) for j in self.driver_range) )
        
        self.model.total_probability = self.model.sum(self.model.sum(self.x[i,j] * self.weight_edge_lnCDF[i,j] for i in self.rider_range) for j in self.driver_range)
        self.model.total_pickup_distance = - self.model.sum( self.distances[i,j] * self.x[i,j] for i in self.rider_range for j in self.driver_range)
        self.model.add_kpi(self.model.total_probability,"Total Probability")
        self.model.add_kpi(self.model.total_pickup_distance,"Total Pickup Distance")
        self.model.maximize_static_lex([self.model.total_probability, self.model.total_pickup_distance])
      
        
        #self.start = time.clock()
    #return the results
    #def solve(self): 
        #if self.model.solve():
            #self.end = time.clock()
            #self.solution_time = self.end-self.start      
            #return orderRealizationStats.make_performance_stats(self)
        #else:
            #import orderDispatch_I
               
        self.start = time.clock()   
    def solve(self): # return the results
        if self.model.solve():
            self.end = time.clock()
            self.solution_time = self.end-self.start            
            return orderRealizationStats.make_performance_stats(self)