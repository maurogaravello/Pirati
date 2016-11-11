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
    :param f2: numpy 2d array of the same shape of u
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

    u_new = u[1:-1, 1:-1] + dt * (u_xx + u_yy + f1 + f2 * u[1:-1, 1:-1])

    return u_new


#
# function for solving the 2d hyperbolic equation
# \pt A + div(A v(A) w(t,x)) = 0
# with an explicit Lax-Friedrics method
# 
#
def one_step_hyperbolic(A, v, w_x, w_y, dx, dy, dt):
    """
    This function performs a one time step for the hyperbolic equation
    \partial_t A + div(A v(A) w(x, y)) = 0
    by a dimensional splitting and a 
    Lax-Friedrics method. It is important that the support of A
    is strictly contained in the integration domain!!
    
    :param A: numpy 2d array describing the state at time t
    :param x: numpy 2d array describing the x-mesh. Same shape as A
    :param y: numpy 2d array describing the y-mesh. Same shape as A
    :param v: function. It gives the speed of ships depending on the density
    :param w_x: numpy 2d array of the same shape of A
                describing the x component of w
    :param w_y: numpy 2d array of the same shape of A
                describing the y component of w
    :param dx: float. The size of the x-mesh
    :param dy: float. The size of the y-mesh
    :param dt: float. The time step. It should satisfy a stability condition

    :output A_new: numpy 2d array of the same shape as A describing the state at
                   time t + dt

    """



    # x-split
    f = augment(A * v(A) * w_x)
    A = augment(A)

    f_x = (1. / (2. * dx)) * (f[1:-1, 2:] - f[1:-1, :-2])
    A = .5 * (A[1:-1, 2:] + A[1:-1, :-2]) - dt * f_x 

    # y-split

    g = augment(A * v(A) * w_y)
    A = augment(A)
    
    g_y = (1. / (2. * dy)) * (g[2:, 1:-1] - g[:-2, 1:-1])
    A = .5 * (A[2:, 1:-1] + A[:-2, 1:-1]) - dt * g_y

    return A


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


#
# Godunov_Flux_x function
#
def Godunov_Flux_x(u, v, pm):
    """
    This function calculates the Godunov flux for the x-component.
    It returns a numpy 2d array (the Godunov flux).
    This numpy 2d array has size
    equal to the size of u minus 1 in the x-direction

    :param u: numpy 2d array with two ghost cells.
    Density of the state
    :param v: decreasing velocity function. The corresponding flux,
              i.e. u |---> u v(u), should be strictly concave 
    :param pm: float. Point of maximum for the flux 
    """


    
    f1 = u * v(u)
    mask_sh_pos = (u[:, :-1] <= u[:, 1:]) & (f1[:, :-1] <= f1[:, 1:])
    mask_sh_neg = (u[:, :-1] <= u[:, 1:]) & (f1[:, :-1] > f1[:, 1:])

    mask_rar_neg = (u[:, :-1] > u[:, 1:]) & (u[:, 1:] >= pm)
    mask_rar_pos = (u[:, :-1] > u[:, 1:]) & (u[:, :-1] <= pm)

    mask_pos = mask_sh_pos | mask_rar_pos
    mask_neg = mask_sh_neg | mask_rar_neg
    
    mask_theta = numpy.logical_not(mask_pos | mask_neg)

    return mask_theta * pm * v(pm) + mask_pos * f1[:, :-1] + \
           mask_neg * f1[:, 1:]

#
# Godunov_Flux_y function
#
def Godunov_Flux_y(u, v, pm):
    """
    This function calculates the Godunov flux for the y-component.
    It returns a numpy 2d array (the Godunov flux).
    This numpy 2d array has size
    equal to the size of u minus 1 in the y-direction

    :param u: numpy 2d array with two ghost cells.
    Density of the state
    :param v: decreasing velocity function. The corresponding flux,
              i.e. u |---> u v(u), should be strictly concave 
    :param pm: float. Point of maximum for the flux 
    """


    
    f1 = u * v(u)
    mask_sh_pos = (u[ :-1, :] <= u[1:, :]) & (f1[ :-1, :] <= f1[1:, :])
    mask_sh_neg = (u[ :-1, :] <= u[1:, :]) & (f1[ :-1, :] > f1[1:, :])

    mask_rar_neg = (u[ :-1, :] > u[1:, :]) & (u[1:, :] >= pm)
    mask_rar_pos = (u[ :-1, :] > u[1:, :]) & (u[ :-1, :] <= pm)

    mask_pos = mask_sh_pos | mask_rar_pos
    mask_neg = mask_sh_neg | mask_rar_neg
    
    mask_theta = numpy.logical_not(mask_pos | mask_neg)

    return mask_theta * pm * v(pm) + mask_pos * f1[ :-1, :] + \
           mask_neg * f1[1:, :]

#
# function for solving the 2d hyperbolic equation
# \pt A + div(A v(A) w(t,x)) = 0
# with an explicit Godunov-type method
def one_step_hyperbolic_godunov(A, v, w_x, w_y, dx, dy, dt):
    """
    This function performs a one time step for the hyperbolic equation
    \partial_t A + div(A v(A) w(x, y)) = 0
    by a dimensional splitting and a 
    Godunov-type method.
    
    :param A: numpy 2d array describing the state at time t
    :param x: numpy 2d array describing the x-mesh. Same shape as A
    :param y: numpy 2d array describing the y-mesh. Same shape as A
    :param v: function. It gives the speed of ships depending on the density
    :param w_x: numpy 2d array of the same shape of A
                describing the x component of w
    :param w_y: numpy 2d array of the same shape of A
                describing the y component of w
    :param dx: float. The size of the x-mesh
    :param dy: float. The size of the y-mesh
    :param dt: float. The time step. It should satisfy a stability condition

    :output A_new: numpy 2d array of the same shape as A describing the state at
                   time t + dt

    """

    # x-split
    w_x = augment(w_x)
    A = augment(A)
    w_x = 0.5 * (w_x[:, 1:] + w_x[:, :-1])

    gf = Godunov_Flux_x(A, v, 0.5) * w_x

    A = A[1:-1, 1:-1] + (dt / dx) * (gf[1:-1, :-1] - gf[1:-1, 1:])

    
    # y-split

    w_y = augment(w_y)
    A = augment(A)
    w_y = 0.5 * (w_y[1:, :] + w_y[:-1, :])

    gf = Godunov_Flux_y(A, v, 0.5) * w_y
    
    
    A = A[1:-1, 1:-1] + (dt / dy) * (gf[:-1, 1:-1] - gf[1:, 1:-1])

    return A
