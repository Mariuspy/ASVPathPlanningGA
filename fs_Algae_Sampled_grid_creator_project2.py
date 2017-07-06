# -*- coding: utf-8 -*-
'''
#==============================================================================
# Fecha de Creacion: 01/06/2017
# Descripcion: Crea una matriz origen x destino indicando si pasa por cuadro de
#               mancha de algas.
#               Basada en Algae_SAmpled_grid_creator
#               Nombre original fs_Alage_Sampled_grid_creator_project2.py               
# Input:  Matriz de rutas validas ('allowed_routes_positive.csv')
#         Lista de coordenadas de balizas ('ListaCoordenadasConvRefMetros.csv')
#         Patron de mancha de algas('arr_pattern_c.csv')
# Output:'sampled_grid_pattern.csv'
#==============================================================================
'''

import numpy as np
import time
import os
import parameters_algae_sampled_grid as param
import parameters_opt_ga as param2
import fs_intersec_finding_func

#from FindRouteIntersections import find_orientation,find_between_points, 
#   find_intersec



def main(arr_alg_pattern):
    

    
    print 'Start fs_algae routine', time.ctime() # Para registrar duracion de simulacion
    print 'File name = ' , os.path.basename(__file__) # Para registrar nombre de 
    
    
    #==============================================================================
    # arr_allowed_routes = np.loadtxt(param.INPUT1,dtype ='uint8', delimiter =',')
    #==============================================================================
    
    
#    arr_sampled_grid = np.zeros((param.GRID_X_DIV,param.GRID_Y_DIV))
    arr_sampled_grid_pattern = np.zeros((param.N_BEACON,param.N_BEACON),dtype='uint8')
    dict_sampled_grid = {}
    

    
#==============================================================================
#     arr_alg_pattern = np.loadtxt(param.INPUT3,dtype ='uint8', delimiter =',')
#==============================================================================
    


            
    def check_all_intersection(ruta_test,bal_ori,bal_dest):
        "Calcula todas las intersecciones"
        intersec_check = 0 
#==============================================================================
#         if bal_ori == 7 and bal_dest == 54:
#             print bal_ori, bal_dest
#==============================================================================
        for x in range(param.GRID_X_DIV):
            for y in range(param.GRID_Y_DIV):
                if param2.samp_pattern[x][y]:# and param2.arr_inlake_square[x][y]:
                    centro_test = param2.arr_centers_coord[x][y]
                    intersec_check = \
                        fs_intersec_finding_func.check_intersection(    
                            ruta_test,centro_test)
    ##                if intersec_check == 2 and arr_sampled_grid_pattern[
    ##                    bal_ori][bal_dest]<1:
#==============================================================================
#                     if bal_ori == 7 and bal_dest == 54:
#                         print '-----------', centro_test, intersec_check
#==============================================================================
                    if intersec_check >= 2:    
#==============================================================================
#     ##        print grid_x,grid_y
#                         if bal_ori == 7 and bal_dest == 54:
#                             print '================', centro_test, intersec_check
#==============================================================================
    
                        arr_sampled_grid_pattern[bal_ori][bal_dest]+=1
                        
                        if str(bal_ori)+'_'+str(bal_dest) in dict_sampled_grid:
                            dict_sampled_grid[str(bal_ori)+'_'+str(bal_dest)].append([x,y])
                        else:
                            dict_sampled_grid[str(bal_ori)+'_'+str(bal_dest)] = [[x,y]]
                            
#==============================================================================
#                         if arr_sampled_grid_pattern[bal_ori*param.N_BEACON+x][
#                                 param.N_BEACON*bal_dest+y]==1:
#                             print bal_ori, bal_dest, x, y, centro_test
#==============================================================================
    ##                if (bal_ori == 22 and bal_dest == 56) or (bal_ori == 56 and bal_dest == 22):
    ##                    print bal_ori, bal_dest, intersec_check, x, y,arr_sampled_grid_pattern[bal_ori][bal_dest]
                        
                    
    ##                check_intersection(ruta_test,centro_test,bal_ori,bal_dest,x,
    ##                  y) # To graph the sampled path
        
    
    ##idx = 0
    ##idx2 = 42
    ##
    ##ruta_test = [param2.list_coord[idx],param2.list_coord[idx2]]
    ##print ruta_test
    ##check_all_intersection(ruta_test,idx,idx2)
    ##print arr_sampled_grid_pattern[idx][idx2]
    ##print check_all_intersection([param2.list_coord[22],param2.list_coord[56]],22,56)
    
    for idx in range(param.N_BEACON):
        for idx2 in range(param.N_BEACON):
    ##        print idx, idx2
            if param2.arr_allowed_routes_pos[idx][idx2]:
    ##            print idx, idx2
                ruta_test = [param2.list_coord[idx],param2.list_coord[idx2]]
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
    ##                ruta_test = [param2.list_coord[list_best_indiv[idx]],param2.list_coord[
    ##                  list_best_indiv[idx+1]]]
    ##                check_all_intersection(ruta_test)
                    
    ####        print ruta_test
    ##        for x in range(GRID_X_DIV):
    ##            for y in range(GRID_Y_DIV):
    ##                centro_test = param2.arr_centers_coord[x][y]
    ##        ##        print centro_test
    ##                check_intersection(ruta_test,centro_test,x,y)
    ####        else:
    ####            print 'not allowed'
    
    #print arr_sampled_grid         
#==============================================================================
#     np.savetxt(param.OUTPUT1, arr_sampled_grid_pattern,  
#        fmt = '%i', delimiter=",")
#==============================================================================
    
    print 'Ending fs_algae routine', time.ctime()
    print '\n'
    
    print len(arr_sampled_grid_pattern)
    
    return arr_sampled_grid_pattern, dict_sampled_grid

if __name__ == '__main__':
    main()


