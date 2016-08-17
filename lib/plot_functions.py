#!/usr/bin/env python
###
### plot_functions.py
### function for producing plots


NCPU = 6 # number of CPUs

import numpy
import matplotlib
import matplotlib.pyplot
import os
import glob
import sys
from multiprocessing import Pool

#
# Plotting initial data
#
def plot_initial_data(pirates, levels = 10):

    # contour plot of inital density of pirates
    plt_contour(pirates.x, pirates.y, pirates.initial_density_pirates, 'Pirate initial density', 'plot_pirate_initial_density.png', pirates.base_directory, pirates.police_initial_positions, levels)

    # contour plot of inital density of ships
    plt_contour(pirates.x, pirates.y, pirates.initial_density_ships, 'Ship initial density', 'plot_ship_initial_density.png', pirates.base_directory, pirates.police_initial_positions, levels)


#
# Plotting data at a specific time
#
def plot_data(pirates, density_pirates, density_ships, police_positions, time, levels = 10):

    # contour plot of pirate's density at time time
    plt_contour(pirates.x, pirates.y, density_pirates, 'Density of pirates at time ' + str(time), 'plot_pirate_density_' + str(time) + '.png', pirates.base_directory, police_positions, levels)

    # contour plot of ships' density at time time 
    plt_contour(pirates.x, pirates.y, density_ships, 'Density of ships at time ' + str(time), 'plot_ship_density_' + str(time) + '.png', pirates.base_directory, police_positions, levels)
    
    
#
# function for plotting contour
#
def plt_contour(x, y, function, title, name, dir, police_position, levels=10):
    matplotlib.pyplot.figure(1)

    # adjusting police positions
    px = [i[0] for i in police_position]
    py = [i[1] for i in police_position]

    # plotting contour with colorbar
    matplotlib.pyplot.contourf(x, y, function, levels)
    matplotlib.pyplot.colorbar()

    # plotting police positions as white points
    matplotlib.pyplot.plot(px, py, 'wo')

    # plotting title
    matplotlib.pyplot.title(title)

    # saving the plot
    matplotlib.pyplot.draw()
    full_name = os.path.join(dir, name)
    matplotlib.pyplot.savefig(full_name)
    matplotlib.pyplot.close(1)



#
# plot the geometric vector speed
#
def plt_geometric_vector_speed(pirates):
    h_p = 10
    v_p = 20
    x = numpy.linspace(pirates.x[0], pirates.x[-1], h_p)
    y = numpy.linspace(pirates.y[0], pirates.y[-1], v_p)
    x_mesh, y_mesh = numpy.meshgrid(x, y)
    vf = matplotlib.pyplot.figure(1)

    print numpy.ones_like(x_mesh + y_mesh)
    dx = numpy.ones_like(x_mesh + y_mesh)
    dy = numpy.zeros_like(x_mesh + y_mesh)
    matplotlib.pyplot.quiver(x_mesh, y_mesh, dx, dy)
    matplotlib.pyplot.show(vf)
    matplotlib.pyplot.close(vf)
