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

################################### CALCULATING RADIAL VELS AND STORING IN ARRAY ###############################
current_long = 0
index = 0
vels = []
while current_long <= 90:
    vel_max_current = df['v_obs_max (km/s)'][index]
    ang = current_long*(np.pi/180)
    val = int(vel(vel_max_current, ang))
    vels.append(val)
    current_long += 10
    index += 1

print(vels)

# Create velocity column for clouds
df['velocity (km/s)'] = vels

df

# Create velocity error column
v_error_array = [3, 3, 4, 3, 3, 3, 4, 4, 4, 5]

df['v_error (km/s)'] = v_error_array

df

# Calculated radius of clouds from GC
current_long_2 = 0
radii = []
while current_long_2 <= 90:
    rad_val = round(radius(current_long_2), 2)
    radii.append(rad_val)
    current_long_2 += 10

print(radii)
