#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 10:14:34 2017

@author: mario
"""
import numpy as np
import csv

#==============================================================================
# # PARAMETROS
#==============================================================================

#INPUT1 = 'arr_alg_pattern_size5.csv'
INPUT2 = 'sampled_grid_event_tracking.csv'
INPUT3 = 'combination.csv'
INPUT4 = 'ListaCoordenadasConvRefMetros3.csv'
INPUT5 = 'intersection_routes.csv'
INPUT6 = 'best_last_pop.csv'
INPUT7 = 'sampled_grid_event_tracking2.csv'

OUTPUT1 = 'best_indiv_test_ngen100_sim1.csv'
OUTPUT2 = 'improve_rate_ngen100_sim1.csv'
OUTPUT3 = 'ImproveRate_Solution_ngen100_sim1.png'
OUTPUT4 = 'Best_Solution_ngen100_sim1.csv'
OUTPUT5 = 'best_last_pop2.csv'

N_BEACON = 60 
N_SIM = 3
CXPB = 0.8
MUTPB =  0.2
NGEN = 1000
POPU = 100
ELIT_RATE = 0.2 
FRANJA = 20
ATT_FACTOR = 1000 # Intentos para encontrar siguiente baliza en poblacion inicial valida
ATT_POPU = 100000 # Intentos para encontrar una poblacion inicial validad  de POPU individuos
LAKE_SIZE = 68720000

LAKE_SIZE_X = 12000
LAKE_SIZE_Y = 14000

GRID_SIZE = 200 # metros
GRID_X_DIV = LAKE_SIZE_X/GRID_SIZE # numero de cuadros sobre el eje x
GRID_Y_DIV = LAKE_SIZE_Y/GRID_SIZE # numero de cuadros sobre el eje y

FIT_FUNC_TYPE = 1
'''
1 - Death Penalty + Penalty Factor - km2
2 - Penalty Factor - coverage %
3 - Exponential Penalty Factor - coverage %
4 - Penalty Factor - size km2
5 - Penalty Factor - ROI
6-  Death Penalty
'''

#==============================================================================
# # CONSTANTES
#==============================================================================

arr_sampled_grid_pattern = np.loadtxt(INPUT2, dtype = 'uint8', 
                                      delimiter =',')

###############################################################################

arr_reg1= np.loadtxt('reg1_ev_track.csv' ,dtype = 'uint8', delimiter =',')
arr_reg2= np.loadtxt('reg2_ev_track.csv' ,dtype = 'uint8', delimiter =',')


arr_subgroup = np.concatenate((arr_reg1,arr_reg2))

###############################################################################

arr_allowed_routes = np.loadtxt(INPUT3,dtype = 'uint8',delimiter =',' )

###############################################################################

lst_centers = []
for x in range(GRID_X_DIV):
    sublst_centers = []
    for y in range(GRID_Y_DIV):
        sublst_centers.append([x, y])
    lst_centers.append(sublst_centers)

arr_centers = np.array(lst_centers)
arr_centers_coord = GRID_SIZE*arr_centers+GRID_SIZE/2


###############################################################################

ifile  = open(INPUT5, "rb") #
reader = csv.reader(ifile)


intersec_routes = [] # lista con intersecciones entre rutas (matrix 3,600 x 3,600)

for lst_intersec_ori in reader: 
    sub_lst_intersec = [] # sublista correspondiente a una linea de la matriz
    for lst_intersec_dst in lst_intersec_ori:
       if lst_intersec_dst != '':       
           sub_lst_intersec.append(lst_intersec_dst) 
    intersec_routes.append(sub_lst_intersec)
ifile.close()
###############################################################################