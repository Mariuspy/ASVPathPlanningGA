
import parameters_opt_ga as param
import numpy as np

def find_orientation(point, segment1, segment2):
    "Find the orientation ccw or cw respect to a segment."


    ori_dest = [float(segment1[0])-float(segment2[0]), float(
                segment1[1])-float(segment2[1])] 
    ori_point = [float(point[0])-float(segment2[0]), float(
                 point[1])-float(segment2[1])]
    
    if np.cross(ori_point,ori_dest) > 0:
        orientation = 1
    elif np.cross(ori_point,ori_dest) < 0:
        orientation = -1
    else:
        orientation = 0

    return orientation


def find_between_points(pt,p1,p2):
    "Find if pt is in segment p1p2"

    inside = 0
    x1 = float(p1[0])
    y1 = float(p1[1])
    x2 = float(p2[0])
    y2 = float(p2[1])
    xt = float(pt[0])
    yt = float(pt[1])

    if (x2>x1):
        if (y2>y1):        
            if  ((x1<=xt<=x2) and (y1<=yt<=y2)):
                inside = 1

        else:
            if  ((x1<=xt<=x2) and (y1>=yt>=y2)):
                inside = 1

    else:
        if (y2>y1):
            if  ((x2<=xt<=x1) and (y1<=yt<=y2)):

                inside = 1
##                print "this3"
        else:
            if  ((x1>=xt>=x2) and (y2<=yt<=y1)):
                inside = 1
##                print "this4"

    return inside

    
################################################################################3


##print list_coord[0],list_coord[29],list_coord[40],list_coord[15]


def find_intersec(origen1,destino1,origen2,destino2):

#==============================================================================
#     O1_x = float(origen1[0])
#     O1_y = float(origen1[1])
#     D1_x = float(destino1[0])
#     D1_y = float(destino1[1])
#     O2_x = float(origen2[0])
#     O2_y = float(origen2[1])
#     D2_x = float(destino2[0])
#     D2_y = float(destino2[1])
#==============================================================================

    orientation1 = orientation2 = orientation3 = orientation4 = 0
    intersection1 = intersection2 = intersection3 = intersection4 = 0

    intersection_flag = 0
    
##################Verificacion Respecto Origen 2 y Destino 2#######################################
##

#####################Referencia Origen 2############################################################

    orientation1 = find_orientation(origen1, destino2, origen2)  # verifica origen1 respecto origen2-destino2
    orientation2 = find_orientation(destino1, destino2, origen2) # verifica destino1 respecto origen2-destino2

##################Verificacion Respecto Origen 1 y Destino 1#######################################

#####################Referencia Origen 1############################################################

    orientation3 = find_orientation(origen2, destino1, origen1) # verifica origen2 respecto origen1-destino1
    orientation4 = find_orientation(destino2, destino1, origen1) # verifica destino2 respecto origen1-destino1


    if orientation1 == 0:
        intersection1 = find_between_points(origen1, destino2, origen2) # verifica si destino2 entre origen1 y destino1

    if orientation2 == 0:
        intersection2 = find_between_points(destino1, destino2, origen2) # verifica si destino2 entre origen1 y destino1

    if orientation3 == 0:
        intersection3 = find_between_points(origen2, destino1, origen1) # verifica si destino2 entre origen1 y destino1

    if orientation4 == 0:
        intersection4 = find_between_points(destino2, destino1, origen1) # verifica si destino2 entre origen1 y destino1


    if (intersection1 == 1 or intersection2 == 1 or intersection3 ==1 or intersection4 == 1) or ((orientation1 != orientation2 and orientation3 != orientation4) and (orientation1*orientation2*orientation3*orientation4)):
        intersection_flag = 1
    else:
        intersection_flag = 0

##    print intersection1 == 1 or intersection2 == 1 or intersection3 ==1 or intersection4 == 1
##    print orientation1 != orientation2 and orientation3 != orientation4
        

    return intersection_flag


##################################################################################


