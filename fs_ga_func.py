    #!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 14:29:00 2017

@author: mario
"""
#import time

import parameters_opt_ga as param
import random
import numpy as np
import numpy.ma as ma

import fs_intersec_finding_func
import fs_cities_dist_func

from deap import base, tools

toolbox=base.Toolbox()

### Registro de Funciones de Modulo DEAP######################################
toolbox.register("select1", tools.selRoulette) 
toolbox.register("select2", tools.selBest)
toolbox.register("mate", tools.cxOrdered)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)

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
    
    if (param.arr_centers_coord[x][y][0] >= x_min - param.GRID_SIZE and param.arr_centers_coord[x][y][0] <= x_max + param.GRID_SIZE) and \
        (param.arr_centers_coord[x][y][1]  >= y_min - param.GRID_SIZE and param.arr_centers_coord[x][y][1]-param.GRID_SIZE <= y_max + param.GRID_SIZE):
            check_sq_flag = 1
    
#    print 'x_min, max, y_min, y_max', x_min, x_max, y_min, y_max, check_sq_flag, x, y, arr_centers_coord[x][y][0], arr_centers_coord[x][y][1]
     
    return check_sq_flag


def check_all_intersection(ruta_test,bal_ori,bal_dest, arr_sampled_grid):
    "Calcula intersecciones de todas las rutas con cuadros de grilla"
    
    intersec_check = 0

    
    for x in range(param.GRID_X_DIV):
        for y in range(param.GRID_Y_DIV):
            if param.arr_alg_pattern[x][y] and param.arr_inlake_square[x][y] and \
                check_squares(ruta_test,x,y):
#                print x,y
                centro_test = param.arr_centers_coord[x][y]
#                print ruta_test, centro_test
                intersec_check = fs_intersec_finding_func.check_intersection(    
                        ruta_test,centro_test)
##                if intersec_check == 2 and arr_sampled_grid_pattern[
##                    bal_ori][bal_dest]<1:
                if intersec_check == 2:    
#                    print x,y
                    arr_sampled_grid[x][y]+=1
    
    return arr_sampled_grid

def coefficient_variation(individual):
    "Calcula el coeficiente de variacion de las zonas muestreadas"
    coef_var = 0
    samp_grid = []
    
#    print(individual)
    arr_sampled_grid = np.zeros((param.GRID_X_DIV,param.GRID_Y_DIV))
    
    for idx,elements in enumerate(individual):
        if idx < len(individual)-1:
    #        print individual[idx], individual[idx+1]
            ruta_test = [param.list_coord[individual[idx]],param.list_coord[individual[
                    idx+1]]]
    #        print ruta_test
            samp_grid = check_all_intersection(ruta_test, individual[idx], individual[
                    idx+1],arr_sampled_grid)

     
    
    mdata = ma.masked_less(samp_grid,1)
    
    coef_var = np.std(mdata)/np.mean(mdata)
    
#    print np.sum(samp_grid), round(coef_var,3), round(np.std(mdata),3), round(np.mean(mdata),3)
    
    return coef_var

def pop_valid_creation(cand_pop):
    '''Crea una poblacion valida a partir de un conjunto de balizas '''
    
    print "Creacion de poblacion valida"    
    
    numb_iter = 0 # contador de intentos para hallar poblacion
    numb_solu = 0 # contador de soluciones encontradas
    indiv_len = len(cand_pop)
    print "Longitud de invididuos = ", indiv_len
    
    total_possi_solu = [] # lista de poblacion inicial valida

    while numb_iter < param.ATT_POPU and numb_solu < param.POPU: 

        possi_solu = [] # lista de posible individuo
        numb_iter2 = 0  # contador de intentos para hallar siguiente baliza
        count_solu = 0 # contador de balizas en un individuo
        possi_solu.append(random.randint(0,indiv_len-1)) # Generacion aleatoria 
                                                         # primer elemento
        cand = 0 # baliza candidata
        
        while count_solu < indiv_len and numb_iter2 < param.ATT_FACTOR: 
            cand = random.randint(0,indiv_len-1)
            if cand not in possi_solu:
                if int(param.arr_allowed_routes[cand_pop[possi_solu[-1]]][
                        cand_pop[cand]]) != 1:
                    possi_solu.append(cand)
                    count_solu += 1
#                        print possi_solu
            numb_iter2 += 1
#                print count_solu, numb_iter2, numb_solu, numb_iter

        if len(possi_solu) >= indiv_len:
            numb_solu += 1
            total_possi_solu.append(possi_solu)
#                print possi_solu
    
        numb_iter += 1
    
    print "Intentos  aleatorios de creacion de poblacion =", numb_iter
    print "Tamano de Poblacion =", len(total_possi_solu)
    print "\n"
    return total_possi_solu
    
def initIndividual(icls, content):
    "Inicializacion de clase de Individuo (Externo a DEAP)"
    return icls(content)

def initPopulation(pcls, ind_init,pop_valid):
    "Inicializacion de Poblacion"
    return pcls(ind_init(c) for c in pop_valid)   

            
def create_tour(individual):
    "Relaciona el indice de la baliza con las coordenadas"
    answer = [list(param.cities)[e] for e in individual] # Parea el indice del 
    #   individuo en individual con las coordenadas en cities
#    print(e, answer)
#    print  'Cities', answer,
#    print  'e', e, '\n' 
    return answer

##########################Funcion Objetivo#####################################

def ROI_distribution(indiv_ROI,arr_beacons_ROI, 
                    dict_routes_ROI):
    
    arr_sampled_grid = np.zeros((param.GRID_X_DIV,param.GRID_Y_DIV), dtype=np.int)    

    for idx,indiv_element in enumerate(indiv_ROI):
        if idx < len(indiv_ROI)-1:
##            print indiv_ROI[idx], indiv_ROI[idx+1]
##                print "===="
#                print arr_sampled_grid_pattern[idx][idx+1]
            if str(arr_beacons_ROI[indiv_ROI[idx]])+'_'+str(arr_beacons_ROI[
                    indiv_ROI[idx+1]]) in dict_routes_ROI:
##                print idx, idx+1
                for route_element in dict_routes_ROI[str(arr_beacons_ROI[
                        indiv_ROI[idx]])+'_'+str(arr_beacons_ROI[
                                indiv_ROI[idx+1]])]:
                    arr_sampled_grid[route_element[0]][route_element[1]]+=1
    
#    print 'np.sum', np.sum(arr_sampled_grid)            
    
    mdata = ma.masked_less(arr_sampled_grid,1)
    
    print 'np.mean', np.mean(mdata), 'np.std', np.std(mdata)
    
    if np.std(mdata) != 0:
        inv_coef_var = np.mean(mdata)/np.std(mdata)
    else:
        inv_coef_var = 0
        
    print np.sum(arr_sampled_grid), np.sum(mdata) 
    print round(inv_coef_var,3), round(np.std(mdata),3), round(np.mean(mdata),3)
    
    return inv_coef_var


##########################Funcion Objetivo#####################################

def ROI_calculation(indiv_ROI, arr_routes_AB_est_intersec_ROI,arr_beacons_ROI):
    
    ROI_calc = 0
    
    for idx,indiv_element in enumerate(indiv_ROI):
        if idx < len(indiv_ROI)-1:
##                print individual[idx], individual[idx+1]
##                print "===="
#                print arr_sampled_grid_pattern[idx][idx+1]
            ROI_calc = ROI_calc + (
                arr_routes_AB_est_intersec_ROI[arr_beacons_ROI[
                        indiv_ROI[idx]]][arr_beacons_ROI[indiv_ROI[
                                idx+1]]])   
    
    
    return ROI_calc
    

def evaluation(individual, fit_func_eval, arr_routes_AB_est_intersec_eval, 
               arr_beacons_eval,dict_routes_AB_eval):
    "Selecciona y calcula la Funcion Objetivo de un individuo"
#        print individual
    
###########################Region de Interes###################################    
    if fit_func_eval == 5 or fit_func_eval == 6:
    
        ROI_algae_sampled = ROI_calculation(individual,arr_routes_AB_est_intersec_eval,
                                            arr_beacons_eval)
        
    if fit_func_eval == 9:
        
        ROI_algae_distributed = ROI_distribution(individual,arr_beacons_eval, 
                                                 dict_routes_AB_eval)
    
#==============================================================================
#         for idx,indiv in enumerate(individual):
#             if idx < len(individual)-1:
#     ##                print individual[idx], individual[idx+1]
#     ##                print "===="
#     #                print arr_sampled_grid_pattern[idx][idx+1]
#                 ROI_algae_sampled = ROI_algae_sampled + (
#                         arr_routes_AB_est_intersec_eval[arr_beacons_eval[
#                                 individual[idx]]][arr_beacons_eval[individual[
#                                         idx+1]]])
#==============================================================================
                

##        print ROI_algae_sampled

###############verificacion en matriz de rutas validas#####################
    

#####################Calculo de intersecciones#############################

    tot_intersec_count = 0 # contador de intersecciones en individuos
    tot_intersec_count = fs_intersec_finding_func.invalid_route_count(
            individual, param.arr_allowed_routes, arr_beacons_eval)
   
#==============================================================================
##                     1-  Death Penalty + Penalty Factor -- km2
#==============================================================================

    if fit_func_eval == 1:        
        if tot_intersec_count > 0:
            answer2 = (-1,)
        else:
            answer2 = ((1-float(tot_intersec_count)/(len(individual)-1))*(
                          param.FRANJA*fs_cities_dist_func.total_distance(
                                  create_tour(individual))-(param.FRANJA**2)*
                                      tot_intersec_count)*100/param.LAKE_SIZE,)

 
#==============================================================================
#                      2- Penalty Factor -- coverage %
#==============================================================================

    elif fit_func_eval == 2:
        answer2 = ((1-float(tot_intersec_count)/(len(individual)-1))*(
                       param.FRANJA*fs_cities_dist_func.total_distance(
                               create_tour(individual))-(param.FRANJA**2)*
                                   float(tot_intersec_count))*100/param.LAKE_SIZE,)        

#==============================================================================
##                     3- Exponential Penalty Factor -- coverage %
#==============================================================================
    elif fit_func_eval == 3:    
        answer2 = (np.exp(-tot_intersec_count/8)*(
                       param.FRANJA*fs_cities_dist_func.total_distance(
                               create_tour(individual))-(param.FRANJA**2)*
                                   tot_intersec_count)*100/param.LAKE_SIZE,)        


#==============================================================================
##                      4- Penalty Factor -- size km2       
#==============================================================================
    elif fit_func_eval == 4:
        answer2 = ((1-float(tot_intersec_count)/(len(individual)-1))*(
                  param.FRANJA*fs_cities_dist_func.total_distance(create_tour(
                          individual))-(param.FRANJA**2)*tot_intersec_count),)        
   
    
    
#==============================================================================
# #                     5-Penalty Factor -- ROI exponential  
#==============================================================================
    elif fit_func_eval == 5:
#==============================================================================
#         answer2 =((1-float(tot_intersec_count)/(len(individual)-1))*
#                   ROI_algae_sampled,)
#==============================================================================
        answer2 =((np.exp(-tot_intersec_count/8))*ROI_algae_sampled,)
        
#==============================================================================
#         print individual, answer2
#         print tot_intersec_count, ROI_algae_sampled
#==============================================================================

#==============================================================================
# #                    6-  Death Penalty -- ROI        
#==============================================================================
    elif fit_func_eval == 6:
        if tot_intersec_count > 0:
            answer2 = (-1,)
        else:
            answer2 =(ROI_algae_sampled,)
    
#==============================================================================
#                     7-  Death Penalty -- variation coefficient      
#==============================================================================  
    elif fit_func_eval == 7:
        if tot_intersec_count > 0:
            answer2 = (-1,)
        else:
            answer2 =(coefficient_variation(individual),)  
#==============================================================================
#                     8- Penalty Factor -- variation coefficient        
#==============================================================================  
    elif fit_func_eval == 8:
        answer2 =((1-float(tot_intersec_count)/(len(
                individual)-1))*coefficient_variation(individual),)  
        
#==============================================================================
#                     9- Penalty Factor -- ROI distribution        
#==============================================================================  
    elif fit_func_eval == 9:
        answer2 =((np.exp(-tot_intersec_count/8))*ROI_algae_distributed,) 
        
    else:
        print 'FIT_FUNC_TYPE ERROR!'
    
    
    return answer2 # El fitness siempres es una tupla


def genetic_algorithm(pop):
    "Implementacion del GA en una poblacion dada (pop)"
    
    print "Start of the Genetic Algorithm"
    print "\n"
    
    list_max = [] # lista de maximas de las generaciones de esta simulacion
    list_ave = [] # lista de promedio de las generaciones de esta simulacion
    list_imp_rate = [] # lista de mejora del fitness percentual a traves de las
                       # generaciones
    prev_best_fitness = 0
    improv_rate = 0
    valid_solu_flag_in = 0
    valid_solu_flag_out = 0
    valid_gen = -1

##        Inicio de GA
    
    # Evaluacion de toda la poblacion
    fitnesses = list(map(toolbox.evaluate, pop))
#        print pop
    for ind, fit in zip(pop, fitnesses):
#            print fit
        ind.fitness.values = fit
    
#==============================================================================
#     # Inicio de Evolucion
#==============================================================================
    for g in range(param.NGEN):
#        print 'Generation=', g #, time.ctime()
        gen_best=[]
        
        # Seleccion de inviduos para la proxima generacion
        offspring = toolbox.select1(pop, int(param.POPU*(
                1-param.ELIT_RATE))) # Se aplicaran operadores geneticos
        offspring_aux = toolbox.select2(pop, int(
                param.POPU*param.ELIT_RATE)) # Elitismo
        # Clonacion de los individuos elegidos
        offspring = list(map(toolbox.clone, offspring))
    
        # Operadores geneticos
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
#                print child1, child2
            if random.random() < param.CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < param.MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        offspring = offspring + offspring_aux # Se agrega elitismo

        # Se evaluan individuos con fitness invalidos, y se calcula los valores de ellos
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        
##        print("  Evaluated %i individuals" % len(invalid_ind))
        
        # Se reemplaza la poblacion con los hijos
        pop[:] = offspring
        # Se juntan los fitness de la poblacion en una lista
        fits = [ind.fitness.values[0] for ind in pop]

            
        length = len(pop)
        mean = sum(fits) / length
#            sum2 = sum(x*x for x in fits)
#            std = abs(sum2 / length - mean**2)**0.5

        list_max.append(max(fits))
        list_ave.append(mean)
        
        if g > 0:
            improv_rate = (max(fits)-prev_best_fitness)*100/prev_best_fitness
            
            
#            print g, max(fits),improv_rate    
        list_imp_rate.append(improv_rate)
        prev_best_fitness = max(fits)
        gen_best = tools.selBest(pop,1)[0]
        
#        print 'Gen_best=', gen_best, max(fits)

                 
 ## Se verifica si el mejor individuo de la generacion es valido
        if valid_solu_flag_out == 0 and g > 0:
             for idx, indiv in enumerate(gen_best): # verificacion en matriz de rutas validas
                 if idx != (len(gen_best)-1):
                     if int(param.arr_allowed_routes[param.arr_subgroup[
                             gen_best[idx]]][param.arr_subgroup[
                                     gen_best[idx+1]]]) == 1:
                         valid_solu_flag_in = 0
                         break
                     else:
                        valid_solu_flag_in = 1
             if valid_solu_flag_in == 1:
                 valid_solu_flag_out = 1
                 valid_gen = g 
#                 print "valid gen", valid_gen
                 

                      
            
##    print("-- End of (successful) evolution --")
    best_ind = tools.selBest(pop, 1)[0]
    worst_ind = tools.selWorst(pop,1)[0]
    
    print best_ind.fitness, max(fits)
    
    last_pop = pop
    
#    print best_ind

#==============================================================================
#     ## Se verifica si el mejor individuo de la generacion es valido
#         if valid_solu_flag == 0:
#             for idx, indiv in enumerate(best_ind): # verificacion en matriz de rutas validas
#                 if idx != (len(best_ind)-1):
#                     if int(arr_allowed_routes[best_ind[idx]][best_ind[idx+1]]) != 1:
#                         valid_solu_flag = 1
# 
#         if valid_solu_flag == 1:
#             print g
#             valid_gen = g
# 
#         n_ruta_inval = 0 # contador de rutas invalidas en individuo
# 
#         for idx, indiv in enumerate(best_ind): # verificacion en matriz de rutas validas
#             if idx != (len(best_ind)-1):
#                 if int(arr_allowed_routes[best_ind[idx]][best_ind[idx+1]]) == 1:
#                     n_ruta_inval += 1
#                     
#         print n_ruta_inval            
#==============================================================================

    
    
#    Se retornan indicadores del GA
    return (best_ind , max(fits), worst_ind, list_max, list_ave, 
            list_imp_rate, valid_gen, last_pop) #, pop, list_max

#####Registro de la funcion evaluate luego de definir la funcion evaluation            

def assign_eval_parameters(fit_func, arr_routes_AB_est_intersec, arr_beacons,
                           dict_routes_AB_est_intersec):
    toolbox.register("evaluate",evaluation, 
                     fit_func_eval = fit_func, 
                     arr_routes_AB_est_intersec_eval = arr_routes_AB_est_intersec,
                     arr_beacons_eval = arr_beacons, 
                     dict_routes_AB_eval = dict_routes_AB_est_intersec)

#==============================================================================
# def subgroup_selection():
#     "Seleccion sub-conjunto de balizas alrededor de mancha de algas"
#     arr_alg_coord= np.loadtxt('arr_alg_coord_size_event_tracking3.csv' ,
#                               dtype = 'uint8', delimiter =',')
#     max_north_coord = np.max(arr_alg_coord)[0]
#     min_north_coord = np.mix(arr_alg_coord)[0]
#     
#     
#     for element in arr_alg_coord:
#         
#         if abs(element[0]-prev_element[0])>1:
#==============================================================================
            
        
    
    
    
    
