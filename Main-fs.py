#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 13:52:40 2017

@author: mario
"""

import numpy as np

import fs_MainOptimYpakaraiLakeTSPGAWithAlgaeImprovementRate3 as OptimGA
import fs_Algae_Sampled_grid_creator_project2 as AB_est
# import fs_CalculoCoberturaTemporal as AB_sampled
import parameters_opt_ga as param
#import parameters_fullstrategy as param2



####Initial Parameters Definition

strategy_phase = 0
fitness_function = 2
'''
Fitness Function Options
------------------------

1 - Death Penalty + Penalty Factor -- km2
2 - Penalty Factor -- coverage %
3 - Exponential Penalty Factor -- coverage %
4 - Penalty Factor -- size km2
5 - Penalty Factor -- ROI
6 -  Death Penalty
7 -  Death Penalty -- ROI variation
8 - Penalty Factor -- ROI variation   
'''
ab_size = 0
time_frames = 0 # number of time frames executed
arr_beacons = np.arange(60,dtype='uint8')
ab_conditions_coord = []


MAX_TIME_FRAMES = 2

OptimGA.print_parameters()

####Creacion de comportamiento dinamico de AB en max_time_frames

for idx in range(MAX_TIME_FRAMES):
    ab_conditions_coord.append(np.loadtxt('Data/ab_conditions2.csv', 
                                          dtype = 'uint8', delimiter =','))
   


#####Creacion de samp grid sin datos

samp_grid =  np.zeros((param.GRID_X_DIV,param.GRID_Y_DIV),
                            dtype = 'uint16') 

while time_frames < MAX_TIME_FRAMES:
    
#    samp_grid = np.loadtxt('', dtype = 'uint8', delimiter =',')

    print '\n'
    print 'TIME FRAME ', time_frames
    print '=============='
    
    
    print '------Find Route-AB Intersec Matrix'
    
    arr_routes_AB_est_intersec = AB_est.main(samp_grid) # Routes between 
                                                # beacons and Estimated 
                                                # (sampled) AB intersections
                                                # matrix
                                                # Used in intensification phase
    print '------ Genetic Algorithm'                                            
#    print arr_routes_AB_est_intersec
    
    best_indiv = OptimGA.main(fitness_function)
    
#==============================================================================
#     current_ab_cond_coord = ab_conditions_coord[time_frames]
#     
#     samp_grid = grid_measure.main(best_indiv, current_ab_cond_coord)
#     
#     if np.sump(samp_grid) != 0 and np.sum(samp_grid) > ab_size:
#         ab_size = np.sum(samp_grid)
#         fitness_function ==2
#         arr_subgroup = select_subgroup()
#         np.savetxt('', samp_grid, fmt = '%i', delimiter=",")
#         
#==============================================================================
    

 
    
    
    time_frames += 1


