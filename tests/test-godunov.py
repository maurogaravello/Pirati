#!/usr/bin/env python
###
### test-godunov.py
### 

import sys
import os
import argparse
import numpy
import logging
from datetime import datetime


path = os.path.join(os.getcwd(), "lib")
sys.path.insert(0, path)

import pirates
import pde
import save

def evolution(pirates):
    """
    This function performs the evolution for the whole system

    :param pirates: pirate class

    The output is a tuple (p_new, s_new, police_new) of three elements.
    :output p_new: numpy 2d array of the same shape as p_density
                   describing the density of pirates at time t + dt
    :output s_new: numpy 2d array of the same shape as s_density
                   describing the density of ships at time t + dt
    :output police_new: list of final position of police vessels
    """

    p_density = pirates.initial_density_pirates
    s_density = pirates.initial_density_ships
    police = pirates.police_initial_positions

    print_number = 1
    for i in xrange(1, len(pirates.time)):

        # evolution from t to t + dt
        (p_density, s_density, police) = one_step_evolution(p_density, s_density, police, pirates.x_mesh, pirates.y_mesh,
                                                            pirates.kernel_mathcal_K, pirates.cut_off_C, pirates.dx, pirates.dy, pirates.dt, pirates.kappa, pirates.a, pirates.ships_speed, pirates.ships_direction_mesh[0], pirates.ships_direction_mesh[1])

        # printing
        if pirates.printing[i]:
        #if True:
            name = 'saving_' + str(print_number).zfill(4)
            save.solution_Save(pirates.base_directory, name, pirates.time[i], p_density, s_density, police)
            print_number += 1



def one_step_evolution(p_density, s_density, police, xx, yy,
                       p_kernel, cut_off, dx, dy, dt, kappa, a,
                       velocity, nu_x, nu_y):
    # some checks
    shape_p_density = numpy.shape(p_density)
    assert (shape_p_density == numpy.shape(s_density))
    assert (shape_p_density == numpy.shape(xx))
    assert (shape_p_density == numpy.shape(yy))
    assert (shape_p_density == numpy.shape(yy))

    
    ################################
    # Evolution of pirate density
    ################################



    p_new = p_density

    ################################
    # Evolution of ship density
    ################################

    vel_x = nu_x
    vel_y = nu_y
    s_new = pde.one_step_hyperbolic_godunov(s_density, velocity, vel_x, vel_y, dx, dy, dt)


    ################################
    # Evolution of police position
    ################################

    police_new = police

    return (p_new, s_new, police_new)



if __name__ == '__main__':

    desc = """test-godunov.py ....."""

    parser = argparse.ArgumentParser(description = desc, prog = "simulation.py")
    parser.add_argument('DirName', type=str, help="Enter the name of the directory")

    args = parser.parse_args()

    dirName = args.DirName

    filelog = os.path.join(dirName, 'Simulation-pirates.txt')

    try:
        os.remove(filelog)
    except OSError:
        pass

    logging.basicConfig(filename = filelog,
                        filemod = 'w', level = logging.DEBUG)
    
    logging.info('Started  at ' + str(datetime.now()))

    # Reads all parameters, Initial Datum, Flow and MaxCharSpeed
    execfile(os.path.join(dirName, "parameters.py"))

    
    simul_pirates = pirates.pirates(x_1, x_2, y_1, y_2, n_x, n_y, M, tMax, d_o,
                                    InitialDatum_rho, InitialDatum_A,
                                    speed_ships, nu, dirName, mathcal_K, cut_off_C, kappa, a)




    evolution(simul_pirates)

    logging.info('Finished  at ' + str(datetime.now()))
