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
import plot_functions as plt

def check_negative(value):
    """ check if a value is negative"""
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("%s is an invalid entry" % value)

    return ivalue



if __name__ == '__main__':

    desc = """plot.py is the main program for plotting the simulation"""

    parser = argparse.ArgumentParser(description = desc, prog = "simulation.py")
    parser.add_argument('DirName', type=str, help="Enter the name of the directory")

    # initial data
    parser.add_argument('-id', '--initial_data', dest='init_data', action='store_true')
    parser.add_argument('-l', '--levels_color', type = check_negative, help="Enter the number of working processors", default = 10)

    # geometric vector field    
    parser.add_argument('-gvf', '--geometric_vector_field', dest='geometric_vector_field', action='store_true', help='Plot the geometric vector field')
    parser.add_argument('-vf_x', '--horizontal_points_vf', type = check_negative, help="Enter the number of horizontal points for the vector field", default = 10)
    parser.add_argument('-vf_y', '--vertical_points_vf', type = check_negative, help="Enter the number of vertical points for the vector field", default = 10)

    parser.add_argument('-p', '--processors', type = check_negative, help="Enter the number of working processors", default = 1)

       
    args = parser.parse_args()
    
    

    dirName = args.DirName

    filelog = os.path.join(dirName, 'Plot-pirates.txt')

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
                                    speed_ships, nu, dirName)


    if args.init_data:
        plt.plot_initial_data(simul_pirates, args.levels_color)

    if args.geometric_vector_field:
        plt.plt_geometric_vector_speed(simul_pirates, args.horizontal_points_vf, args.vertical_points_vf)
