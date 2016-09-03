#!/usr/bin/env python

import numpy
import scipy.signal
import pde
import ode

#
# function for solving the system 
# 
def one_step_evolution(p_density, s_density, police, xx, yy,
                       p_kernel, f1, f2, dx, dy, dt):
    """
    This function performs a one time step evolution for the whole system

    :param p_density: numpy 2d array describing the density of pirates at time t
    :param s_density: numpy 2d array describing the density of ships at time t
    :param xx: numpy 2d array describing the x-mesh. Same shape as p_density
               and s_density
    :param yy: numpy 2d array describing the y-mesh. Same shape as p_density
               and s_density
    :param p_kernel: numpy 2d array describing the kernel in the equation for
                     pirates. Same shape as p_density

    :param f1: float. 
    :param f2: function of x and y. It returns a 2d array of the same shape of u
    :param dx: float. The size of the x-mesh
    :param dy: float. The size of the y-mesh
    :param dt: float. The time step. It should satisfy a stability condition

    :output p_new: numpy 2d array of the same shape as p_density
                   describing the density of pirates at time t + dt
    :output s_new: numpy 2d array of the same shape as s_density
                   describing the density of ships at time t + dt
    :output police_new: 
    """
    # some checks
    shape_p_density = numpy.shape(p_density)
    assert (shape_p_density == numpy.shape(s_density))
    assert (shape_p_density == numpy.shape(xx))
    assert (shape_p_density == numpy.shape(yy))
    assert (shape_p_density == numpy.shape(yy))

    ################################
    # Evolution of pirate density
    ################################

    # 2d convolution on a fixed mesh
    # h * k [n, m] = dx * dy * convolve2d(h, k)
    p_convolution = dx * dy * scipy.signal.convolve2d(p_density, p_kernel, mode='same')
    # gradient of the convolution
    grad_py, grad_px = numpy.gradient(p_convolution, dx, dy)
    # norm of the gradient
    norm_grad_p_convolution = numpy.sqrt(grad_px**2 + grad_py**2)

    
    # term depending on the police
    f = .....

    p_new = pde.one_step_parabolic(p_density, xx, yy, ...., f, dx, dy, dt)

    ################################
    # Evolution of ship density
    ################################


    s_new = pde.one_step_hyperbolic(s_density, .........)


    ################################
    # Evolution of police position
    ################################
    
    police_new = ode.ode(.....)

