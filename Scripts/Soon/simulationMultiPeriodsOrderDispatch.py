 # -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 15:40:39 2020

The main file for simultion process: evaluate multi-periods order dispatch performance under various contexts

@author: Meilin Zhang
"""
# Import packages
import loadData, printResults
import dispatch_control_flow

N_simulations = 300


if __name__ == '__main__':
    # Load the data
    data_dir = "C:/Users/RDL/Desktop/20240504/T=60，乘客[1,10]分钟等待阈值/scenario 1.050/"
    dict_dataLoader = loadData.load_data(data_dir)
    
    list_parameters = dict_dataLoader['para'].to_dict('records')
    list_riders = dict_dataLoader['rider'].to_dict('records')
    list_drivers = dict_dataLoader['driver'].to_dict('records')
      
    for setting in list(zip(list_parameters, list_riders, list_drivers)):
        for i in range(0, N_simulations):    
            scenario = loadData.get_data_scenarios(setting)
            dispatch_control_flow.run_simulation("I", data_dir, scenario = scenario.copy())
                        
            dispatch_control_flow.run_simulation("III_revised", data_dir, scenario = scenario.copy())
            
            print("N_simulation="+str(i))


