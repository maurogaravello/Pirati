#!/usr/bin/env python

#######################################
# test.py
#
# 
# 
# 
#######################################


import numpy
import sys
import os
import argparse
import logging
from datetime import datetime
import scipy.signal
import matplotlib
import matplotlib.pyplot


path = os.path.join(os.getcwd(), "lib")
sys.path.insert(0, path)

import pirates

def ff(x, y):    
    # return numpy.maximum(1. - x**2 - y**2, 0.)
    return numpy.maximum(1. - numpy.absolute(y), 0.)

if __name__ == '__main__':

    desc = """test.py"""

    parser = argparse.ArgumentParser(description = desc, prog = "test.py")
    parser.add_argument('DirName', type=str, help="Enter the name of the directory")

    args = parser.parse_args()

    dirName = 'simulations/prova'
    dirName = args.DirName
    execfile(os.path.join(dirName, "parameters.py"))


    simul_pirates = pirates.pirates(x_1, x_2, y_1, y_2, n_x, n_y, M, tMax, d_o,
                                    InitialDatum_rho, InitialDatum_A,
                                    speed_ships, nu, dirName, mathcal_K, cut_off_C)


    prova = ff(simul_pirates.x_mesh - 5., simul_pirates.y_mesh- 10.)

    grad_py, grad_px = numpy.gradient(prova, simul_pirates.dy, simul_pirates.dx)

    print numpy.amax(grad_py)

    f1 = matplotlib.pyplot.figure(1)

    matplotlib.pyplot.contourf(simul_pirates.x_mesh, simul_pirates.y_mesh, grad_py, 100)
    matplotlib.pyplot.colorbar()
    
    matplotlib.pyplot.show(f1)
    matplotlib.pyplot.close(f1)

    
    exit(1)
    
    x1 = simul_pirates.x - (simul_pirates.x_1 + simul_pirates.x_2)/2.
    y1 = simul_pirates.y - (simul_pirates.y_1 + simul_pirates.y_2)/2.
    
    
    ker = simul_pirates.kernel_mathcal_K
    print numpy.shape(ker)
    print numpy.shape(simul_pirates.initial_density_ships)
    
    p_convolution = simul_pirates.dx * simul_pirates.dy * scipy.signal.convolve2d(simul_pirates.initial_density_ships, ker, mode='same')

    # grad = numpy.gradient(p_convolution)
    grad_y, grad_x = numpy.gradient(p_convolution, simul_pirates.dx, simul_pirates.dy)

    print simul_pirates.dx, simul_pirates.dy
    print numpy.shape(grad_x)
    print numpy.shape(grad_y)

    print numpy.shape(p_convolution)

    f1 = matplotlib.pyplot.figure(1)

    matplotlib.pyplot.contourf(simul_pirates.x_mesh, simul_pirates.y_mesh, simul_pirates.initial_density_ships, 10)
    matplotlib.pyplot.colorbar()
    
    matplotlib.pyplot.show(f1)
    matplotlib.pyplot.close(f1)

    norm = numpy.sqrt(grad_y**2 + grad_x ** 2)

    print numpy.shape(norm)


    f2 = matplotlib.pyplot.figure(2)

    matplotlib.pyplot.contourf(simul_pirates.x_mesh, simul_pirates.y_mesh, norm, 50)
    matplotlib.pyplot.colorbar()
    
    matplotlib.pyplot.show(f2)
    matplotlib.pyplot.close(f2)


