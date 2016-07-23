#!/usr/bin/env python

import numpy
import scipy
import scipy.integrate


def ode(vect_field, initial_conditions, t_0, t_1):

    time = [t_0, t_1]

    res = scipy.integrate.odeint(vect_field, initial_conditions, time)

    # print res
    return res[1]

