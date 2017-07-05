# -*- coding: utf-8 -*-
'''
#==============================================================================
#   Fecha de Creacion: 01/06/2017
#   Descripcion: Basado en CAlculoCoberturaTemporal. 
#               Presenta cantidad de veces
#                 que el dron ha pasado por los cuadros de la grilla del lago
#   Input:  Rutas validas('combination.csv')
#           Lista de coordenadas('ListaCoordenadasConvRefMetros.csv')
#           Mejor individuo obtenido de GA ('best_indiv_algae_pattern_pop100_
#               gen5000_2.csv')
#   Output: Representacion del lago con cantidad de veces que el dron ha pasado
#           en cada cuadro de la grilla           
#           'sampled_grid_performed_size_algae_pattern_pop100_gen5000_2.csv'
#==============================================================================
'''

#==============================================================================
# import csv
#==============================================================================
import numpy as np
import time
import os
import fs_intersec_finding_func

import parameters_opt_ga as param
#==============================================================================
# import fs_intersec_finding_func
#==============================================================================


def main(list_best_indiv,arr_alg_coord):
    
    print time.ctime() # Para registrar duracion de simulacion
    print 'File name = ' , os.path.basename(__file__) # Para registrar nombre de script
    

#     arr_alg_coord = np.loadtxt(param.INPUT4, dtype = 'uint16', delimiter =',')
    # arr_alg_pattern = np.loadtxt(param.INPUT5, dtype = 'uint16', delimiter =',')
    
#    print arr_alg_coord.dtype
    
#    print arr_alg_coord
    
    ###############################################################################
    ##############Copiado de FindRouteIntersections.py#############################
    ###############################################################################
    ###############################################################################
    
    ################Importacion de Rutas posibles##################################
#==============================================================================
#     allowed_routes = []
#     
#     ifile  = open(param.INPUT1, "rb")
#     reader = csv.reader(ifile)
#     
#     for coord_list in reader:
#         sub_lst_allowed = []
#         for coords in coord_list:
#            if coords != '':
#                sub_lst_allowed.append(coords) 
#         allowed_routes.append(sub_lst_allowed)
#     
#     ifile.close()
#==============================================================================
    
#    allowed_routes = param.arr_allowed_routes
    
    
    
    ##################################################################################
    ##################################################################################
    
    
#==============================================================================
#     lst_centers = []
#     for x in range(param.GRID_X_DIV):
#         sublst_centers = []
#         for y in range(param.GRID_Y_DIV):
#             sublst_centers.append([x, y])
#         lst_centers.append(sublst_centers)
#     
#     arr_centers = np.array(lst_centers,dtype = 'uint16')
#     arr_centers_coord = param.GRID_SIZE*arr_centers+param.GRID_SIZE/2
#==============================================================================
    
    arr_centers_coord = param.arr_centers_coord
    
    ##################################################################################
#==============================================================================
#     with open(param.INPUT2, 'rb') as f:
#         reader = csv.reader(f)
#         coord_orig = list(reader)
#     
#     list_coord = []
#     for n in coord_orig:
#         list_coord.append([float(n[0]),float(n[1])])
#     
#     ##print list_coord
#==============================================================================
    
    list_coord = param.list_coord
    
#==============================================================================
#     list_coord2 = []
#     
#     for n in coord_orig:
#         list_coord2.append(complex(float(n[0]),float(n[1])))
#     
#     ##print list_coord2
#==============================================================================
    
    ##################################################################################
    
    
    
    
    
    arr_sampled_grid = np.zeros((param.GRID_X_DIV,param.GRID_Y_DIV),
                                dtype = 'uint16') # cuadros del lago muestreados
    arr_sampled_grid_algae = np.zeros((
            param.GRID_X_DIV,param.GRID_Y_DIV),dtype = 'uint16') # cuadros del
                                                                 # lago con 
                                                                 # algas muestreados
    
    
#==============================================================================
#     list_best_indiv = np.loadtxt(param.INPUT3, dtype = 'int', delimiter =',')
#==============================================================================
    
    
    ##print list_best_indiv
    
    first_cover_lst = [0]
    redund_cover_lst = [0]
    
#==============================================================================
#     in_lake_center = [] # lista de centros de cuadros dentro del lago
#     
#     in_lake_map = np.loadtxt(param.INPUT6,dtype = 'int', delimiter =',')
#             
#     in_lake_center = np.loadtxt(param.INPUT7,dtype = 'int', delimiter =',')
#==============================================================================
    
    in_lake_center = param.arr_inlake_center
    #==============================================================================
    # def verify_passing_grids(ruta_test):
    #     for x in range(param.GRID_X_DIV): # Verificar los cuadros por los que pasa
    #         for y in range(param.GRID_Y_DIV):
    #             centro_test = arr_centers_coord[x][y]
    #         ##        print centro_test
    #             intersec_check = intersec_finding_func.check_intersection(
    #                 ruta_test,centro_test)
    #             
    #             if intersec_check == 2: 
    #                     #and arr_sampled_grid_pattern[bal_ori][bal_dest]<1:
    #      ##   print grid_x,grid_y
    #                     if [x,y] in arr_alg_coord:
    #                        print x,y 
    #                        if arr_sampled_grid[x][y] < 1:
    #                            first_cover_lst[idx] += 1
    #                        else:
    #                            redund_cover_lst[idx] += 1
    #                     arr_sampled_grid[x][y]+=1
    #==============================================================================
        
    
    #==============================================================================
    # for idx in range(len(list_best_indiv)): # Para cada baliza del individuo
    #     print idx, list_best_indiv[idx]
    #     if idx != len(list_best_indiv)-1: # Excepto la ultima baliza
    #         ruta_test = [list_coord[list_best_indiv[idx]],list_coord[
    #             list_best_indiv[idx+1]]]    
    #         print 'Ruta test', ruta_test
    #         intersec_check = 0
    #         for x in range(param.GRID_X_DIV): # Verificar los cuadros por los que pasa
    #             for y in range(param.GRID_Y_DIV):
    #                 centro_test = arr_centers_coord[x][y]
    #                 print 'Centro test', centro_test
    #                 intersec_check = intersec_finding_func.check_intersection(
    #                     ruta_test,centro_test)
    #                 if intersec_check == 2: 
    #                     #and arr_sampled_grid_pattern[bal_ori][bal_dest]<1:
    # # ##        print grid_x,grid_y
    #                     if [x,y] in arr_alg_coord:
    #                        print x,y 
    #                        if arr_sampled_grid[x][y] < 1:
    #                            first_cover_lst[idx] += 1
    #                        else:
    #                            redund_cover_lst[idx] += 1
    #                     arr_sampled_grid[x][y]+=1
    #                 ##        else:
    # ##            print 'not allowed'
    #         first_cover_lst.append(first_cover_lst[idx])
    #         redund_cover_lst.append(redund_cover_lst[idx])
    #==============================================================================
            
    for idx in range(len(list_best_indiv)): # Para cada baliza del individuo
    #for idx in range(3): # Para cada baliza del individuo
    #    print idx, list_best_indiv[idx]
        if idx != len(list_best_indiv)-1: # Excepto la ultima baliza
            ruta_test = [list_coord[list_best_indiv[idx]],list_coord[
                list_best_indiv[idx+1]]]    
