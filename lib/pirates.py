#!/usr/bin/env python

### pirates.py
### class containing all the relevant data

import numpy as np
import logging

class pirates(object):

    def __init__(self, x_1, x_2, y_1, y_2, n_x, n_y, M, tMax, d_o,
                 InitialDatum_rho, InitialDatum_A, speed_ships, nu, DirName,
                 mathcal_K, cut_off_C_pirates, kappa, a, cut_off_C_ships, cut_off_C_police, pictures = 90):
        """
        Initializatium function for the class.
        :param x_1: float. Lower bound for x-coordinate of the domain
        :param x_2: float. Upper bound for x-coordinate of the domain
        :param y_1: float. Lower bound for y-coordinate of the domain
        :param y_2: float. Upper bound for y-coordinate of the domain
        :param n_x: int. Number of points for the discretization of the x-component
                    of the domain.
        :param n_y: int. Number of points for the discretization of the y-component
                    of the domain.
        :param M: int. Number of police vessels.
        :param tMax: float. Time of the simulation
        :param d_o: tuple of lenght M. Each element is a tuple of 2 floats,
                    describing the initial position of the police vessels
        :param InitialDatum_rho: function. It gives the initial density of the 
                                 pirates.
        :param InitialDatum_A: function. It gives the initial density of the 
                               commercial ships.

        :param speed_ships: function. It gives the speed of ship when density is A
        :param nu: tuple of two functions. They give the geometrical direction of
                   the ships.
        :param DirName: string. It gives the name of the working directory, i.e. of
                        the directory containing the simulation

        :param mathcal_K: function describing the kernel in the equation for pirates
        :param cut_off_C_pirates: function describing the kernel in the equation for pirates
        :param kappa: function. It gives the normalization for the
                      direction in the equation for pirates
        :param cut_off_C_ships: function describing the kernel in the equation for ships
        :param cut_off_C_police: function describing the kernel in the equation for police
        :param a: array of floats. Coefficients a in the source term f for the eq
        :param pictures: int. Approximate number of pictures.
        """

        # 2d domains
        self.x_1 = x_1
        self.x_2 = x_2
        self.y_1 = y_1
        self.y_2 = y_2
        self.domain = ((x_1, x_2), (y_1, y_2))
        self.n_x = n_x
        self.n_y = n_y
        self.check_domain()

        self.create_mesh()
        self.create_initial_datum(InitialDatum_rho, InitialDatum_A)

        
        # police
        self.police_vessels = M
        self.police_initial_positions = d_o
        self.check_positions()


        # ships' velocity
        self.ships_speed = speed_ships
        self.ships_direction = nu
        self.ships_direction_mesh = nu(self.x, self.y)
        
        # time 
        self.time_of_simulation = tMax
        self.create_time_mesh()

        # printing mesh
        self.pictures = pictures
        self.create_print_mesh()

        # base directory
        self.base_directory = DirName

        # kernels and cut-off
        self.mathcal_K = mathcal_K
        # self.cut_off_C = cut_off_C
        self.cut_off_C_pirates = cut_off_C_pirates
        self.cut_off_C_ships = cut_off_C_ships
        self.cut_off_C_police = cut_off_C_police
        self.create_kernels()

        # normalization function kappa
        self.kappa = kappa

        # coefficient a for the source term f in the equation for pirates
        self.a = a
        
    #
    # Function for creating the space mesh
    #
    def create_mesh(self):
        """
        This function creates the grid for the domain Omega.
        
        self.x = numpy vector starting from self.x_1, ending to self.x_2, with
                 self.n_x points, i.e. its length = self.n_x
        self.dx = the horizontal step

        self.y = numpy vector starting from self.y_1, ending to self.y_2, with
                 self.n_y points, i.e. its length = self.n_y
        self.dy = the vertical step

        self.x_mesh and self.y_mesh are the corresponding meshgrids. Their shape
                                    is (self.n_y, self.n_x)
 
        """
        (self.x, self.dx) = np.linspace(self.x_1, self.x_2, self.n_x, retstep=True)
        (self.y, self.dy) = np.linspace(self.y_1, self.y_2, self.n_y, retstep=True)
        self.x_mesh, self.y_mesh = np.meshgrid(self.x, self.y)


    #
    # Function for creating the time mesh
    #
    def create_time_mesh(self):
        """
        This function creates the time mesh.
        
        self.time = numpy vector starting from 0, ending to self.time_of_simulation
        self.dt = the time step

        """
        dxy = min(self.dx, self.dy)
        dt = 0.25* min(dxy**2, dxy/self.ships_speed(0))
        N = 2 + int(self.time_of_simulation / dt)
        (self.time, self.dt) = np.linspace(0., self.time_of_simulation, N, retstep = True)
        assert (self.dt <= dt)


    #
    # Function for creating the printing mesh
    #
    def create_print_mesh(self):
        """
        This function creates the print mesh.
        
        self.time = numpy vector starting from 0, ending to self.time_of_simulation
        self.dt = the time step

        """
        K = min(int(float(len(self.time))/self.pictures), 90)
        self.printing = np.zeros_like(self.time, dtype= bool)
        self.printing[::K] = True
        self.printing[-1] = True

        
    #
    # Function for creating the kernels
    #
    def create_kernels(self):
        """
        This function creates 2d vectors for the kernels

        self.kernel_x = numpy vector centered at x=0 with same size as self.x
                        and mesh size self.dx
        self.kernel_y = numpy vector centered at x=0 with same size as self.y
                        and mesh size self.dy
        self.kernel_mathcal_K = numpy 2d vector generated by the function
                                self.mathcal_K

        """

        self.kernel_x = self.x - (self.x_1 + self.x_2)/2.
        self.kernel_y = self.y - (self.y_1 + self.y_2)/2.
        self.kernel_mathcal_K = self.mathcal_K(self.kernel_x, self.kernel_y)


        
    #
    # Function for creating 2d vectors for intial data
    #
    def create_initial_datum(self, InitialDatum_rho, InitialDatum_A):
        """
        This function creates two 2d-arrays for the initial data for ship and
        pirates.
        :param InitialDatum_rho: function. It gives the initial datum for pirates.
        :param InitialDatum_A: function. It gives the initial datum for ships.

        It creates self.initial_density_pirates and self.initial_density_ships.
        They are two 2d-numpy array of shapes (n_y, n_x)
        """
        self.initial_density_pirates = InitialDatum_rho(self.x_mesh, self.y_mesh)
        self.initial_density_ships = InitialDatum_A(self.x_mesh, self.y_mesh)
    

    #
    # Function for checking the domain is feasible.
    #
    def check_domain(self):
        if self.x_1 >= self.x_2:
            print 'Error: x_1 should be less than x_2'
            logging.info('Error: x_1 should be less than x_2')
            exit()

        if self.y_1 >= self.y_2:
            print 'Error: y_1 should be less than y_2'
            logging.info('Error: y_1 should be less than y_2')
            exit()

        if not isinstance(self.n_x, int) or not isinstance(self.n_y, int):
            print 'Error: both n_x and n_y should be integers'
            logging.info('Error: both n_x and n_y should be integers')
            exit()

        if self.n_x == 0 or self.n_y == 0:
            print 'Error: both n_x and n_y should be strictly positive'
            logging.info('Error: both n_x and n_y should be strictly positive')
            exit()

    #
    # Function for checking the initial position of the police vessels.
    def check_positions(self):
        if not isinstance(self.police_vessels, int):
            print 'Error: the number M of vessels should be integer'
            logging.info('Error: the number M of vessels should be integer')
            exit()
            
            
        if len(self.police_initial_positions) != self.police_vessels:
            print 'Error: the number of police vessels does not coincide with their initial position'
            logging.info('Error: the number of police vessels does not coincide with their initial position')
            exit()

        for i in xrange(len(self.police_initial_positions)):
            if self.police_initial_positions[i][0] < self.x_1 or self.police_initial_positions[i][0] > self.x_2:
                print 'Error: the x position of the ' + str(i+1) + '-th vessel is not correct'
                logging.info('Error: the x position of the ' + str(i+1) + '-th vessel is not correct')
                exit()

            if self.police_initial_positions[i][1] < self.y_1 or self.police_initial_positions[i][1] > self.y_2:
                print 'Error: the y position of the ' + str(i+1) + '-th vessel is not correct'
                logging.info('Error: the y position of the ' + str(i+1) + '-th vessel is not correct')
                exit()
