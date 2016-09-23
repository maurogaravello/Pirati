#!/usr/bin/env python

import numpy
import scipy
import scipy.integrate


# def ode(vect_field, initial_conditions, t_0, t_1):

#     time = [t_0, t_1]

#     res = scipy.integrate.odeint(vect_field, initial_conditions, time)

#     # print res
#     return res[1]


def ode(F_x, F_y, position, dt):
    """
    This function performs a one time step for the ODE
    \dot z = F
    in a two-dimensional domain
    by the explicit Euler forward method with time step dt
    
    :param F_x: float. The x-component of the vector field
    :param F_y: float. The y-component of the vector field
    :param position: list of two elements. It is the initial position in R^2
    :param dt: float. The time step.

    :output (new_position_x, new_position_y): tuple of two floats. It represents
                          the position at final time 
    """
    new_position_x = position[0] + dt* F_x
    new_position_y = position[1] + dt* F_y

    return (new_position_x, new_position_y)
