# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 12:32:39 2020

Output the results into files

@author: Meilin Zhang
"""
import pandas as pd

def print_results(output_dir, dict_results):
    df_results = pd.DataFrame(dict_results, index = [0])
    df_results.to_csv(output_dir, mode = 'a', header=False)
    
    

if __name__ == '__main__': 
    my_dict_1 = {'ID': 1, 'avg_time':3}
    my_dict_2 = {'ID': 2, 'avg_time':5}
    
    data_dir = "C:/Users/RDL/Desktop/Static/Test_Print_Results.csv"
    df_value_1 = pd.DataFrame(my_dict_1, index = [0])
    df_value_2 = pd.DataFrame(my_dict_2, index = [0])
    
    df_value_1.to_csv(data_dir, mode = 'a', header=False)
    df_value_2.to_csv(data_dir, mode = 'a', header=False)
    
    #pd.DataFrame(my_dict_1).csv(data_dir, mode='a', index = False)
    