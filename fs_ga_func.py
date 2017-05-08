#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 14:29:00 2017

@author: mario
"""
import parameters_opt_ga as param
import random
import numpy as np

import fs_intersec_finding_func
import fs_cities_dist_func

from deap import base, tools

toolbox=base.Toolbox()

### Registro de Funciones de Modulo DEAP######################################
toolbox.register("select1", tools.selRoulette) 
toolbox.register("select2", tools.selBest)
toolbox.register("mate", tools.cxOrdered)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)


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

##########################Funcion Objetivo#################################

def evaluation(individual):
    "Selecciona y calcula la Funcion Objetivo de un individuo"
#        print individual

###########################Region de Interes###############################    

    ROI_algae_sampled = 0

    for idx,indiv in enumerate(individual):
        if idx < len(individual)-1:
##                print individual[idx], individual[idx+1]
##                print "===="
#                print arr_sampled_grid_pattern[idx][idx+1]
            ROI_algae_sampled = ROI_algae_sampled + (
                    param.arr_sampled_grid_pattern[param.arr_subgroup[
                            individual[idx]]][param.arr_subgroup[individual[
                                    idx+1]]])

##        print ROI_algae_sampled

###############verificacion en matriz de rutas validas#####################
    

#####################Calculo de intersecciones#############################

    tot_intersec_count = 0 # contador de intersecciones en individuos
    tot_intersec_count = fs_intersec_finding_func.invalid_route_count(
            individual, param.arr_allowed_routes, param.arr_subgroup)
   
#==============================================================================
##                     1-  Death Penalty + Penalty Factor - km2
#==============================================================================

    if param.FIT_FUNC_TYPE == 1:        
        if tot_intersec_count > 0:
            answer2 = (-1,)
        else:
            answer2 = ((1-float(tot_intersec_count)/(param.N_BEACON-1))*(
                          param.FRANJA*fs_cities_dist_func.total_distance(
                                  create_tour(individual))-(param.FRANJA**2)*
                                      tot_intersec_count)*100/param.LAKE_SIZE,)

 
#==============================================================================
#                      2- Penalty Factor - coverage %
#==============================================================================

    elif param.FIT_FUNC_TYPE == 2:
        answer2 = ((1-float(tot_intersec_count)/(len(individual)-1))*(
                       param.FRANJA*fs_cities_dist_func.total_distance(
                               create_tour(individual))-(param.FRANJA**2)*
                                   float(tot_intersec_count))*100/param.LAKE_SIZE,)        

#==============================================================================
##                     3- Exponential Penalty Factor - coverage %
#==============================================================================
    elif param.FIT_FUNC_TYPE == 3:    
        answer2 = (np.exp(-tot_intersec_count/8)*(
                       param.FRANJA*fs_cities_dist_func.total_distance(
                               create_tour(individual))-(param.FRANJA**2)*
                                   tot_intersec_count)*100/param.LAKE_SIZE,)        


#==============================================================================
##                      4- Penalty Factor - size km2       
#==============================================================================
    elif param.FIT_FUNC_TYPE == 4:
        answer2 = ((1-float(tot_intersec_count)/(param.N_BEACON-1))*(
                  param.FRANJA*fs_cities_dist_func.total_distance(create_tour(
                          individual))-(param.FRANJA**2)*tot_intersec_count),)        
   
    
    
#==============================================================================
# #                     5-Penalty Factor - ROI        
#==============================================================================
    elif param.FIT_FUNC_TYPE == 5:
        answer2 =((1-float(tot_intersec_count)/(len(individual)-1))*
                  ROI_algae_sampled,)

#==============================================================================
# #                    6-  Death Penalty - ROI        
#==============================================================================
    elif param.FIT_FUNC_TYPE == 6:
        if tot_intersec_count > 0:
            answer2 = (-1,)
        else:
            answer2 =(ROI_algae_sampled,)
    
    else:
        print 'FIT_FUNC_TYPE ERROR!'
    
    
    return answer2 # El fitness siempres es una tupla


def genetic_algorithm(pop):
    "Implementacion del GA en una poblacion dada (pop)"
    
    print "Start of the Genetic Algorithm"
    
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
    
##    print evaluation(best_ind), max(fits)
    
    last_pop = pop
    

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
toolbox.register("evaluate",evaluation)

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
            
        
    
    
    
    
