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

INPUT1 = 'Data/arr_alg_pattern_size_event_tracking3.csv' #
INPUT2 = 'Data/sampled_grid_event_tracking.csv' # used in evaluation function (fs_ga_func.py)
INPUT3 = 'Constants/combination.csv' # used in pop_valid_creation, evaluation 
                                    # and invalid_route_count functions 
                                    # (fs_ga_func.py and fs_MainOptim....py)
INPUT4 = 'Constants/ListaCoordenadasConvRefMetros3.csv' # used in create_tour 
                                                        # (fs_ga_func.py)
INPUT5 = 'Constants/intersection_routes.csv'# used in intersec_count_f function 
                                            #(fs_intersec_finding_func.py)
INPUT6 = 'best_last_pop.csv'#
#INPUT7 = 'sampled_grid_event_tracking2.csv' # Not used in GA
INPUT8 = 'Constants/in_lake.csv'
INPUT9 = 'Constants/in_lake_center.csv'
INPUT10 = 'Constants/allowed_routes_positive.csv'


OUTPUT1 = 'Results/best_indiv_test_ngen100_sim1.csv'
OUTPUT2 = 'Results/improve_rate_ngen100_sim1.csv'
OUTPUT3 = 'Results/ImproveRate_Solution_ngen100_sim1.png'
OUTPUT4 = 'Results/Best_Solution_ngen100_sim1.csv'
OUTPUT5 = 'Results/best_last_pop_test.csv'

N_BEACON = 60 
N_SIM = 1
CXPB = 0.6
MUTPB =  0.2
NGEN = 100
POPU = 100
ELIT_RATE = 0.2
FRANJA = 20
ATT_FACTOR = 1000 # Intentos para encontrar siguiente baliza en poblacion inicial valida
ATT_POPU = 10000 # Intentos para encontrar una poblacion inicial validad  de POPU individuos
LAKE_SIZE = 68720000

LAKE_SIZE_X = 12000
LAKE_SIZE_Y = 14000

GRID_SIZE = 200 # metros
GRID_X_DIV = LAKE_SIZE_X/GRID_SIZE # numero de cuadros sobre el eje x
GRID_Y_DIV = LAKE_SIZE_Y/GRID_SIZE # numero de cuadros sobre el eje y

FIT_FUNC_TYPE = 2
STRATEGY_PHASE = 1 #NO CAMBIAR HASTA ENCONTRAR FUNCION PARA SELECCION DE 
                   # SUB_GRUPO DE BALIZAS PARA FASE DE INTENSFICACION

'''
1 - Death Penalty + Penalty Factor -- km2
2 - Penalty Factor -- coverage %
3 - Exponential Penalty Factor -- coverage %
4 - Penalty Factor -- size km2
5 - Penalty Factor -- ROI
6 -  Death Penalty
7 -  Death Penalty -- ROI variation
8 - Penalty Factor -- ROI variation   
'''

EXPERIMENT = 'test'

#==============================================================================
# # CONSTANTES
#==============================================================================
#==============================================================================
# arr_sampled_grid_pattern = np.loadtxt(INPUT2, dtype = 'uint8', 
#                                       delimiter =',')
#==============================================================================

###############################################################################

if STRATEGY_PHASE == 1:
        arr_subgroup = np.arange(60,dtype='uint8') 

else:
    #PENDIENTE MECANISMO DE SELECCION DE SUBGRUPO DE BALIZAS!!!!!
    
    arr_reg1= np.loadtxt('reg1_ev_track.csv' ,dtype = 'uint8', delimiter =',')
    arr_reg2= np.loadtxt('reg2_ev_track.csv' ,dtype = 'uint8', delimiter =',')
    
    
    arr_subgroup = np.concatenate((arr_reg1,arr_reg2))


###############################################################################



#==============================================================================
# ###################Importar rutas validas################################
#  Importa archivo combination.csv
#  combination.csv = Matriz 60 x 60
#  Indica si una ruta es valida desde una baliza a otra (fila a columna)
#==============================================================================

arr_allowed_routes = np.loadtxt(INPUT3,dtype = 'uint8',delimiter =',' )

arr_allowed_routes_pos = np.loadtxt(INPUT10,dtype = 'uint8',delimiter =',') 

###############################################################################

lst_centers = []
for x in range(GRID_X_DIV):
    sublst_centers = []
    for y in range(GRID_Y_DIV):
        sublst_centers.append([x, y])
    lst_centers.append(sublst_centers)

arr_centers = np.array(lst_centers)
arr_centers_coord = GRID_SIZE*arr_centers+GRID_SIZE/2


#==============================================================================
# ###################Importar matriz de intersecciones#########################
#   Importa archivo intersection_routes.csv
#   intersection_routes.csv = Matriz 3,600 x 3,600
#   Las lineas y columnas representan las rutas
#   x= N_BEACONS*Baliza_origen1 + Baliza_destino1
#   y= N_BEACONS*Baliza_origen2 + Baliza_destino2
#   La interseccion en la matriz indica si hay interseccion o no entre las 
#   rutas (0 o 1)
#   Ej.: Ruta 1 = b1b2, Ruta 2 = b3b4
#   Verificar en x = 1*60 + 2 = 62 e y = 3*60 + 4 = 184 
#==============================================================================


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

#==============================================================================
# ###########Importar Coordenadas de Archivo###################################
#   Importa archivoListaCoordenadasConvRefMetros.csv
#   ListaCoordenadasConvRefMetros.csv = Matriz 60 x 2
#   Cada linea de la matriz representa las coordenadas en metros de cada baliza
#   Ej.: b0 = (4860, 13500)
#   El origen es un punto de referencia
#==============================================================================

with open(INPUT4, 'rb') as f: 
    reader = csv.reader(f)
    coord_orig = list(reader)
    
###Coordenadas para el calculo del rango de accion en numeros decimales########
    
list_coord = [] # lista de coordenadas de balizas en formato (x,y)

for n in coord_orig:
    coord = [float(n[0]), float(n[1])]
    list_coord.append(coord)

#############Coordenadas para el algoritmo genetico en numeros complejos#######


    
list_coord2 = [] # lista de coordenadas de balizas en formato (x + jy) 
#                   (numero complejo)

for n in coord_orig:
    list_coord2.append(complex(float(n[0]),float(n[1])))
    
    
    
list_coord_subgroup =[]
    
for element in arr_subgroup:
        list_coord_subgroup.append(list_coord2[element])

    
cities = list_coord2 # 1- coordenadas de la ciudad en el TSP, se utiliza para
#    create_tour y graficar
#    cities = list_coord_subgroup # 2- subgrupo de balizas

#print 'len cities', len(cities)

arr_inlake_square = np.loadtxt(INPUT8,dtype ='uint8', delimiter =',')

lst_centers = []
for x in range(GRID_X_DIV):
    sublst_centers = []
    for y in range(GRID_Y_DIV):
        sublst_centers.append([x, y])
    lst_centers.append(sublst_centers)

arr_centers = np.array(lst_centers)

arr_centers_coord = GRID_SIZE*arr_centers+GRID_SIZE/2

#arr_alg_pattern = np.loadtxt(INPUT1,dtype ='uint8', delimiter =',')

arr_inlake_center = np.loadtxt(INPUT9,dtype ='uint8', delimiter =',')

samp_pattern =  np.zeros((GRID_X_DIV,GRID_Y_DIV),dtype = 'uint8') 