#==============================================================================
#             print 'ruta_test',list_best_indiv[idx],list_best_indiv[idx+1]
#             print type(list_best_indiv[idx])
#==============================================================================
            intersec_check = 0
    
            for elem in in_lake_center:
                
                centro_test = arr_centers_coord[elem[0],elem[1]]
    #            print 'centro_test', centro_test
                intersec_check = fs_intersec_finding_func.check_intersection(
                          ruta_test,centro_test)
    #            print 'intersec_check', intersec_check
                
                
                if intersec_check == 2: 
    #                      and arr_sampled_grid_pattern[bal_ori][bal_dest]<1:
    #                print 'intersec_check', intersec_check
    #                print 'Alg Square', elem[0],elem[1]
    #                lst_alg_coord = arr_alg_coord.tolist()
                    for elem2 in arr_alg_coord:
                        if np.array_equal(elem,elem2):
#==============================================================================
#                             print 'Elem 0,1 y arr value', elem[0],elem[
#                                 1], arr_sampled_grid_algae[elem[0]][elem[1]] 
#==============================================================================
                            if arr_sampled_grid_algae[elem[0]][elem[1]] < 1:
#==============================================================================
#                                 print elem, elem2
#                                 print '----First cover',first_cover_lst
#==============================================================================
                                first_cover_lst[idx] += 1
                            else:
#==============================================================================
#                                 print 'This', elem, elem2
#                                 print '----Redund cover',redund_cover_lst
#                                 print elem, elem2
#==============================================================================
                                redund_cover_lst[idx] += 1
                            
                            arr_sampled_grid_algae[elem[0]][elem[1]] += 1
                                                  
                    arr_sampled_grid[elem[0]][elem[1]] += 1
                    
    #==============================================================================
    #                 if elem in lst_alg_coord:
    #                     print '--Alg Square', elem
    #                     if arr_sampled_grid[elem[0]][elem[1]] < 1:
    #                         first_cover_lst[idx] += 1
    #                         print '----First cover',first_cover_lst 
    #                     else:
    #                         redund_cover_lst[idx] += 1
    #                         print '----Redund cover',redund_cover_lst
    #                 arr_sampled_grid[elem[0]][elem[1]] += 1
    #==============================================================================
                                    
            first_cover_lst.append(first_cover_lst[idx])
            redund_cover_lst.append(redund_cover_lst[idx])
                                           
                                           
    #==============================================================================
    #          for x in range(param.GRID_X_DIV): # Verificar los cuadros por los que pasa
    #              for y in range(param.GRID_Y_DIV):
    #                  centro_test = arr_centers_coord[x][y]
    #          ##        print centro_test
    #                  intersec_check = intersec_finding_func.check_intersection(
    #                      ruta_test,centro_test)
    #                  if intersec_check == 2: 
    #                      #and arr_sampled_grid_pattern[bal_ori][bal_dest]<1:
    #  # ##        print grid_x,grid_y
    #                      if [x,y] in arr_alg_coord:
    #                         print x,y 
    #                         if arr_sampled_grid[x][y] < 1:
    #                             first_cover_lst[idx] += 1
    #                         else:
    #                             redund_cover_lst[idx] += 1
    #                      arr_sampled_grid[x][y]+=1
    #                  ##        else:
    #  ##            print 'not allowed'
    #          first_cover_lst.append(first_cover_lst[idx])
    #          redund_cover_lst.append(redund_cover_lst[idx])
    #==============================================================================
    
    
    
#==============================================================================
#     print (first_cover_lst)
#     print (redund_cover_lst)
#==============================================================================
    
    
            
    #==============================================================================
    # arr_sampled_grid_filter = arr_sampled_grid         
    # np.savetxt(param.OUTPUT1, arr_sampled_grid_algae, fmt = '%i', delimiter=",")
    # np.savetxt(param.OUTPUT2, first_cover_lst, fmt = '%i', delimiter=",")
    # np.savetxt(param.OUTPUT3, redund_cover_lst, fmt = '%i', delimiter=",")
    # np.savetxt(param.OUTPUT4, arr_sampled_grid, fmt = '%i', delimiter=",")
    # 
    #==============================================================================
    
    print time.ctime()
    
    return arr_sampled_grid_algae




