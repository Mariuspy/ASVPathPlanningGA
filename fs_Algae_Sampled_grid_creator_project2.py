# -*- coding: utf-8 -*-
#==============================================================================
# Fecha de Creacion: 16/01/2017
# Descripcion: Crea una matriz origen x destino indicando si pasa por cuadro de
#               mancha de algas.
# Input:  Matriz de rutas validas ('allowed_routes_positive.csv')
#         Lista de coordenadas de balizas ('ListaCoordenadasConvRefMetros.csv')
#         Patron de mancha de algas('arr_pattern_c.csv')
# Output:'sampled_grid_pattern.csv'
#==============================================================================

import csv
import numpy as np
import time
import os
import parameters_algae_sampled_grid as param
import intersec_finding_func

#from FindRouteIntersections import find_orientation,find_between_points, 
#   find_intersec

print time.ctime() # Para registrar duracion de simulacion
print 'File name = ' , os.path.basename(__file__) # Para registrar nombre de 
                                                  # script
minor_ticks_x = np.arange(0, param.LAKE_SIZE_X, param.GRID_SIZE)
minor_ticks_y = np.arange(0, param.LAKE_SIZE_Y, param.GRID_SIZE)

#==============================================================================
# LAKE_SIZE_X = 12000
# LAKE_SIZE_Y = 14000
# 
# GRID_SIZE = 200 # metros
# GRID_X_DIV = LAKE_SIZE_X/GRID_SIZE # numero de cuadros sobre el eje x
# GRID_Y_DIV = LAKE_SIZE_Y/GRID_SIZE # numero de cuadros sobre el eje y
# 
# N_BEACON = 60
#==============================================================================

color_x=np.arange(0, param.LAKE_SIZE_X, param.GRID_SIZE)
color_y=np.arange(0, param.LAKE_SIZE_Y, param.GRID_SIZE)
##test = pd.read_csv('ListaCoordenadasConvRefMetros.csv')

################Importacion de Rutas posibles##################################
#==============================================================================
# allowed_routes = []
# 
# ifile  = open(param.INPUT1, "rb")
# reader = csv.reader(ifile)
# 
# for coord_list in reader:
#     sub_lst_allowed = []
#     for coords in coord_list:
#        if coords != '':
#            sub_lst_allowed.append(coords) 
#     allowed_routes.append(sub_lst_allowed)
# 
# ifile.close()
# 
# arr_allowed_routes = np.array(allowed_routes)
#==============================================================================

arr_allowed_routes = np.loadtxt(param.INPUT1,dtype ='uint8', delimiter =',')

###############################################################################

lst_centers = []
for x in range(param.GRID_X_DIV):
    sublst_centers = []
    for y in range(param.GRID_Y_DIV):
        sublst_centers.append([x, y])
    lst_centers.append(sublst_centers)

arr_centers = np.array(lst_centers)
arr_centers_coord = param.GRID_SIZE*arr_centers+param.GRID_SIZE/2

##print arr_centers
##print arr_centers_coord


###############################################################################
with open(param.INPUT2, 'rb') as f:
    reader = csv.reader(f)
    coord_orig = list(reader)

list_coord = []
for n in coord_orig:
    list_coord.append([float(n[0]),float(n[1])])

##print list_coord

list_coord2 = []

for n in coord_orig:
    list_coord2.append(complex(float(n[0]),float(n[1])))

##print list_coord2

arr_sampled_grid = np.zeros((param.GRID_X_DIV,param.GRID_Y_DIV))
arr_sampled_grid_pattern = np.zeros((param.N_BEACON*param.GRID_X_DIV,param.N_BEACON*param.GRID_Y_DIV),dtype='uint8')

##with open('best_indiv_algae.csv', 'rb') as f2:
##    reader2 = csv.reader(f2)
##    best_indiv = list(reader2)
##
####print(best_indiv)
####print(type(best_indiv))
##
##list_best_indiv = []
##
##for n in best_indiv:
##    for n2 in n:
##    #list_coord.append(float(n[0]),float(n[1]))
##        list_best_indiv.append(int(n2))

