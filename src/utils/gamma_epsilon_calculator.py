import numpy as np


def calc_epsilon(Q2,E,Eprime):
    y = (E-Eprime)/E
    q24E2 = Q2/(4*E*E)
    epsilon_top = 1-y-q24E2
    epsilon_bottom = 1-y+y**2/2+q24E2
    epsilon = epsilon_top/epsilon_bottom

    return epsilon

def calc_Gamma(Q2,xB,E,Eprime):
    alpha = 1/137 #Fund const
    mP = 0.938 #Mass proton
    epsilon = calc_epsilon(Q2,E,Eprime)

    prefix = alpha/(8*np.pi)
    term1 = Q2/(mP*mP*E*E)
    term2 = (1-xB)/(xB**3)
    term3 = 1/(1-epsilon)

    Gamma = prefix*term1*term2*term3
    Gamma = Gamma/(2*np.pi)

    return Gamma

def calculate_gamma_epsilon(Q2,xB,E,Eprime):

    Gamma = calc_Gamma(Q2,xB,E,Eprime)
    Epsilon = calc_epsilon(Q2,E,Eprime)

    return Gamma, Epsilon