#!/usr/bin/env python

import numpy
import scipy.signal
import pde
import ode
import save
import sys
import logging
from datetime import datetime

#
# function for solving the system in a one temporal step 
# 
def one_step_evolution(p_density, s_density, police, xx, yy,
                       p_kernel, cut_off_pirates,
                       cut_off_ships, cut_off_police,
                       dx, dy, dt, kappa, a,
                       velocity, nu_x, nu_y, controls, time):
    """
    This function performs a one time step evolution for the whole system

    :param p_density: numpy 2d array describing the density of pirates at time t
    :param s_density: numpy 2d array describing the density of ships at time t
    :param police: list containing the position of police
    :param xx: numpy 2d array describing the x-mesh. Same shape as p_density
               and s_density
    :param yy: numpy 2d array describing the y-mesh. Same shape as p_density
               and s_density
    :param p_kernel: numpy 2d array describing the kernel in the equation for
                     pirates. Same shape as p_density
    :param cut_off_pirates: cut_off function for pirates.
    :param cut_off_ships: cut_off function for ships.
    :param cut_off_police: cut_off function for police.
    :param dx: float. The size of the x-mesh
    :param dy: float. The size of the y-mesh
    :param dt: float. The time step. It should satisfy a stability condition
    :param kappa: function. It takes a numpy array and returns an arry of the same shape. It is the normalized function in the equation for pirates
    :param a: array of floats. Coefficients a for the source term f in the equation for pirates.
    :param velocity: function describing the speed of the ship.
    :param nu_x: x-direction of the geometric component of nu
    :param nu_y: x-direction of the geometric component of nu
    :param controls: function giving the controls for police vessels
    :param time: float. initial time

    The output is a tuple (p_new, s_new, police_new) of three elements.
    :output p_new: numpy 2d array of the same shape as p_density
                   describing the density of pirates at time t + dt
    :output s_new: numpy 2d array of the same shape as s_density
                   describing the density of ships at time t + dt
    :output police_new: list of final position of police vessels
    """
    # some checks
    shape_p_density = numpy.shape(p_density)
    assert (shape_p_density == numpy.shape(s_density))
    assert (shape_p_density == numpy.shape(xx))
    assert (shape_p_density == numpy.shape(yy))
    assert (shape_p_density == numpy.shape(yy))

    # Calculus of common terms ?
    police_sum_x = sum(i[0] for i in police)
    police_sum_y = sum(i[1] for i in police)
    M = len(police)
    
    ################################
    # Evolution of pirate density
    ################################

    # 2d convolution on a fixed mesh
    # h * k [n, m] = dx * dy * convolve2d(h, k)
    p_convolution = dx * dy * scipy.signal.convolve2d(s_density, p_kernel, mode='same')
    # gradient of the convolution
    grad_py, grad_px = numpy.gradient(p_convolution, dy, dx)
    # norm of the gradient
    norm_grad_p_convolution = numpy.sqrt(grad_px**2 + grad_py**2)
    flux_x = kappa(norm_grad_p_convolution) * grad_px * p_density
    flux_y = kappa(norm_grad_p_convolution) * grad_py * p_density
    # divergence
    trash, div1 = numpy.gradient(flux_x, dy, dx)
    div2, trash = numpy.gradient(flux_y, dy, dx)
    div = - div1 - div2
    
    # term depending on the police
    f = numpy.zeros_like(xx)
    for i in xrange(len(police)):
        f += a[i] * cut_off_pirates(xx - police[i][0], yy - police[i][1])

    p_new = pde.one_step_parabolic(p_density, xx, yy, div, -f, dx, dy, dt)



    ################################
    # Evolution of ship density
    ################################

    # 2d convolution on a fixed mesh
    # h * k [n, m] = dx * dy * convolve2d(h, k)
    cal_I1_x = - dx * dy * scipy.signal.convolve2d(p_density, xx * cut_off_ships(xx, yy), mode='same')
    cal_I1_y = - dx * dy * scipy.signal.convolve2d(p_density, yy * cut_off_ships(xx, yy), mode='same')

    cal_I2_x = numpy.zeros_like(xx)
    cal_I2_y = numpy.zeros_like(xx)
    for i in xrange(len(police)):
        cal_I2_x += cut_off_ships(xx - police[i][0], yy - police[i][1]) * (police[i][0] - xx)
        cal_I2_y += cut_off_ships(xx - police[i][0], yy - police[i][1]) * (police[i][1] - yy)

    cal_I_x = cal_I1_x + cal_I2_x
    cal_I_y = cal_I1_y + cal_I2_y
    vel_x = cal_I_x + nu_x
    vel_y = cal_I_y + nu_y

    # (vel_x, vel_y) should be at most of norm 1!!!
    vel_pseudo_norm = numpy.maximum(numpy.sqrt(vel_x**2 + vel_y**2), 1.)
    vel_x = vel_x / vel_pseudo_norm
    vel_y = vel_y / vel_pseudo_norm
        
    s_new = pde.one_step_hyperbolic_godunov(s_density, velocity, vel_x, vel_y, dx, dy, dt)

    s_new = numpy.minimum(numpy.maximum(s_new, 0.), 1.)


    
    ################################
    # Evolution of police position
    ################################

    police_new = []
    for i in xrange(len(police)):
        temp = cut_off_police(police[i][0] - xx, police[i][1] - yy) * p_density * s_density
        F1_x = dx * dy * numpy.sum(temp * (xx - police[i][0]))
        F1_y = dx * dy * numpy.sum(temp * (yy - police[i][1]))

        F2_x = police_sum_x - M * police[i][0]
        F2_y = police_sum_y - M * police[i][1]

        F3_x = controls(time)[i][0]   #control_x
        F3_y = controls(time)[i][1]   #control_y

        police_new.append(ode.ode(F1_x + F2_x + F3_x, F1_y + F2_y + F3_y, police[i], dt))



    return (p_new, s_new, police_new)




