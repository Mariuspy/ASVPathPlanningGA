## An Event Detection and Tracking Adaptive Strategy for an Autonomous Surface Vehicle in Lake Environments using Evolutionary Computation

A simulator for finding the optimal path of an Autonomous Surface Vehicle (ASV) using Genetic Algorithm (GA) to perform monitoring of an algae blooming in a lake

__Created by__: 

Mario Arzamendia (marzamendia@ing.una.py)

Collaborators: Daniel Gutierrez
			   Sergio Toral
			   Derlis Gregor

ACETI Research Group
Department of Electronic Engineering
University of Seville

This simulator is still UNDER CONSTRUCTION!!

### 1- Introduction
The simulator implements an adaptive strategy to find and track algae bloom. It consists of two phases, an exploratory phase and an intensification phase. During the exploratory phase, the path is calculated in order to maximize the covered area by the ASV; while in the intensification phase the region where the region with bloom is intensified.
The strategy begins with the exploratory phase, then it moves to the intensification phase and it only returns to the exploratoty phase if the blooming has disappeared or decreased.

Currently, only the exploratory phase is implemented.


### 2- Additional information
This section contains information about the files/modules included in the project.

Structure of the strategy

1- Algae Sampled Grid Creator: 
It calculates how many times all the possible routes pass over the blooming.
Input: Valid routes, beacon coordinates, algae bloom pattern (grid).
Output: Matrix 60 (GRID_Y_SIZE) x 70 (GRID_Y_SIZE) .

Files:

- fs_Algae_Sampled_grid_creator_project2.py
- parameters_algae_sampled_grid.py
- alllowed_routes_positive.csv (inversa de combination.csv)
- ListaCoordenadasConvRefMetros3.csv
- arr_alg_coord_size_event_tracking (Variable)


2- Genetic Algorithm: 
It calculates the best route (individual) according to an objective function.
Input: Output from Algae Sampled Grid Creator, valid routes, beacon coordinates.
Output: 


Files:
- fs_MAinOptimYpakaraiLakeTSPGAWithAlgaeImprovementRate3.py
- fs_ga_func.py
- parameters_opt_ga.py
- arr_alg_coord_size_event_tracking (Variable)
- alllowed_routes_positive.csv (inverse of combination.csv)

