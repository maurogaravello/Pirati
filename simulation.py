#!/usr/bin/env python
###
### plot_control.py
### plots the controls function in the simulation directory

import sys
import os
import argparse
import numpy

path = os.path.join(os.getcwd(), "lib")
sys.path.insert(0, path)

import plt_solution as plt



if __name__ == '__main__':

    desc = """plot_control.py plot all the controls in a simulation
    directory."""

    parser = argparse.ArgumentParser(description = desc, prog = "plot_control.py")
    parser.add_argument('DirName', type=str, help="Enter the name of the directory")

    args = parser.parse_args()

    dirName = args.DirName
    # Reads all parameters, Initial Datum, Flow and MaxCharSpeed
    execfile(os.path.join(dirName, "parameters.py"))

    plt.plotControls(dirName, tMax)
