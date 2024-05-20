# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 12:40:27 2020

The main file for simultion process: evaluate order dispatch performance under various contexts

@author: Meilin Zhang
"""
# Import packages
import loadData, printResults
import orderDispatch_I, orderDispatch_II 
import orderDispatch_III_revised

N_simulations = 5000


if __name__ == '__main__':
    # Load the data
    data_dir = "C:/Users/RDL/Desktop/Static/" 
    dict_dataLoader = loadData.load_data(data_dir)
    
    list_parameters = dict_dataLoader['para'].to_dict('records')
    list_riders = dict_dataLoader['rider'].to_dict('records')
    list_drivers = dict_dataLoader['driver'].to_dict('records')
    
    # Init the Cplex Model
    model_1 = orderDispatch_I.OrderDispatch_I()
    model_2 = orderDispatch_II.OrderDispatch_II()
    model_3_revised = orderDispatch_III_revised.OrderDispatch_III_revised()

    
    i = 0
    for setting in list(zip(list_parameters, list_riders, list_drivers)):
        while i < N_simulations:    
            scenario = loadData.get_data_scenarios(setting)
            
            model_1.setup_model(scenario)
            model_2.setup_model(scenario)
            model_3_revised.setup_model(scenario)
            #model_4.setup_model(scenario)  
            
            dict_results_1 = model_1.solve()
            output_dir_1 = data_dir + 'Model_I_Results.csv'
            printResults.print_results(output_dir_1, dict_results_1)
            

            dict_results_2 = model_2.solve()
            output_dir_2 = data_dir + 'Model_II_Results.csv'
            printResults.print_results(output_dir_2, dict_results_2)

            if model_3_revised.solve():
                dict_results_3_revised = model_3_revised.solve()
            else:
                dict_results_3_revised = model_1.solve()
            output_dir_3_revised = data_dir + 'Model_III_revised_Results.csv'
            printResults.print_results(output_dir_3_revised, dict_results_3_revised)
            

            
            i+=1
            
            print("N_simulation="+str(i))
            

