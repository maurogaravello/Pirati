#!/usr/bin/env python

import numpy

#
# function for solving the 2d parabolic equation
# \pt u = \Delta u + f1(t) + f2(t,x, y) u
# with an explicit method
# and with 0 Newmann boundary conditions
#
def one_step_parabolic(u, x, y, f1, f2, dx, dy, dt):
    """
    This function performs a one time step for the parabolic equation
    \partial_t u = \Delta u + f1 + f2(x,y) * u
    with zero Neumann boundary condition

    :param u: numpy 2d array describing the state at time t
    :param x: numpy 2d array describing the x-mesh. Same shape as u
    :param y: numpy 2d array describing the y-mesh. Same shape as u
    :param f1: float. 
    :param f2: function of x and y. It returns a 2d array of the same shape of u
    :param dx: float. The size of the x-mesh
    :param dy: float. The size of the y-mesh
    :param dt: float. The time step. It should satisfy a stability condition

    :output u_new: numpy 2d array of the same shape as u describing the state at
                   time t + dt
    """
    assert (numpy.shape(u) == numpy.shape(x))
    assert (numpy.shape(u) == numpy.shape(y))
    c = dt / (min(dx**2, dy**2))
    assert(c < 0.5)
    
    u = augment(u)

    # Calculate the numerical Laplacian
    u_xx = (1. / (dx**2)) * (u[1:-1, 2:] + u[1:-1, :-2] - 2 * u[1:-1, 1:-1])
    u_yy = (1. / (dy**2)) * (u[2:, 1:-1] + u[:-2, 1:-1] - 2 * u[1:-1, 1:-1])

    u_new = u[1:-1, 1:-1] + dt * (u_xx + u_yy + f1 + f2(x, y) * u[1:-1, 1:-1])

    return u_new


def one_step_hyperbolic():
    pass


def augment(u):
    """
    This function takes a 2D numpy array u of shape (u1, u2)
    and produces a 2D numpy array of shape (u1 + 2, u2 + 2)
    for taking care of zero Newmann boundary conditions
    """
    (u1, u2) = numpy.shape(u)
    v = u[1,:].reshape((1, u2))
    u = numpy.concatenate((v,u), axis = 0)

    v = u[-2,:].reshape((1, u2))
    u = numpy.concatenate((u,v), axis = 0)

    v = u[:,1].reshape((u1 + 2, 1))
    u = numpy.concatenate((v,u), axis = 1)

    v = u[:,-2].reshape((u1 + 2, 1))
    u = numpy.concatenate((u,v), axis = 1)

    return u



