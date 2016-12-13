#!/usr/bin/env python

# saving procedures

import numpy
import os

# Saving to disk the solution for (rho, A, d)
def solution_Save(dirName, name, time, rho, A, d, cost):
    """This function saves the state of the simulation.

    :param dirName: string containing the path
    :param name: string. Name of the file
    :param time: float. Time of the simulation state.
    :param rho: 2d-array. Density of the pirates.
    :param A: 2d-array. Density of the ships.
    :param d: array. Position of the police vessels.
    :param cost: float. Cost at time 'time'
    """
    filename = os.path.join(dirName, name)
    
    numpy.savez_compressed(filename, t=time, r=rho, A=A, d=d, c = cost)


# Saving the cost
def cost_Save(dirName, name, cost):
    """This function saves the final cost of the simulation.

    :param dirName: string containing the path
    :param name: string. Name of the file
    :param cost: float. Cost at time 'time'
    """
    filename = os.path.join(dirName, name)
    
    numpy.savez_compressed(filename, c = cost)
    



