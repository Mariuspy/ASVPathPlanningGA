
INPUT1 = 'Constants/allowed_routes_positive.csv' # indica rutas validas
INPUT2 = 'Constants/ListaCoordenadasConvRefMetros3.csv' # indica coordenadas balizas
INPUT3 = 'arr_alg_pattern_size_event_tracking3.csv' # indica cuadros con mancha en grilla
INPUT4 = 'Constants/in_lake.csv'

OUTPUT1 = 'sampled_grid_event_tracking3.csv'


LAKE_SIZE_X = 12000
LAKE_SIZE_Y = 14000

# Center of Algae Bloom
#ALG_X = 25 
#ALG_Y = 55
#ALG_SIZE = 5


GRID_SIZE = 200 # metros
GRID_X_DIV = LAKE_SIZE_X/GRID_SIZE # numero de cuadros sobre el eje x
GRID_Y_DIV = LAKE_SIZE_Y/GRID_SIZE # numero de cuadros sobre el eje y

N_BEACON = 60
