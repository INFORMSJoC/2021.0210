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
    Delta_T = scenario['delta_t']
    Delta_Distance = scenario['delta_distance']
    arriving_list = scenario['arriving_list']
    rider_dict = scenario['rider_dict']
    driver_dict = scenario['driver_dict']
    T = scenario['T']
    
    opt_setting = {}
    opt_setting['rider_dict'] = rider_dict
    opt_setting['driver_dict'] = driver_dict
    opt_setting['T'] = T
    opt_setting['OPT_Interval'] = OPT_Interval
    opt_setting['Delta_T'] = Delta_T
    opt_setting['Delta_Distance'] = Delta_Distance
    opt_setting['model_type'] = model_type
    opt_setting['orderDispatch_dict'] = {}
    opt_setting['orderFulfill_dict'] = {}
    opt_setting['orderPickupDistance_dict'] = {}
    opt_setting['orderPickupTime_dict'] = {}
    opt_setting['orderDispatch_moment'] = {}
    
    opt_setting['ID'] = scenario['ID']
    
    opt_setting['travel_speeds'] = scenario['travel_speeds']
    opt_setting['travel_speeds_lnCDF'] = scenario['travel_speeds_lnCDF']
    opt_setting['travel_speeds_CDF'] = scenario['travel_speeds_CDF']
    
    opt_setting['cur_time'] = 0
    opt_setting['match_time'] = 0
    opt_setting['index_interval'] = 1
    opt_setting['riders'] = {}
    opt_setting['drivers'] = {}
    opt_setting['available_drivers'] = {}
    opt_setting['on_trip_drivers'] = {}
    opt_setting['waiting_riders'] = {}
    opt_setting['waiting_drivers'] = {}

    for k in range(1, len(arriving_list)+1):
        opt_setting['cur_time'] = arriving_list[k][3]
        if opt_setting['cur_time'] <= opt_setting['index_interval'] * opt_setting['OPT_Interval'] + opt_setting['Delta_T']:
        #if opt_setting['cur_time'] <= opt_setting['index_interval'] * opt_setting['OPT_Interval'] + 2*opt_setting['OPT_Interval']:
            if opt_setting['cur_time'] <= opt_setting['index_interval'] * opt_setting['OPT_Interval']:
                if arriving_list[k][1] == 'Rider':
                    opt_setting['riders'][arriving_list[k][2]] = 1
                else:
                    opt_setting['available_drivers'][arriving_list[k][2]] = 1
            else:
                if arriving_list[k][1] == 'Rider':
                    opt_setting['waiting_riders'][arriving_list[k][2]] = 1
                else:
                    if abs(driver_dict[arriving_list[k][2]][4]) <= opt_setting['Delta_Distance']:
                        opt_setting['on_trip_drivers'][arriving_list[k][2]] = 1
                    else:
                        opt_setting['waiting_drivers'][arriving_list[k][2]] = 1
        else:
            for i in opt_setting['riders']:
                if opt_setting['index_interval'] * opt_setting['OPT_Interval'] >= rider_dict[i][0] + rider_dict[i][1]:
                    opt_setting['riders'][i] = -1
                    
            for j in opt_setting['available_drivers']:
                if opt_setting['index_interval'] * opt_setting['OPT_Interval'] >= driver_dict[j][0] + driver_dict[j][3]:
                    opt_setting['available_drivers'][j] = -1
            

    
            opt_setting['match_time'] = opt_setting['index_interval'] * opt_setting['OPT_Interval']
            opt_setting['drivers'].update(opt_setting['available_drivers'])
            opt_setting['drivers'].update(opt_setting['on_trip_drivers'])
                
            model.setup_model(opt_setting, rider_dict = rider_dict.copy(), driver_dict = driver_dict.copy())
            dict_results = model.solve()
            output_dir = data_dir + 'Model_' + model_type + '_Results.csv'
            printResults.print_results(output_dir, dict_results)
        
            opt_setting['index_interval'] += 1
            opt_setting['updated_riders'] = {}        
            for i in opt_setting['waiting_riders'].keys():
                if rider_dict[i][0] <= opt_setting['index_interval'] * opt_setting['OPT_Interval']:
                    opt_setting['updated_riders'][i] = 1
            opt_setting['riders'].update(opt_setting['updated_riders'])
            
            for i in opt_setting['updated_riders'].keys():
                opt_setting['waiting_riders'].pop(i, None)
                
     
            for y in opt_setting['orderDispatch_dict'].values():
                if y in opt_setting['available_drivers']:
                    opt_setting['available_drivers'][y] = 0
                    opt_setting['drivers'][y] = 0
                elif y in opt_setting['on_trip_drivers']:
                    opt_setting['on_trip_drivers'][y] = 0
                    opt_setting['drivers'][y] = 0
                    
                    
            opt_setting['updated_ontrip_drivers'] = {}        
            for i in opt_setting['on_trip_drivers'].keys():
                if opt_setting['on_trip_drivers'][i] == 1:
                    if driver_dict[i][0] <= opt_setting['index_interval'] * opt_setting['OPT_Interval']:
                        opt_setting['updated_ontrip_drivers'][i] = 1
            opt_setting['available_drivers'].update(opt_setting['updated_ontrip_drivers'])
            
            for i in opt_setting['updated_ontrip_drivers'].keys():
                opt_setting['on_trip_drivers'].pop(i, None)  
                                
                
            opt_setting['updated_waiting_drivers'] = {}
            for i in opt_setting['waiting_drivers'].keys():
                if driver_dict[i][0] <= opt_setting['index_interval'] * OPT_Interval:
                    opt_setting['updated_waiting_drivers'][i] = 1
            opt_setting['available_drivers'].update(opt_setting['updated_waiting_drivers'])     

            for i in opt_setting['updated_waiting_drivers'].keys():
                opt_setting['waiting_drivers'].pop(i, None)
                    
            if arriving_list[k][1] == 'Rider':
                if arriving_list[k][3] <= opt_setting['index_interval'] * opt_setting['OPT_Interval']:
                    opt_setting['riders'][arriving_list[k][2]] = 1
                else:
                    opt_setting['waiting_riders'][arriving_list[k][2]] = 1
            else:
                if arriving_list[k][3] <= opt_setting['index_interval'] * opt_setting['OPT_Interval']:
                    opt_setting['available_drivers'][arriving_list[k][2]] = 1
                else:
                    if abs(driver_dict[arriving_list[k][2]][4]) <= opt_setting['Delta_Distance']:
                        opt_setting['on_trip_drivers'][arriving_list[k][2]] = 1
                    else:
                        opt_setting['waiting_drivers'][arriving_list[k][2]] = 1


    printResults.print_overall_performance(data_dir, opt_setting, rider_dict, driver_dict)
    
    
