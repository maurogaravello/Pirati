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

import pde

def v(A):
    return 1. - A

if __name__ == '__main__':

    A = numpy.zeros((5,6))
    A[1,2] = .5
    A[2,2] = .5
    
    w_x = numpy.ones((5,6))
    w_y = numpy.zeros((5,6))
    dx = 0.2
    dy = 0.25
    dt = 0.25 * min(dx**2, dx / 1.)
    

    A_new = pde.one_step_hyperbolic(A, v, w_x, w_y, dx, dy, dt)

    print A_new
