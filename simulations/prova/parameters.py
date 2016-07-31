# parameters for pirates - 

######################################################
## DOMAIN \Omega = (x_1, x_2) x (y_1, y_2)
######################################################

x_1 = 0. # minimum value for x
x_2 = 10. # maximum value for x

y_1 = 0. # minimum value for y
y_2 = 20. # maximum value for y

######################################################
## MESH SIZES
## n_x = number of cells in the x-direction
## n_y = number of cells in the y-direction
######################################################

n_x = 200 # integer
n_y = 100 # integer

######################################################
## Number M of police vessels
######################################################

M = 3 # integer number

######################################################
## TIME
######################################################

tMax = 10. # time of simulation

######################################################
## INITIAL DATA
######################################################

# Initial Datum for rho (density of piracy)
def InitialDatum_rho (x, y):
    return x*y

# Initial Datum for A (density of ships)
def InitialDatum_A (x, y):
    return numpy.zeros_like(x)

# Initial Datum for police vessels
# d_o -> list of size M
# each element is a tuple with 2 elements
d_o = [(5., 11.), (2., 10.), (7., 10.)] 

######################################################
## EQUATION FOR A
######################################################

# speed of ships
def speed_ships(A):
    A_max = 1. # maximum density
    v_max = 1. # maximum speed
    return v_max - A/A_max

# geometric vector speed
def nu(x,y):
    return (1., 0.)