##list_best_indiv = range(60)
##random.shuffle(list_best_indiv)
##print list_best_indiv

arr_alg_pattern = np.loadtxt(param.INPUT3,dtype ='uint8', delimiter =',')

#######Verificacion de interseccion de ruta con cuadros########################

##for origen in range(60):
##    for destino in range(60):
##        print origen,destino
##        if int(allowed_routes[origen][destino]):
####            print 'allowed'

##individual = [5, 48, 8, 46, 15, 34, 0, 33, 58, 29, 11, 22, 50, 20, 51, 17, 
##44, 6, 39, 4, 40, 9, 7, 43, 10, 38, 2, 36, 1, 35, 12, 37, 16, 41, 3, 42, 19, 
##45, 14, 31, 59, 30, 57, 24, 56, 27, 53, 25, 55, 26, 52, 21, 47, 18, 49, 23, 
##54, 28, 13, 32]
##Solucion importada de R_fitness_penalty_factor2.txt



##print list_best_indiv
        
def check_all_intersection(ruta_test,bal_ori,bal_dest):
    "Calcula todas las intersecciones"
    intersec_check = 0 
    for x in range(param.GRID_X_DIV):
        for y in range(param.GRID_Y_DIV):
            if arr_alg_pattern[x][y]:
                centro_test = arr_centers_coord[x][y]
                intersec_check = \
                    intersec_finding_func.check_intersection(    
                        ruta_test,centro_test)
##                if intersec_check == 2 and arr_sampled_grid_pattern[
##                    bal_ori][bal_dest]<1:
                if intersec_check == 2:    
##        print grid_x,grid_y
                    arr_sampled_grid_pattern[bal_ori*param.N_BEACON+x][param.N_BEACON*bal_dest+y]+=1
                    if arr_sampled_grid_pattern[bal_ori*param.N_BEACON+x][param.N_BEACON*bal_dest+y]==1:
                        print bal_ori, bal_dest, x, y, centro_test
##                if (bal_ori == 22 and bal_dest == 56) or (bal_ori == 56 and bal_dest == 22):
##                    print bal_ori, bal_dest, intersec_check, x, y,arr_sampled_grid_pattern[bal_ori][bal_dest]
                    
                
##                check_intersection(ruta_test,centro_test,bal_ori,bal_dest,x,
##                  y) # To graph the sampled path
    

##idx = 0
##idx2 = 42
##
##ruta_test = [list_coord[idx],list_coord[idx2]]
##print ruta_test
##check_all_intersection(ruta_test,idx,idx2)
##print arr_sampled_grid_pattern[idx][idx2]
##print check_all_intersection([list_coord[22],list_coord[56]],22,56)

for idx in range(param.N_BEACON):
    for idx2 in range(param.N_BEACON):
##        print idx, idx2
        if arr_allowed_routes[idx][idx2]:
            print idx, idx2
            ruta_test = [list_coord[idx],list_coord[idx2]]
            check_all_intersection(ruta_test,idx, idx2)
            
##    if idx != len(list_best_indiv)-1:
##        if int(allowed_routes[list_best_indiv[idx]][
##          list_best_indiv[idx+1]]) != 0:
##            print "this"
##            if int(allowed_routes[list_best_indiv[idx]][list_best_indiv[
##              idx+1]]) == -1:
##                
##                n_ruta_inval += 1
##
##            
##                ruta_test = [list_coord[list_best_indiv[idx]],list_coord[
##                  list_best_indiv[idx+1]]]
##                check_all_intersection(ruta_test)
                
####        print ruta_test
##        for x in range(GRID_X_DIV):
##            for y in range(GRID_Y_DIV):
##                centro_test = arr_centers_coord[x][y]
##        ##        print centro_test
##                check_intersection(ruta_test,centro_test,x,y)
####        else:
####            print 'not allowed'

#print arr_sampled_grid         
np.savetxt(param.OUTPUT1, arr_sampled_grid_pattern,  
   fmt = '%i', delimiter=",")

print time.ctime()




