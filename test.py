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

path = os.path.join(os.getcwd(), "lib")
sys.path.insert(0, path)

import ode

if __name__ == '__main__':

    desc = """test.py find the solution using
    a given control. The solution is computed by using a
    numerical method based on the exact expression of
    the solution."""

    parser = argparse.ArgumentParser(description = desc, prog = "test.py")
    # parser.add_argument('DirName', type=str, help="Enter the name of the directory")
    # parser.add_argument('-n', '--number', type = int, help = "Enter the number of the control", default = 0)
    # parser.add_argument('-p', '--processors', type = int, help = "Number of processors for the plotting", default = 1)

    args = parser.parse_args()


    def vect_field(y, t):
        return y

    t_0 = 0.
    t_1 = 5.
    y_0 = 2.

    prova = ode.ode(vect_field, y_0, t_0, t_1)

    print prova
