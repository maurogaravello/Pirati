#!/usr/bin/env python
###
### simulation.py
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
import evolution

if __name__ == '__main__':

    desc = """simulation.py performs the simulation"""

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
                                    speed_ships, nu, dirName, mathcal_K, cut_off_C_pirates, kappa, a, cut_off_C_ships, cut_off_C_police, controls)

    evolution.evolution(simul_pirates)

    logging.info('Finished  at ' + str(datetime.now()))
