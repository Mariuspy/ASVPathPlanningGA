#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 13:52:40 2017

@author: mario
"""

import numpy as np

import fs_MainOptimYpakaraiLakeTSPGAWithAlgaeImprovementRate3 as OptimGA
import fs_Algae_Sampled_grid_creator_project2 as AB_est
import fs_CalculoCoberturaTemporal as AB_sampled
import parameters_opt_ga as param
#import parameters_fullstrategy as param2
import time

import csv


####Initial Parameters Definition

print '=====START MAIN ROUTINE=====' 
print time.ctime()

EXPERIMENT = 13
MAX_TIME_FRAMES = 3
GROUP_EST_SIZE = 5 # AB Squares separated by more than 5 squares form a 
                   # different AB group

FITNESS_FUNC_EXPL = 3
FITNESS_FUNC_INT = 5

PHASE_SIZE_THR = 0.75
EXPL_PH = 0
INT_PH = 1
HYB_PH = 2
'''
Fitness Function Options
------------------------

1 - Death Penalty + Penalty Factor -- km2
2 - Penalty Factor -- coverage %
3 - Exponential Penalty Factor -- coverage %
4 - Penalty Factor -- size km2
5 - Penalty Factor -- ROI exponential
6 -  Death Penalty -- ROI
7 -  Death Penalty -- coefficient of variation
8 - Penalty Factor -- coefficient of variation
9 - Penalty Factor -- ROI dstributed
'''

ab_flag = 0
ab_increase_flag = 0

strategy_phase = EXPL_PH

hybrid_count = 0

time_frames = 0 # number of time frames executed
arr_beacons = np.arange(60,dtype='uint8')
ab_conditions_coord = []
ab_groups = []
ab_groups_sizes = []
prev_ab_groups_sizes = []

                 
fitness_function = FITNESS_FUNC_EXPL

OptimGA.print_parameters() # Impresion de parametros del algoritmo genetico

####Creacion de comportamiento dinamico de AB en max_time_frames

for idx in range(MAX_TIME_FRAMES):
    ab_conditions_coord.append(np.loadtxt('Data/ab_conditions'+str(idx)+'_coord.csv', 
                                          dtype = 'uint8', delimiter =','))
   


#####Creacion de samp grid sin datos

samp_grid =  np.zeros((param.GRID_X_DIV,param.GRID_Y_DIV),
                            dtype = 'uint16')



arr_routes_AB_est_intersec= np.zeros((param.N_BEACON,param.N_BEACON),
                            dtype = 'uint16')

####Print parameters

print "MAIN PROGRAM PARAMETERS"

print 'Experiment No. = ', EXPERIMENT
print 'Max Time Frames = ', MAX_TIME_FRAMES
print 'Bloom Margin Distance (No. of Squares Side) =', GROUP_EST_SIZE
print 'Fitness Function Exploration =',FITNESS_FUNC_EXPL 
print 'Fitness Function Intensification =', FITNESS_FUNC_INT 


print '========================================================================'



while time_frames < MAX_TIME_FRAMES:
    
    real_AB = np.loadtxt('Data/ab_conditions'+str(time_frames)+'_pattern.csv', 
                         dtype = 'uint8', delimiter =',')

    print '\n'
    print 'TIME FRAME ', time_frames
    print '=============='
    
    
    
    
    if strategy_phase == EXPL_PH:
        print 'EXPLORATORY PHASE'
        print '------Reset Route-AB Intersec Matrix'
        print '\n'
        
        arr_routes_AB_est_intersec = np.zeros((param.N_BEACON,param.N_BEACON),
                            dtype = 'uint16')
        param.dict_routes_AB_est_intersec = {}
        
        best_indiv = OptimGA.main(fitness_function, arr_beacons, 
                                  arr_routes_AB_est_intersec, 
                                  param.dict_routes_AB_est_intersec) 
        
    else:
        print '-------Find Route-AB Intersec Matrix'
        arr_routes_AB_est_intersec, param.dict_routes_AB_est_intersec  = AB_est.main(samp_grid) # Routes between 
                                                # beacons and Estimated 
                                                # (sampled) AB intersections
                                                # matrix
        if strategy_phase == HYB_PH:
            print 'HYBRID PHASE'
            print '\n'
            
            best_indiv = OptimGA.main(fitness_function, arr_beacons, 
                                      arr_routes_AB_est_intersec, 
                                      param.dict_routes_AB_est_intersec)#REPLACE BY MOGA LATER!!
        
        else:
            print 'INTENSIFICATION PHASE'
            print '\n'
            
            best_indiv = OptimGA.main(fitness_function, arr_beacons, 
                                      arr_routes_AB_est_intersec, 
                                      param.dict_routes_AB_est_intersec)
             
            
            
        
    with open('Results/dict_exp'+str(EXPERIMENT)+'_'+str(time_frames)+'.csv', 'wb') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in param.dict_routes_AB_est_intersec.items():
            writer.writerow([key, value])
            
    np.savetxt('Results/arr_routes_AB_est_intersec_exp'+str(EXPERIMENT)+'_'+str(time_frames)+'.csv', 
               arr_routes_AB_est_intersec, fmt = '%i', delimiter=",")  
    
    np.savetxt('Results/best_indiv_exp'+str(EXPERIMENT)+'_'+str(time_frames)+'.csv', 
               best_indiv, fmt = '%i', delimiter=",") 
        
        
    
#==============================================================================
#     if ab_flag:
#         print 'INTENSIFICATION PHASE'
#         print '------Find Route-AB Intersec Matrix'
#         print '\n'
#         arr_routes_AB_est_intersec, dict_routes_AB_est_intersec  = AB_est.main(samp_grid) # Routes between 
#                                                 # beacons and Estimated 
#                                                 # (sampled) AB intersections
#                                                 # matrix
#         with open('Results/dict_exp'+str(EXPERIMENT)+str(time_frames)+'.csv', 'wb') as csv_file:
#             writer = csv.writer(csv_file)
#             for key, value in dict_routes_AB_est_intersec.items():
#                 writer.writerow([key, value])
#         
#     else:
#         print 'EXPLORATORY PHASE'
#         print '------Reset Route-AB Intersec Matrix'
#         print '\n'
#         arr_routes_AB_est_intersec = np.zeros((param.N_BEACON,param.N_BEACON),
#                             dtype = 'uint16')
#         dict_routes_AB_est_intersec = {}
# 
#     
#     np.savetxt('Results/arr_routes_AB_est_intersec_exp'+str(EXPERIMENT)+'_'+str(time_frames)+'.csv', 
#                arr_routes_AB_est_intersec, fmt = '%i', delimiter=",")    
#                                             # Used in intensification phase
#     print '------ Genetic Algorithm'                                            
# #    print arr_routes_AB_est_intersec
#     
#     best_indiv = OptimGA.main(
#             fitness_function, arr_beacons, arr_routes_AB_est_intersec, 
#             dict_routes_AB_est_intersec)
#     
#     np.savetxt('Results/best_indiv_exp'+str(EXPERIMENT)+'_'+str(time_frames)+'.csv', 
#                best_indiv, fmt = '%i', delimiter=",") 
#==============================================================================
    
    print '------ Path Execution and Sampling Evaluation'

    samp_grid = AB_sampled.main(best_indiv, ab_conditions_coord[time_frames])
    
    np.savetxt('Results/samp_grid_exp'+str(EXPERIMENT)+'_'+str(time_frames)+'.csv', samp_grid, 
               fmt = '%i', delimiter=",")
    
    for idx,element_x in enumerate(samp_grid):
        for idx2,element_y in enumerate(element_x):
#            print idx, idx2, element_y
            if element_y != 0:
                param.samp_pattern[idx][idx2]=1
#                print 'This'
                
    np.savetxt('Results/samp_pattern_exp'+str(EXPERIMENT)+'_'+str(time_frames)+'.csv', param.samp_pattern, 
               fmt = '%i', delimiter=",")          
    
    #   FIND SAMP COORDINATES
    #   SEPARATE IN GROUPS
    
    def find_samp_coord(samp_grid):
        "Halla las coordenadas de los cuadros con algas muestreados"
        samp_grid_coord = []
        for idx,element in enumerate(samp_grid):
            for idx2, element2 in enumerate(element):
                if element2:
                    samp_grid_coord.append([idx,idx2])
                    
        return samp_grid_coord
        
    
    samp_grid_coord = find_samp_coord(samp_grid)
    
    
#    print samp_grid_coord
    
    def find_ab_groups(samp_grid_coord):
        ab_groups = [[samp_grid_coord[0]]]
        ab_id = 0
        for idx2, elements in enumerate(samp_grid_coord):
            if idx2 > 0:
                diff_flag = 0
                for idx3,elements2 in enumerate(ab_groups[ab_id]):
#==============================================================================
#                     print 'Samp grid', elements 
#                     print 'AB groups', elements2, ab_groups
#                     print elements[0], elements2[0], elements[1],elements2[1]
#==============================================================================
                    if (abs(elements[0]-elements2[0]))< GROUP_EST_SIZE and (
                            abs(elements[1]-elements2[1]))<GROUP_EST_SIZE:
                        
                        ab_groups[ab_id].append(elements)
                        break
                    if idx3 == (len(ab_groups[ab_id])-1):
                        diff_flag = 1
                if diff_flag ==1:
                    ab_groups.append([elements])
                    ab_id += 1
#                        else:
#                            ab_groups.append(elements)
#                            idx += 1
#        print 'Len ab_groups', len(ab_groups)
        
        ab_groups_sizes = []
        
        for elements in ab_groups:
            ab_groups_sizes.append(len(elements))
        
        return ab_groups, ab_groups_sizes

    
                
#    print "AB groups", ab_groups
                    
    def select_beacons_subgroup(ab_groups):
        "Select a group of beacons based on the AB localization"
        subgroup_beacons = set()
        
        for idx,ab_elements in enumerate(ab_groups):
            
            ab_side = 0
            
            x_min, y_min = np.min(ab_elements, axis = 0)*param.GRID_SIZE
            
            x_max, y_max = np.max(ab_elements, axis = 0)*param.GRID_SIZE
            x_max += param.GRID_SIZE
            y_max += param.GRID_SIZE
            
            ab_side = y_max - y_min           
            
            for idx2,beacon_elements in enumerate(param.list_coord):
                
#                print beacon_elements
                
                if  y_min - ab_side <= int(beacon_elements[1]) <= y_max + ab_side:
                    subgroup_beacons.add(idx2)
                    
        return list(subgroup_beacons)     
                    
                    
    
    print 'Sum samp_grid', np.sum(samp_grid)
    print 'Non zero sampling', np.count_nonzero(samp_grid)
    print 'Non zero real AB', np.count_nonzero(real_AB)
    
    def ab_evaluation(samp_grid_loc, ab_groups_sizes_loc, prev_ab_groups_sizes_loc, 
                      arr_beacons_loc,ab_flag_loc,samp_grid_coord_loc, 
                          fitness_function_loc):
        "Evaluate the conditions of the AB and selects the next phase accordingly"
        
        global hybrid_count
        global strategy_phase
        
        ab_increase_flag_loc = 0
        ab_groups,ab_groups_sizes = find_ab_groups(samp_grid_coord_loc)
        
        if np.sum(samp_grid_loc) != 0:
            
            for idx in range(len(ab_groups_sizes)-len(prev_ab_groups_sizes_loc)):
                  prev_ab_groups_sizes_loc.append(0) # Para comparar listas con igual longitud
       
            print 'ab_groups size', ab_groups_sizes
            print 'prev_ab_groups_sizes', prev_ab_groups_sizes_loc
          
            for idx, ab_size in enumerate(ab_groups_sizes):
                print '== ab_size, prev_groups_sizes[idx]', ab_size, prev_ab_groups_sizes[idx]
            
                if ab_size>prev_ab_groups_sizes_loc[idx]:
                    
                    ab_increase_flag_loc = 1
                    break
            
            
            if ab_increase_flag_loc == 1:
                
                if strategy_phase == INT_PH:
                    print 'Remain in Intensification Phase'
                else:
                    print 'Moving to Intensification Phase'
                
                
                strategy_phase = INT_PH
                fitness_function_loc = FITNESS_FUNC_INT#Cambiar de posicion
                hybrid_count = 0
                
                print 'Before', arr_beacons_loc, len(arr_beacons_loc)
                arr_beacons_loc = np.array(select_beacons_subgroup(ab_groups))
                print 'After', arr_beacons_loc, len(arr_beacons_loc)

            else:
                if strategy_phase == HYB_PH:
                    print 'Remain in Hybrid Phase'
                else:
                    print 'Moving to Hybrid Phase'
                
                strategy_phase = HYB_PH
                fitness_function_loc = FITNESS_FUNC_INT
                hybrid_count += 1
                
                
                
#==============================================================================
#             ab_flag_loc == 1
#                             
#             for idx in range(len(ab_groups_sizes)-len(prev_ab_groups_sizes_loc)):
#                  prev_ab_groups_sizes_loc.append(0) # Para comparar listas con igual longitud
#       
#             print 'ab_groups size', ab_groups_sizes
#             print 'prev_ab_groups_sizes', prev_ab_groups_sizes_loc
#          
#             for idx, ab_size in enumerate(ab_groups_sizes):
#                  print 'ab_size, prev_groups_sizes[idx]', ab_size, prev_ab_groups_sizes[idx]
# 
#             
#             if ab_flag_loc == 0:
#                 print 'Moving to Intensification Phase'
#             else: 
#                 print 'Remain in Intensification Phase'
#                             
#             
#             
#             if ab_flag_loc == 0:
#                 
# 
#                 ab_increase_flag_loc = 1
#                     
#                 print 'Before', arr_beacons_loc, len(arr_beacons_loc)
#                 arr_beacons_loc = np.array(select_beacons_subgroup(ab_groups))
#                 fitness_function_loc = FITNESS_FUNC_INT
#                 print 'After', arr_beacons_loc, len(arr_beacons_loc)
#                 
#             else:
#                 print 'Remain in Intensification Phase'
#                        
#                 for idx in range(len(ab_groups_sizes)-len(prev_ab_groups_sizes_loc)):
#                     prev_ab_groups_sizes_loc.append(0) # Para comparar listas con igual longitud
#             
#                 print 'ab_groups size', ab_groups_sizes
#                 print 'prev_ab_groups_sizes', prev_ab_groups_sizes_loc
#             
#                 for idx, ab_size in enumerate(ab_groups_sizes):
#                     print 'ab_size, prev_groups_sizes[idx]', ab_size, prev_ab_groups_sizes[idx]
#                 
#                     if ab_size<=PHASE_SIZE_THR*prev_ab_groups_sizes_loc[idx]:
#                         
#                         print 'Moving to Exploratory Phase'
#                         ab_increase_flag_loc = 0
#                         fitness_function_loc = FITNESS_FUNC_EXPL 
#                         arr_beacons_loc = np.arange(60,dtype='uint8')                    
#              
#                         break # Evaluar
# 
# 
#                         
#                 print 'Remain in intensification Phase'
#                 ab_increase_flag_loc = 1
#                 fitness_function_loc = FITNESS_FUNC_INT
#                 
#                 print 'Before', arr_beacons_loc, len(arr_beacons_loc)
#                 arr_beacons_loc = np.array(select_beacons_subgroup(ab_groups))
#                 print 'After', arr_beacons_loc, len(arr_beacons_loc)
#==============================================================================
        else:
            if strategy_phase == EXPL_PH:
                print 'Remain in Exploratory Phase'
            else:
                print 'Moving to Exploratory Phase'
                    
            
            ab_flag_loc = 0
#            ab_increase_flag_loc = 0
            fitness_function_loc = FITNESS_FUNC_EXPL #Cambiar de POSICION!!
            arr_beacons_loc = np.arange(60,dtype='uint8')
        
        np.savetxt('Results/sub_group_beacons_exp'+str(EXPERIMENT)+'_'+str(time_frames)+'.csv', 
               arr_beacons_loc, fmt = '%i', delimiter=",") 
        
        
        prev_ab_groups_sizes_loc = ab_groups_sizes
        
        print 'Prev_ab_group_sizes', prev_ab_groups_sizes_loc, ab_groups_sizes
           
        
        return (ab_flag_loc,ab_increase_flag_loc, arr_beacons_loc, fitness_function_loc, 
                prev_ab_groups_sizes_loc)
        
    (ab_flag, ab_increase_flag, arr_beacons, fitness_function, 
        prev_ab_groups_sizes) = ab_evaluation(samp_grid, ab_groups_sizes, 
                                             prev_ab_groups_sizes, arr_beacons, 
                                                 ab_flag,samp_grid_coord,
                                                     fitness_function)
    
    
        
#     if np.sump(samp_grid) != 0 and np.sum(samp_grid) > ab_size:
#         ab_size = np.sum(samp_grid)
#         fitness_function ==2
#         arr_subgroup = select_subgroup()
#         np.savetxt('', samp_grid, fmt = '%i', delimiter=",")
#         
#============================================================================== 
    
    
    time_frames += 1
    
print '=====END MAIN ROUTINE====='
print time.ctime()