#
# function for solving the system
# 
# def evolution(p_density, s_density, police, xx, yy,
#                        p_kernel, cut_off, dx, dy, dt):
def evolution(pirates):
    """
    This function performs the evolution for the whole system

    :param pirates: pirate class

    The output is a tuple (p_new, s_new, police_new) of three elements.
    :output p_new: numpy 2d array of the same shape as p_density
                   describing the density of pirates at time t + dt
    :output s_new: numpy 2d array of the same shape as s_density
                   describing the density of ships at time t + dt
    :output police_new: list of final position of police vessels
    """

    p_density = pirates.initial_density_pirates
    s_density = pirates.initial_density_ships
    police = pirates.police_initial_positions

    print_number = 1
    steps = len(pirates.time)
    cost = pirates.dt * numpy.sum(p_density * s_density)
    for i in xrange(1, steps):

        police_old = police
        
        # evolution from t to t + dt
        (p_density, s_density, police) = one_step_evolution(p_density, s_density, police, pirates.x_mesh, pirates.y_mesh,
                                                            pirates.kernel_mathcal_K, pirates.cut_off_C_pirates, pirates.cut_off_C_ships, pirates.cut_off_C_police, pirates.dx, pirates.dy,
                                                            pirates.dt, pirates.kappa, pirates.a, pirates.ships_speed, pirates.ships_direction_mesh[0], pirates.ships_direction_mesh[1], pirates.controls, pirates.time[i])

        police = pirates.project(police)
        
        # cost
        lenght2 = 0.
        cost += pirates.dt * numpy.sum(p_density * s_density)
        for ii in xrange(0, pirates.police_vessels):
            lenght2 += (police[ii][0] - police_old[ii][0])**2 + (police[ii][1] - police_old[ii][1])**2
        cost += numpy.sqrt(lenght2)
        
        # progresses
        sys.stdout.write('\r')
        # the exact output you're looking for:
        percentage = i * 100 /steps
        sys.stdout.write("[%-100s] %d%%" % ('='*percentage, percentage))
        sys.stdout.flush()

        if i%100 == 0:
            logging.info('Completed step ' + str(i) + ' over ' + str(steps) + ' steps at time ' + str(datetime.now()))
        
        # printing
        if pirates.printing[i]:
        #if True:
            name = 'saving_' + str(print_number).zfill(4)
            save.solution_Save(pirates.base_directory, name, pirates.time[i], p_density, s_density, police, cost)
            print_number += 1

        
    # saving the cost
    save.cost_Save(pirates.base_directory, 'cost', cost)

    logging.info('Final cost = ' + str(cost))
