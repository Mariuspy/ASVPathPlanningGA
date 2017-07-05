 # -*- coding: utf-8 -*-p
"""
#==============================================================================
#  Fecha de Creacion: 19/04/2016
#  Descripcion: Reestructuracion del codigo
#               Realiza optimizacion con GA Considera cobertura de cuadros en 
#               zona de manchas como funcion
#  objetivo 
#  Creado a partir Optimization-YpakaraiLake-TSP-GA.py
#  Input:  Coordenadas de balizas ('ListaCoordenadasConvRefMetros.csv')
#          Patron de mancha de algas('arr_alg_pattern.csv')
#          Lista con interseccion de rutas ('intersection_routes.csv')
#  Output: Mejor individuo con metricas
#==============================================================================
"""

#==============================================================================
# ############## Graph modules ################################################
# import matplotlib
# 
# #matplotlib.use('Agg')  # Descomentar esto para guardar grafico en archivo externo
# 
# import matplotlib.pyplot as plt
# import matplotlib.colors as colors
# import matplotlib.cm as cmx
#==============================================================================

import random
# import operator
import time
# import itertools
import numpy as np
# import math
#import csv
#import inspect 

import os

from deap import base, creator, tools

import parameters_opt_ga as param
import fs_intersec_finding_func
import fs_cities_dist_func
import fs_ga_func

def print_parameters():

    #==========================================================================
    ########################Impresion de Parametros#######################
    #==========================================================================
    print 'PARAMETROS'
    
    print 'Tamano del lago (LAKE_SIZE) = ' , param.LAKE_SIZE
    print 'Numero de Balizas (N_BEACON) = ' ,  param.N_BEACON
    print 'Numero de simulaciones (N_SIM) = ' ,  param.N_SIM
    print 'Probabilidad de Cruce (CXPB) = ',  param.CXPB
    print 'Probabilidad de Mutacion (MUTPB) = ', param.MUTPB
    print 'Cantidad de generaciones (NGEN) = ', param.NGEN
    print 'Poblacion (POPU)  = ', param.POPU
    print 'Elitismo  (0 <= ELIT_RATE <= 1) = ', param.ELIT_RATE
    print 'Franja de Sensor (FRANJA) = ', param.FRANJA
    print 'Factor de Intentos para individuo (ATT_FACTOR)= ', param.ATT_FACTOR
    print 'Factor de Intentos para poblacion (ATT_POPU) = ', param.ATT_POPU
    print param.FIT_FUNC_TYPE
    
    print('\n')
    
    print 'INPUT/OUTPUT'
    
#    print 'arr_sampled_grid_pattern =', param.INPUT2 
    print 'arr_allowed_routes =', param.INPUT3
    print 'list_coord =', param.INPUT4 
    print 'intersec_routes =', param.INPUT5 
    print 'arr_pop_valid =', param.INPUT6 
    
    
    print 'best_of_best =', param.OUTPUT1 
    print 'arr_imp_rate =', param.OUTPUT2 
    print 'coverage vs generations =', param.OUTPUT3 
    print 'arr_max =', param.OUTPUT4 
    print 'best_last_pop =', param.OUTPUT5  
    
    print '======================================================================='

def main(fit_func_type, arr_subgroup,arr_routes_AB_est_intersec,
         dict_routes_AB_est_intersec):
    
    print 'Start GA', time.ctime() # Para registrar duracion de simulacion
    print 'File name = ' , os.path.basename(__file__) # Para registrar nombre de 
                                                      # script
    
    random.seed(time.time()) # genera semilla aleatoria
    

    
    fs_ga_func.assign_eval_parameters(fit_func_type, arr_routes_AB_est_intersec, 
                                      arr_subgroup,dict_routes_AB_est_intersec)
    
    #==========================================================================
    #     ### Inicio de simulaciones múltiples
    #==========================================================================

    
