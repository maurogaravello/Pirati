#!/usr/bin/env python
###
### plt_solution.py
### plots the solution computed by JR_solution.py and by S_solution.py

### JSRnnnn.png: curves J, S, R at fixed time t
### Tot.png   :  integral J(t,a) da, S(t,a) da and R (t,a) da as a function of t
### film.mpg  : mpg of JSRnnnn.png

NCPU = 6 # number of CPUs

import numpy
import matplotlib
import matplotlib.pyplot
import os
import glob
import sys
from multiprocessing import Pool

def plot_initial_data(pirates):
    plt_contour(pirates.x, pirates.y, pirates.initial_density_pirates, 'prova', 'plot.png', pirates.base_directory)


def plt_contour(x, y, function, title, name, dir):
    matplotlib.pyplot.figure(1)

    matplotlib.pyplot.contour(x, y, function)
    # plt.clabel(CS, inline=1, fontsize=10)
    matplotlib.pyplot.title(title)
    matplotlib.pyplot.draw()
    full_name = os.path.join(dir, name)
    matplotlib.pyplot.savefig(full_name)




