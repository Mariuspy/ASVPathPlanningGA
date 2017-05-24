### An Event Detection and Tracking Adaptive Strategy for an Autonomous Surface Vehicle in Lake Environments using Evolutionary Computation

A simulator for finding the optimal path of an Autonomous Surface Vehicle (ASV) using Genetic Algorithm (GA) to perform monitoring of an algae blooming in a lake

Created by:
 
- Mario Arzamendia (marzamendia@ing.una.py)

Collaborators: 

- Daniel Gutierrez

- Sergio Toral

- Derlis Gregor

ACETI Research Group - Department of Electronic Engineering - University of Seville

Laboratory of Distributed Systems - Faculty of Engineering - National University of Asuncion

**This simulator is still __UNDER CONSTRUCTION__!! **

**To execute type the following command: **.

```
python fs_MainOptimYpakaraiLakeTSPGAWithAlgaeImprovementRate3.py
```

#### 1- Introduction
The simulator implements an adaptive strategy to find and track algae bloom. It consists of two phases, an exploratory phase and an intensification phase. During the exploratory phase, the path is calculated in order to maximize the covered area by the ASV; while in the intensification phase the region where the region with bloom is intensified.
The strategy begins with the exploratory phase, then it moves to the intensification phase and it only returns to the exploratoty phase if the blooming has disappeared or decreased.

Currently, only the exploratory phase is implemented.


#### 2- Additional information
This section contains information about the files/modules included in the project.

__Structure of the strategy__

_1- Algae Sampled Grid Creator_: 
It calculates how many times all the possible routes pass over the blooming and shows it in a grid map of the lake (user defined).

_Input_: Valid routes, beacon coordinates, algae bloom pattern (grid).

_Output_: Matrix 60 (_GRID_Y_SIZE_) x 70 (_GRID_Y_SIZE_) .

_Files_:

- _fs_Algae_Sampled_grid_creator_project2.py_
- _parameters_algae_sampled_grid.py_
- _alllowed_routes_positive.csv_ (inversa de combination.csv)
- _ListaCoordenadasConvRefMetros3.csv_
- _arr_alg_coord_size_event_tracking.csv_ (Variable)


_2- Genetic Algorithm_: It calculates the best route (individual) according to an objective function.
  
_Input_: Output from Algae Sampled Grid Creator, valid routes, beacon coordinates.
  
_Output_: Best individual, fitness function value, statistics of multiple simulations (average, standard deviation).

_Files_:

- _fs_MAinOptimYpakaraiLakeTSPGAWithAlgaeImprovementRate3.py_ :Main program of the Genetic Algoritm
- _fs_ga_func.py_: Module containing GA functions
- _parameters_opt_ga.py_: Module containing parameters of the simulation.
- _combination.csv_ : Matrix N_BEACONS x N_BEACONS, indicating the valid routes between origin and destination beacon. "0" means is a valid route.
- _alllowed_routes_positive.csv_ (inverse of combination.csv): Matrix N_BEACONS x N_BEACONS, indicating the valid routes between origin and destination beacon. "1" means is a valid route.te.