##################################################################################
def create_rect_sides(center):
    "Retorna las esquinas del cuadrado cuyo centro es introducido"
    center_x = center[0]
    center_y = center[1]
    s1 = (center_x-param.GRID_SIZE/2, center_y-param.GRID_SIZE/2)
    s2 = (center_x-param.GRID_SIZE/2, center_y+param.GRID_SIZE/2)
    s3 = (center_x+param.GRID_SIZE/2, center_y+param.GRID_SIZE/2)
    s4 = (center_x+param.GRID_SIZE/2, center_y-param.GRID_SIZE/2)
    return s1, s2, s3, s4


##print create_rect_sides(arr_centers_coord[10,10])
##print len(create_rect_sides(arr_centers_coord[10,10]))


##def check_intersection(ruta, center, bal_ori, bal_dest,grid_x,grid_y): #To graph the sampled path
def check_intersection(ruta, center):
    "Dada una ruta y un centro de cuadrado, verifica si la ruta pasa por el cuadrado"

##    print ruta
    origen = ruta[0]
    destino = ruta[1]
    
    corners = create_rect_sides(center)
    intersec_flag = 0
##    print corners

    for idx in range(len(corners)):
##        print idx, len(corners)-1
        if idx != len(corners)-1:
##            print corners[idx],corners[idx+1], find_intersec(origen,destino,corners[idx], corners[idx+1])
            if find_intersec(origen, destino, corners[idx], corners[idx+1]):
                intersec_flag += 1
                
        else:
##            print corners[-1],corners[0], find_intersec(origen,destino,corners[-1], corners[0])
            if find_intersec(origen, destino, corners[-1], corners[0]):
                intersec_flag += 1

    return intersec_flag                
##    print bal_ori,bal_dest, arr_sampled_grid[bal_ori][bal_dest]
#==============================================================================
#     if intersec_flag == 2 and arr_sampled_grid_pattern[bal_ori][bal_dest]<1:
# ##        print grid_x,grid_y
#         arr_sampled_grid_pattern[bal_ori][bal_dest]+=1
#==============================================================================
##        arr_sampled_grid[grid_x][grid_y]+=1 # To graph the sampled path
##        print x,y
##    elif intersec_flag >2:
##        print "ERROR!"


##ruta_test = [list_coord[49],list_coord[15]]
##centro_test = arr_centers_coord[20][40]

##print ruta_test
##print centro_test

##check_intersection(ruta_test,centro_test)

##print arr_centers_coord[59][69]

def intersec_count_f(indiv, intersec_routes, arr_subgroup):
    "Cuenta la cantidad de intersecciones de un individuo."

    short_indiv = [] # lista parcial de indiv
    last_route = 0   # ultima ruta en short_indiv
    intersec_count = 0 # contador de intersecciones de rutas en individuo

    
    for idx, element in enumerate(indiv):   # Creacion de nueva lista
        short_indiv = arr_subgroup[indiv[:idx+1]]         # Agrega gradualmente los elementos del individuo y
                                            # chequea la cantidad de interseccioens hasta ese punto

        if len(short_indiv)>2: # Solo evalua si la lista tiene mas de 2 elementos
            last_route = param.N_BEACON*short_indiv[-2] + short_indiv[-1] 
            test_route = 0 # Ruta para verificar interseccion
            
            for idx2, element3 in enumerate(short_indiv): # Seleccion de baliza
                if idx2 < len(short_indiv)-2: # Todas las rutas excepto la ultima
                    test_route = param.N_BEACON*short_indiv[idx2] + short_indiv[
                            idx2+1]
                    intersec_count += int(intersec_routes[
                            last_route][test_route])
            
    return intersec_count

def invalid_route_count(indiv, allowed_routes, arr_subgroup):
    "Cuenta la cantidad de rutas invalidas de un individuo."

    n_ruta_inval = 0 # contador de rutas invalidas en individuo

    for idx, ind in enumerate(indiv): # verificacion en matriz de rutas validas
        if idx != (len(indiv)-1):
            if int(allowed_routes[arr_subgroup[indiv[idx]]][arr_subgroup[indiv[
                    idx+1]]]) == 1:
                n_ruta_inval += 1
                
    return n_ruta_inval
