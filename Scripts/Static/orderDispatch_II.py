# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 11:09:27 2020

Order dispatch optimization: High-Value Trips First(HVTF)

@author: Meilin Zhang
"""
from docplex.mp.model import Model
import numpy as py
import pandas as pd
import random
import numpy as np
import orderRealizationStats_HVTFMatches
import time


import sys
try:
    import docplex.mp
except:
    raise Exception('Please install docplex')


class OrderDispatch_II:
    def __init__(self):
        self.model = Model("HVTF Matches")

    def setup_model(self, scenario):
        # clears the model of all modeling objects.
        self.model.clear()

        self.distances = scenario['distanceMatrix']
        self.ID = scenario['ID']
        self.N = scenario['N']
        self.M = scenario['M']

        self.rider_range = range(1, self.N + 1)
        self.driver_range = range(1, self.N + 1)
        self.drivers_speed = scenario['driversSpeed']
        self.riders_wait = scenario['ridersWait']
        self.riders_reward = scenario['ridersReward']

        self.travel_speeds_lnCDF = scenario['travelSpeedLnCDF']
        self.riders_targetPickup = scenario['ridersTargetPickup']

        self.travel_range = range(1, len(self.travel_speeds_lnCDF) + 1)
        self.travel_speeds = scenario['travel_speeds']
        self.travel_bar = max(self.travel_speeds)

        #self.setup_variables()
        #self.setup_constraints()
        #self.setup_objective()

        self.scenario = scenario

        # 按订单价值排列订单list
        self.list1 = list(self.riders_reward.values())
        self.list1.sort(reverse=True)
        self.dict1 = {}
        for i in self.list1:
            for k in self.riders_reward:
                if i == self.riders_reward[k]:
                    self.dict1.setdefault(k, i)
        #print(self.dict1)

        #按订单价值对订单序号进行排列
        self.order_sort = list(self.dict1.keys())
        self.order_sort

        # 按订单价值进行司机匹配
        self.start = time.clock()
        
        self.a = []
        self.c = []
        for k in range(0, self.N):
            self.distance1 = {j: self.distances[self.order_sort[k], j] for j in range(1, self.M + 1)}
            self.distance1_value = list(self.distance1.values())
            self.distance1_value = np.array(self.distance1_value)
            self.min_index = np.argmin(self.distance1_value)
            self.b = np.argsort(self.distance1_value)
            self.g = self.min_index
            for j in range(len(self.b)):
                if self.g in self.a:
                    self.g = self.b[j + 1]
                else:
                    self.g = self.g
                    break
            self.a.append(self.g)
            self.c.append(self.g + 1)

        # 把匹配方案中司机的列表按照乘客1,2,3,....,N的顺序排列
        self.d = [0] * self.N
        for h in range(0, self.N):
            self.order_sort[h]
            self.d[self.order_sort[h] - 1] = self.c[h]
            
        self.end = time.clock()
        self.solution_time = self.end-self.start
        #print(self.d)

    #def make_solution_vector_2(self.d):
        #self.sol = [0] * self.N
        #self.sol = self.d
        #return self.sol

    #def make_rider_driver_dir_2(self.sol_vec):
        # sol_vec contains an array of drivers in rider order at slot i-1 we have rider(j)
        #return { self.sol_vec[i]: i+1 for i in range(self.N)}

    def solve(self):
        return orderRealizationStats_HVTFMatches.make_performance_stats(self)