#==============================================================================
#     best_lst_imp_rate = []
#     best_lst_max = [] # Lista de los mejores fitness de todas las generaciones
#     best_lst_ave = [] # Lista de los fitness promedio de todas las generaciones
#==============================================================================
    tot_best_ind = [] # Lista de los mejores individuos de todas las generaciones
    best_of_best = [] # Mejor individuo de todas las simulaciones
    best_evaluation = 0 # Fitness del mejor individuo
    best_sim = 0
    
    
    for sim in range(param.N_SIM):
    
        valid_gen2 = 0    
    
    #==========================================================================
    #     ### Genera una población inicial valida
    #==========================================================================

        
        pop_valid = fs_ga_func.pop_valid_creation(arr_subgroup)
        np.savetxt('Results/initial_pop_test.csv', pop_valid, fmt = '%i', 
                   delimiter=",")
        
        
    
    #==========================================================================
    #####################Importacion de poblacion externa######################
    #     
    #     arr_pop_valid = np.loadtxt(param.INPUT6, dtype = 'uint8', 
    #                                      delimiter =',')
    #     pop_valid_import = arr_pop_valid.tolist()
    # 
    # #    print 'pop valid import', type(pop_valid_import), pop_valid_import
    #     
    # #    print pop_valid, 'This'
    # 
    #==========================================================================

        
        toolbox = base.Toolbox()
    
    #==========================================================================
    #     ### Inicializacion de las funciones del GA del modulo DEAP
    #==========================================================================
    ################Individual Representation And Evaluation###################
    
        creator.create("FitnessMin", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)
    
        toolbox.register("indices", np.random.permutation, len(arr_subgroup))
        toolbox.register(
                         "individual", tools.initIterate, creator.Individual, 
                             toolbox.indices)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    
    
    
    ################Poblacion inicial pre-definida#############################
    
        toolbox.register("individual_guess", fs_ga_func.initIndividual, 
                         creator.Individual)
        toolbox.register("population_guess", fs_ga_func.initPopulation, list, 
        toolbox.individual_guess, pop_valid)
    
    
        pop = toolbox.population_guess() # Creacion de poblacion valida
    
    #    pop = toolbox.population(param.POPU) # Creacion de poblacion aleatoria

    ################ Llamado a la funcion GA###################################
        (best_individual, evaluation2, worst_individual, lst_max, lst_ave, 
             lst_imp_rate, valid_gen2, last_pop_ga) = fs_ga_func.genetic_algorithm(
                     pop)
        
        
        best_ind_final = [] # conversion de balizas de GA a balizas reales
        for element in best_individual:
            best_ind_final.append(arr_subgroup[element])    
        
#        print best_individual
#        print fs_intersec_finding_func.invalid_route_count(
#            best_individual, param.arr_allowed_routes, arr_subgroup)
#==============================================================================
#         arr_imp_rate = np.array(lst_imp_rate)
#         arr_max = np.array(lst_max)
#==============================================================================
        
        
    #==============================================================================
    #########Almacenamiento de la tasa de mejoras de la simulacion en archivo
    ######### externo
    ###########################################################################
    #
    #     if os.path.isfile(param.OUTPUT2):
    #         with open(param.OUTPUT2,'a') as f_handle:
    #             np.savetxt(f_handle, arr_imp_rate[None,:],fmt = '%.3f', delimiter = ',')
    #     
    #     else:
    #         np.savetxt(param.OUTPUT2, arr_imp_rate[None,:],fmt = '%.3f', delimiter = ',')
    #         
    #     
    #     if os.path.isfile(param.OUTPUT4):
    #         with open(param.OUTPUT4,'a') as f_handle:
    #             np.savetxt(f_handle, arr_max[None,:],fmt = '%.3f', delimiter = ',')
    # 
    #     else:
    #         np.savetxt(param.OUTPUT4, arr_max[None,:],fmt = '%.3f', delimiter = ',')
    #==============================================================================
        
    ### 11- Imprime los resultados del GA.
        print 'Simulation', sim
        print best_ind_final
    #    print 'Fitness = ',round((evaluation(best_individual)[0]),3)
        print 'Fitness = ', round(evaluation2,3)
        print 'Rutas invalidas = ', fs_intersec_finding_func.invalid_route_count(
                best_individual,param.arr_allowed_routes,arr_subgroup)
    #    print '1ra Generacion con ruta valida = ', valid_gen2
    #    tot_best_ind.append(evaluation(best_individual)[0])
        tot_best_ind.append(evaluation2)    
    
    
    
    #########Eleccion de la simulacion con el mejor resultado#################################
        if evaluation2 > best_evaluation:
    #    if evaluation(best_individual)[0] > best_evaluation:
    #        best_evaluation = evaluation(best_individual)[0]
            best_evaluation = evaluation2
            best_of_best = best_ind_final
            best_of_best_order = best_individual
#==============================================================================
#             best_lst_max = lst_max
#             best_lst_ave = lst_ave
#             best_lst_imp_rate = lst_imp_rate
#==============================================================================
            best_sim = sim
            best_last_pop = last_pop_ga
        print('\n')
        
    
    ### 13- Imprime los resultados de la mejor simulación.
    #########Impresion de resultados###########################################
    
    print 'BEST OF SIMULATIONS'
    print best_of_best
    print 'Best fitness =', round(best_evaluation,3)
    
    print '\n'
    
    
    #np.savetxt(param.OUTPUT1, best_of_best, fmt = '%i', delimiter=",")
    
    np.savetxt(param.OUTPUT5, best_last_pop, fmt = '%i', delimiter=",")
    
    arr_tot_best_ind = np.array(tot_best_ind) 
    
    best_n_rutas_inval = 0
    
    for idx, indiv in enumerate(best_of_best): # verificacion en matriz de rutas validas
                if idx != (len(best_of_best)-1):
                    if int(param.arr_allowed_routes[best_of_best[idx]][
                           best_of_best[idx+1]]) == 1:
                       best_n_rutas_inval += 1
    
    
    print 'Rutas Invalidas = ', (best_n_rutas_inval,
                                 fs_intersec_finding_func.invalid_route_count(
                                         best_of_best_order,
                                         param.arr_allowed_routes, arr_subgroup))
