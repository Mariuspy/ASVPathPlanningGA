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
import numpy.ma as ma
import time
import os
import parameters_algae_sampled_grid as param
import parameters_opt_ga as param2

import fs_intersec_finding_func

#from FindRouteIntersections import find_orientation,find_between_points, 
#   find_intersec

print time.ctime() # Para registrar duracion de simulacion
print 'File name = ' , os.path.basename(__file__) # Para registrar nombre de 
                                                  # script

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

arr_inlake_square = np.loadtxt(param.INPUT4,dtype ='uint8', delimiter =',')

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
    list_coord.append([int(n[0]),int(n[1])])

##print list_coord

#==============================================================================
##########nO UTILIZADO AQUI####################################################
#
# list_coord2 = []
# 
# for n in coord_orig:
#     list_coord2.append(complex(float(n[0]),float(n[1])))
#==============================================================================

##print list_coord2

arr_sampled_grid = np.zeros((param.GRID_X_DIV,param.GRID_Y_DIV))
#arr_sampled_grid_pattern = np.zeros((param.N_BEACON*param.GRID_X_DIV,param.N_BEACON*param.GRID_Y_DIV),dtype='uint8')

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

individual = [1, 39, 2, 44, 14, 45, 37, 21, 55, 28, 31, 17, 11, 42, 26, 40, 57,
              3, 50, 27, 32, 20, 33, 25, 34, 29, 53, 23, 12, 49, 10, 41, 13, 
              24, 38, 9, 52, 7, 51, 5, 59, 30, 19, 35, 15, 43, 22, 54, 6, 58,
              8, 56, 36, 0, 4, 47, 18, 46, 48, 16]

##Solucion importada de R_fitness_penalty_factor2.txt



##print list_best_indiv
        
def check_squares(ruta_test,x,y):
    "Verifica si los cuadros x,y estan en el rango de accion de ruta_test"
    x_min = x_max = y_min = y_max = 0 # limit of the search space
    check_sq_flag = 0
    
    if ruta_test[0][0] < ruta_test[1][0]:
        x_min = ruta_test[0][0]
        x_max = ruta_test[1][0]
    else:
        x_min = ruta_test[1][0]
        x_max = ruta_test[0][0]
        
    if ruta_test[0][1] < ruta_test[1][1]:
        y_min = ruta_test[0][1]
        y_max = ruta_test[1][1]
    else:
        y_min = ruta_test[1][1]
        y_max = ruta_test[0][1]
    
    if (arr_centers_coord[x][y][0] >= x_min - param2.GRID_SIZE and arr_centers_coord[x][y][0] <= x_max + param2.GRID_SIZE) and \
        (arr_centers_coord[x][y][1]  >= y_min - param2.GRID_SIZE and arr_centers_coord[x][y][1]-param2.GRID_SIZE <= y_max + param2.GRID_SIZE):
            check_sq_flag = 1
    
#    print 'x_min, max, y_min, y_max', x_min, x_max, y_min, y_max, check_sq_flag, x, y, arr_centers_coord[x][y][0], arr_centers_coord[x][y][1]
     
    return check_sq_flag

def check_all_intersection(ruta_test,bal_ori,bal_dest):
    "Calcula intersecciones de todas las rutas con cuadros de grilla"
    intersec_check = 0 
    counter = 0
    
#    print ruta_test
    for x in range(param.GRID_X_DIV):
        for y in range(param.GRID_Y_DIV):
            if arr_alg_pattern[x][y] and arr_inlake_square[x][y] and check_squares(ruta_test,x,y):
                    
#                print x,y
                centro_test = arr_centers_coord[x][y]
#                print ruta_test, centro_test
                intersec_check = fs_intersec_finding_func.check_intersection(    
                        ruta_test,centro_test)
##                if intersec_check == 2 and arr_sampled_grid_pattern[
##                    bal_ori][bal_dest]<1:
                if intersec_check == 2:    
                    print '======',arr_centers_coord[x][y]
                    arr_sampled_grid[x][y]+=1
                    counter += 1
#                    if arr_sampled_grid_pattern[bal_ori*param.N_BEACON+x][param.N_BEACON*bal_dest+y]==1:
#                        print bal_ori, bal_dest, x, y, centro_test
##                if (bal_ori == 22 and bal_dest == 56) or (bal_ori == 56 and bal_dest == 22):
##                    print bal_ori, bal_dest, intersec_check, x, y,arr_sampled_grid_pattern[bal_ori][bal_dest]
                    
    print counter, bal_ori, bal_dest, list_coord[bal_ori],list_coord[bal_dest]
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

#==============================================================================
# for idx in range(param.N_BEACON):
#     for idx2 in range(param.N_BEACON):
# ##        print idx, idx2
#         if arr_allowed_routes[idx][idx2]:
# #            print idx, idx2
#             ruta_test = [list_coord[idx],list_coord[idx2]]
#             check_all_intersection(ruta_test,idx, idx2)
#==============================================================================
            
for idx3,elements in enumerate(individual):
    if idx3 < len(individual)-1:
#        print individual[idx3], individual[idx3+1]
        ruta_test = [list_coord[individual[idx3]],list_coord[individual[idx3+1]]]
#        print ruta_test
        check_all_intersection(ruta_test, individual[idx3], individual[idx3+1])
        

mdata = ma.masked_less(arr_sampled_grid,1)

coef_var = np.std(mdata)/np.mean(mdata)

print round(np.std(mdata),3), round(np.mean(mdata),3), round(coef_var,3)
            
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
np.savetxt('test.csv', arr_sampled_grid,  
   fmt = '%i', delimiter=",")

print time.ctime()




