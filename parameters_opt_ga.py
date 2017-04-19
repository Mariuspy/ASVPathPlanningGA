#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 10:14:34 2017

@author: mario
"""

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