#==============================================================================
#     ROI_count = 0
# 
#     for idx,indiv in enumerate(best_of_best_order):
#             if idx < len(best_of_best)-1:
#     ##                print individual[idx], individual[idx+1]
#     ##                print "===="
#     #                print arr_sampled_grid_pattern[idx][idx+1]
#                 ROI_count = ROI_count + (
#                         arr_routes_AB_est_intersec[best_of_best[idx]][best_of_best[
#                                         idx+1]])
#     
#     
#     print 'ROI', ROI_count
#==============================================================================
    
    print 'Average = ', round(np.average(arr_tot_best_ind),3)
    
    print 'Standard Deviation = ', round(np.std(arr_tot_best_ind),3)
    
    print 'Best Simulation = ', best_sim
    
    #==============================================================================
    # ###Registro de resultados de lista de promedios y mejores valores
    # ###de fitness en archivos externos.
    # ###Lo uso cuando corro multiples simulaciones en servidor y lo
    # ###grafico en mi maquina.
    # #########################################################################
    #
    # file = open("lst_max_ga_restrict41.txt","w")
    # file.write(time.ctime())
    # file.write('\n')
    # file.write(os.path.basename(__file__))
    # file.write('\n')
    # for element in best_lst_max:
    #     file.write(str(element)+',')
    # file.close()
    #
    # file = open("lst_ave_ga_restrict41.txt","w")
    # file.write(time.ctime())
    # file.write('\n')
    # file.write(os.path.basename(__file__))
    # file.write('\n')
    # for element in best_lst_ave:
    #     file.write(str(element)+',')
    # file.close()
    #==============================================================================
    
    print 'Distance = ', round(fs_cities_dist_func.total_distance(
            fs_ga_func.create_tour(best_of_best)))

    
#    print best_of_best_order, arr_subgroup
    
    print 'Intersections = ' , fs_intersec_finding_func.intersec_count_f(
            best_of_best_order, param.intersec_routes, arr_subgroup) 
    
    
    #==============================================================================
    # #####Graficos################################################################
    # fig = plt.figure()
    # 
    # ax1 = plt.subplot(211)
    # plt.ylabel('Improvement rate[%]')
    # #plt.xlabel('Generations')
    # plt.plot(best_lst_imp_rate)
    # 
    # plt.subplot(212 )
    # plt.ylabel('Coverage[%]')
    # plt.plot(best_lst_max)
    # 
    # plt.xlabel('Generations')
    # plt.tight_layout()
    # 
    # fig.savefig(param.OUTPUT3, dpi = 600)
    # 
    # #plt.show()
    #==============================================================================
    
    print "C'est Fini"
    print 'End GA',time.ctime()
    print '\n'
    
    #==============================================================================
    # ##### 14- Grafica los resultados de la mejor simulación
    # ##################Graficos ###############################################3
    # ##contour = range(60)
    # ####fig, ax = plt.subplots()
    # ####ax.yaxis.set_major_formatter(formatter)
    # ####ax.xaxis.set_major_formatter(formatter)
    # ##
    # ##plt.figure(figsize= (20,7.5))
    # ##
    # ##plt.subplot(121)
    # ##plt.grid(b=True, which='both', color='0.65',linestyle='-')
    # ##plot_contour(create_tour(contour, cities))
    # ##plot_tour(create_tour(best_of_best,cities))
    # ####plt.plot(cities[48].real, cities[48].imag, c='g', marker='s')
    # ##
    # ##
    # ##
    # ##
    # ####fig, ax = plt.subplots()
    # ####ax.yaxis.set_major_formatter(formatter)
    # ##plt.subplot(122)
    # ##plt.ylabel('Fitness[square meters]')
    # ##plt.xlabel('Generations')
    # ##plt.plot(best_lst_max,'r-', antialiased=True, label = 'Best')
    # ##plt.plot(best_lst_ave,'b-', antialiased=True, label = 'Average')
    # ####plt.legend('Best fitness','Mean fitness')
    # ##plt.legend(loc = 4)
    # ####plt.ylim((8500000,11000000))
    # ####plt.xlim((0,2000))
    # ##
    # ##plt.grid(b=True, which='both', color='0.65',linestyle='-')
    # ##plt.show()
    #==============================================================================
    
    return best_of_best
    

if __name__ == '__main__':
    main()
    