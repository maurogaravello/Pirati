#!/usr/bin/env python

### pirates.py
### class containing all the relevant data

import numpy as np
import logging

class pirates(object):

    def __init__(self, x_1, x_2, y_1, y_2, n_x, n_y, M, tMax, d_o,
                 InitialDatum_rho, InitialDatum_A, speed_ships, nu, DirName):
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

        # time 
        self.time_of_simulation = tMax
        self.dt = np.array([0.])

        # ships' velocity
        self.ships_speed = speed_ships
        self.ships_direction = nu

        # base directory
        self.base_directory = DirName

    #
    # Function for creating the meshes
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
