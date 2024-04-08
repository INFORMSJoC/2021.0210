# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 19:43:56 2021

@author: dlrong
"""


import orderDispatch_V
import printResults

def run_simulation(model_type, data_dir, scenario):
    # This is a discret-event driven simulation
    if model_type == 'V':
        model = orderDispatch_V.OrderDispatch_V()

        
    OPT_Interval = scenario['OPT_Interval']
    arriving_list = scenario['arriving_list']
    rider_dict = scenario['rider_dict']
    driver_dict = scenario['driver_dict']
    T = scenario['T']
    opt_setting = {}
    
    opt_setting['T'] = T
    opt_setting['OPT_Interval'] = OPT_Interval
    opt_setting['model_type'] = model_type
    opt_setting['orderDispatch_dict'] = {}
    opt_setting['orderFulfill_dict'] = {}
    opt_setting['orderPickupDistance_dict'] = {}
    opt_setting['orderPickupTime_dict'] = {}
    
    opt_setting['ID'] = scenario['ID']
    
    opt_setting['travel_speeds'] = scenario['travel_speeds']
    opt_setting['travel_speeds_lnCDF'] = scenario['travel_speeds_lnCDF']     
    opt_setting['travel_speeds_CDF'] = scenario['travel_speeds_CDF']
    
    opt_setting['cur_time'] = 0
    opt_setting['index_interval'] = 1
    opt_setting['riders'] = {}
    opt_setting['drivers'] = {}
    
    opt_setting['match_time'] = 0
    
    for k in range(1,len(arriving_list)+1):
        opt_setting['cur_time'] = arriving_list[k][3]
        if opt_setting['cur_time'] <= T - OPT_Interval:
            if arriving_list[k][1] == 'Rider':
                opt_setting['riders'][arriving_list[k][2]] = 1
            else:
                opt_setting['drivers'][arriving_list[k][2]] = 1
                
            opt_setting['match_time'] = opt_setting['cur_time']
              
            for i in opt_setting['riders']:
                if opt_setting['match_time'] >= rider_dict[i][0] + rider_dict[i][1]:
                    opt_setting['riders'][i] = -1
                    
            for j in opt_setting['drivers']:
                if opt_setting['match_time'] >= driver_dict[j][0] + driver_dict[j][3]:
                    opt_setting['drivers'][j] = -1
                    
            model.setup_model(opt_setting, rider_dict = rider_dict.copy(), driver_dict = driver_dict.copy())
            dict_results = model.solve()
            output_dir = data_dir + 'Model_'+ model_type +'_Results.csv'
            printResults.print_results(output_dir, dict_results)

    printResults.print_overall_performance(data_dir, opt_setting, rider_dict, driver_dict)   
    #print('riders:'+str(opt_setting['riders']))
    #print('Quantities_rides='+str(len(opt_setting['riders'])))
    #print('Quantities='+str(len(opt_setting['orderFulfill_dict'])))