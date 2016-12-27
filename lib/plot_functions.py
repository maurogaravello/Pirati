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

    v = numpy.linspace(0., 1.0, 35, endpoint=True)
    
    # plotting contour with colorbar
    # matplotlib.pyplot.contourf(x, y, function, levels)
    matplotlib.pyplot.contourf(x, y, function, v, cmap=matplotlib.pyplot.cm.jet)
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
def plt_geometric_vector_speed(pirates, h_p, v_p):
    x = numpy.linspace(pirates.x[0], pirates.x[-1], h_p)
    y = numpy.linspace(pirates.y[0], pirates.y[-1], v_p)
    x_mesh, y_mesh = numpy.meshgrid(x, y)
    vf = matplotlib.pyplot.figure(1)

    (dx, dy) = pirates.ships_direction(x, y)
    matplotlib.pyplot.quiver(x_mesh, y_mesh, dx, dy)
    matplotlib.pyplot.title('Geometric vector field $\\nu$', fontsize = 18)
    #matplotlib.pyplot.show(vf)
    matplotlib.pyplot.draw()
    full_name = os.path.join(pirates.base_directory, 'plot_gvf.png')
    matplotlib.pyplot.savefig(full_name)
    matplotlib.pyplot.close(vf)


#
# plot the kernels and the cut-off functions 
#
def plt_kernels(pirates, x, y, h_p = 50, v_p = 50, levels = 50):
    
    x_mesh, y_mesh = numpy.meshgrid(x, y)

    vf = matplotlib.pyplot.figure(1)

    # plotting contour with colorbar
    matplotlib.pyplot.contourf(x, y, pirates.mathcal_K(x, y), levels)
    matplotlib.pyplot.colorbar()

    # plotting title
    title = '$\\mathcal{K}$ kernel'
    matplotlib.pyplot.title(title)

    # saving the plot
    matplotlib.pyplot.draw()
    #matplotlib.pyplot.show(vf)
    full_name = os.path.join(pirates.base_directory, 'plot_kernel_K.png')
    matplotlib.pyplot.savefig(full_name)
    matplotlib.pyplot.close(vf)

    
    vf = matplotlib.pyplot.figure(1)

    # plotting contour with colorbar
    matplotlib.pyplot.contourf(x, y, pirates.cut_off_C(x, y), levels)
    matplotlib.pyplot.colorbar()

    # plotting title
    title = 'Cut-off function $\\mathcal{C}$'
    matplotlib.pyplot.title(title)

    # saving the plot
    matplotlib.pyplot.draw()
    #matplotlib.pyplot.show(vf)
    full_name = os.path.join(pirates.base_directory, 'plot_cut-off_C.png')
    matplotlib.pyplot.savefig(full_name)
    matplotlib.pyplot.close(vf)
    

#
# plot the solutions
#
def plt_solutions(pirates, levels = 10):

    dirName = pirates.base_directory
    
    list_files = glob.glob(os.path.join(dirName, 'saving*.npz'))
    list_files.sort()

    # plotting initial conditions
    plt_contour(pirates.x, pirates.y, pirates.initial_density_pirates, 'Pirates density at time t=0', 'pirates_plot_0000.png', pirates.base_directory, pirates.police_initial_positions, levels)
    plt_contour(pirates.x, pirates.y, pirates.initial_density_ships, 'Ships density at time t=0', 'ships_plot_0000.png', pirates.base_directory, pirates.police_initial_positions, levels)


    
    # pirates' and ships pictures
    for FileName in list_files:
        name = '_plot' + os.path.splitext(FileName)[0][1:][-5:] + '.png'
        pirate_file = 'pirates' + name
        ship_file = 'ships' + name

        # read the file
        npzf = numpy.load(FileName)
        t = npzf['t']
        p_density = npzf['r']
        s_density = npzf['A']
        police = npzf['d']
        npzf.close()


        # contour plot of density of pirates
        plt_contour(pirates.x, pirates.y, p_density, 'Pirates density at time t=' + str("%.3f" %t), pirate_file, dirName, police, levels)

        # contour plot of inital density of ships
        plt_contour(pirates.x, pirates.y, s_density, 'Ships density at time t=' + str("%.3f" %t), ship_file, dirName, police, levels)

#
# final movie
#
def movie(pirates):
    pirate = os.path.join(pirates.base_directory, 'pirates_plot*')
    movie_p = os.path.join(pirates.base_directory, 'movie_pirates.mpg')
    ship = os.path.join(pirates.base_directory, 'ships_plot*')
    movie_s = os.path.join(pirates.base_directory, 'movie_ships.mpg')
    
    os.system("mencoder 'mf://'" + pirate + " -mf type=png:fps=5 -ovc lavc -lavcopts vcodec=wmv2 -oac copy -o " + movie_p)
    os.system("mencoder 'mf://'" + ship + " -mf type=png:fps=5 -ovc lavc -lavcopts vcodec=wmv2 -oac copy -o " + movie_s)
