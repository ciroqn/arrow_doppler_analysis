import pandas as pd

df = pd.read_csv('vobs_archive_21.csv', sep=',',skipfooter=11, usecols=range(3), engine='python')

df


################################ CREATE FUNCTIONS/DEFS FOR CALCULATIONS ###############################
import numpy as np
from astropy import constants as c
from astropy import units as u

def vel(v_max, angle, v_0 = 220):
    velocity = v_max + v_0*np.sin(angle)
    return velocity

def radius(gamma, r_sun_kpc = 8.5):
    gamma_rads = gamma*(np.pi/180)
    radius = r_sun_kpc*np.sin(gamma_rads)
    return radius
