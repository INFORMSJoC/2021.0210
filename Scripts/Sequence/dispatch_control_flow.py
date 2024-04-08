# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 23:19:04 2020

The control flow multi-periods simulation in order dispatch processing

@author: Meilin Zhang
"""
import orderDispatch_I,orderDispatch_III_revised
import printResults

def run_simulation(model_type, data_dir, scenario):
    # This is a discret-event driven simulation
    if model_type == 'I':
        model = orderDispatch_I.OrderDispatch_I()
    elif model_type == 'III_revised':
        model = orderDispatch_III_revised.OrderDispatch_III()

    
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
    
    opt_setting['match_time'] = 0 #the timestamp of order matching
    
    for k in range(1, len(arriving_list)+1):
        opt_setting['cur_time'] = arriving_list[k][3]#the arrival time of kth event
        if opt_setting['cur_time'] <= T:#"the arrival time of kth event" v.s. "T"
            # "the arrival time of kth event" v.s. "the timestamp of the batch matching of current period"
            if opt_setting['cur_time'] <= opt_setting['index_interval'] * OPT_Interval:
                if arriving_list[k][1] == 'Rider':
                    opt_setting['riders'][arriving_list[k][2]] = 1  # status code: 1 is pending, 0 is assigned, -1 is missed
                else:
                    opt_setting['drivers'][arriving_list[k][2]] = 1 # status code: 1 is pending, 0 is assigned, -1 is missed
            else:
                #To determine whether rider or driver is missed
                for i in opt_setting['riders']:
                    if opt_setting['index_interval'] * OPT_Interval >= rider_dict[i][0] + rider_dict[i][1]:
                        opt_setting['riders'][i] = -1
                        
                for j in opt_setting['drivers']:
                    if opt_setting['index_interval'] * OPT_Interval >= driver_dict[j][0] + driver_dict[j][3]:
                        opt_setting['drivers'][j] = -1
                #undate the timestamp of matching
                opt_setting['match_time'] = opt_setting['index_interval'] * OPT_Interval
                #Buildinng the batch matching model
                model.setup_model(opt_setting, rider_dict = rider_dict.copy(), driver_dict = driver_dict.copy())  
                dict_results = model.solve()
                output_dir = data_dir + 'Model_'+ model_type +'_Results.csv'
                printResults.print_results(output_dir, dict_results)
                #update to next period
                opt_setting['index_interval'] += 1 
                #Put the first event whose opt_setting['cur_time'] > opt_setting['index_interval'] * OPT_Interval to opt_setting['riders'] or opt_setting['drivers']
                if arriving_list[k][1] == 'Rider':
                    opt_setting['riders'][arriving_list[k][2]] = 1  # status code: 1 is pending, 0 is assigned, -1 is missed
                else:
                    opt_setting['drivers'][arriving_list[k][2]] = 1
                    
        continue  
    printResults.print_overall_performance(data_dir, opt_setting, rider_dict, driver_dict)
    

    
    
 
        
    
    
    
    
    
    
    
    
    
    