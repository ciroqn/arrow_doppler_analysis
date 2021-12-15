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

# Add rad column to df
df['radius (kpc)'] = radii

df

# import relevant packages

from bokeh.layouts import gridplot
from bokeh.models import Range1d
from bokeh.plotting import figure, output_notebook, show
from bokeh.models.tools import HoverTool

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

%matplotlib inline
output_notebook()


##################################### PLOTTING ROTATION CURVE (I.E. ORBITAL VELOCITY VS RADIUS (IN KPC)) ########################################
# Plot the 10 data points for ROTATION CURVE

x = df['radius (kpc)']
y = df['velocity (km/s)']
y_err = df['v_error (km/s)']

plt.plot(x,y, '.',label='Data Points')
plt.errorbar(x,y,yerr=y_err, xerr=None, fmt='none')
plt.ylim(0,300)
plt.ylabel('Velocity / kms\u207b\u00b9')
plt.xlabel('Radius / kpc')
plt.grid(False)
plt.legend()

# no need for 'plt.show()' until after the code for curve fit


# Alternative to the scipy line fit.
#x = np.linspace(0,8.5,100)
#y = 250-197*np.exp(-1.00*x)
#plt.plot(x, y, '-r', label='Eq')

# Fitting line to graph
from scipy.optimize import curve_fit

# Here'e a simple mathematical curve that might fit
def gal_curve(r,C0,C1,C2):
    return C0-C1*np.exp(-C2*r)

R = df['radius (kpc)'].values
V = df['velocity (km/s)'].values
R2 = np.linspace(0,8.5, 50)

# Use some trial values for initial parameters for the constants
p0 = [250,200,0.15]

# and fit the curve 
c,pcov = curve_fit(gal_curve,R,V,p0)  # curvue_fit(function, x, y, parameters)

print('Optimised parameters are:', *c)

# Plot it 
plt.plot(R2,gal_curve(R2,*c), label='Galactic Rotation Curve')   # plt.plot(x,y)
plt.legend()
plt.show()
