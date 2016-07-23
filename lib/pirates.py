#!/usr/bin/env python

### pirates.py
### class containing all the relevant data

class pirates(object):

    def __init__(self, x_1, x_2, y_1, y_2, n_x, n_y, M, tMax):

        self.x_1 = x_1
        self.x_2 = x_2
        self.y_1 = y_1
        self.y_2 = y_2
        self.domain = ((x_1, x_2), (y_1, y_2)) 

        self.n_x = n_x
        self.n_y = n_y
        self.police_vessels = M

        self.time_of_simulation = tMax
        
