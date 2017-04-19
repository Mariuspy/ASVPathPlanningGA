#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 14:31:13 2017

@author: mario
"""
import matplotlib.pyplot as plt

##########Cities and Distance Representation#######################
def distance(A, B): 
    "Calcula la distancia euclediana entre 2 balizas."
    return abs(A - B)


def total_distance(tour):
    "Distancia total del tour"
    return sum(distance(tour[i], tour[i-1]) 
               for i in range(len(tour)))

def plot_tour(tour, alpha=1, color=None):
    "Dibujo del tour con lineas azules entre circulos azules, y la baliza inical como cuadrado rojo."
    plotline(list(tour), alpha=alpha, color=color)
    plotline([tour[0]], 'rs', alpha=alpha)
    
    
def plotline(points, style='bo-', linewidth = 1.0, alpha=1, color=None):
    "Dibujo de una lista de puntos (numeros complejos) en el plano 2-D."
    X, Y = XY(points)
    
    if color:
        plt.plot(X, Y, style, linewidth = linewidth, alpha=alpha, color=color)
    else:
        plt.plot(X, Y, style, linewidth = linewidth, alpha=alpha)
    
def XY(points):
    "Dado una lista depuntos, retorna dos listas: Coordenadas X y Coordenadas Y."
    return [p.real for p in points], [p.imag for p in points]


def plot_contour(tour, alpha=1, color=None):
    "Dibujo de contrno de lago"
    plotline(list(tour) + [tour[0]], style ='ro-', linewidth = 2.0, alpha=alpha, color=color)
    plt.ylabel('[meters]')
    plt.xlabel('[meters]')