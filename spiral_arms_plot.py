import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# Establish necessary variables and constants for calculations to come

R0 = 8.5 # sun distance from GC
V0 = 220# sun rotation
V = 244.35 # galaxy rotation
KPC_M = 3.08567758e+19 # kiloparsec to metre conversion factor
KPC_KM = 3.08567758e+16 # kpc to km conversion factor
R0_KM = R0*KPC_KM # R0 in km
R0_M = R0 * KPC_M # R0 in m

# Read data (csv file with LSR-corrected vels)

df = pd.read_csv('list_vobs_csv.csv', sep=',')

df.head(16)

# Using combination of sine rule and difference in radial vels for Sun and cloud. i.e. finding distance of cloud from GC in km
V0_ms = V0*1000
V_ms = V*1000

sin_l = np.sin(df['longitude']*(np.pi/180))
R_calculation_numerator = V*R0_KM
R_calculation_denom = V0 + (df['v_obs (km/s)']/sin_l)
df['R from GC (km)'] = R_calculation_numerator/R_calculation_denom # in km

df['R from GC (kpc)'] = df['R from GC (km)']/KPC_KM

df.head(16)


################### FINDING R1 FOR EACH CLOUD USING COSINE RULE ##############################

# Calculating R1, which is the the distance from the Sun and NOT from the GC. R is the distance from the GC to 
# celestial object
import math

cos_l = np.cos(df['longitude']*(np.pi/180))
first_part = R0_KM*cos_l
discriminant = (df['R from GC (km)'])**2-(R0_KM**2)*(sin_l)**2
sqrt = (discriminant)**0.5
R1 = first_part+sqrt
df['R1 from Sun (km)'] = R1

# Now for R1 in kpc
df['R1 from Sun (kpc)'] = R1 / KPC_KM

df.head(40)
#df.tail(40)


##################### SEPARATING REDSHIFTED AND BLUESHIFTED CLOUDS TO PLOT ON POLAR GRAPH (COLOUR-CODED) #######################################

# To separate neg velocities from the rest
index_neg_vel = []
neg_vels = []
for index, vel in enumerate(df['v_obs (km/s)']):    # the enumerate() function gives the index of the velocity that satisfies the condition directly below
    if vel < 0:
        index_neg_vel.append(index)
        neg_vels.append(vel)

radius_sun_km = []
relevant_longitudes = []
for ind in index_neg_vel:
    radius_neg_vel = df.iloc[ind, 2]
    longitudes_neg_vel = df.iloc[ind, 0]
    radius_sun_km.append(radius_neg_vel)
    relevant_longitudes.append(longitudes_neg_vel)

rad_sun_km_array = np.array(radius_sun_km)
rel_long_array = np.array(relevant_longitudes)

sin_l_neg = np.sin(rel_long_array*(np.pi/180))

cos_l_neg = np.cos(rel_long_array*(np.pi/180))
first_part_neg = R0_KM*cos_l_neg
discriminant = (rad_sun_km_array)**2-(R0_KM**2)*(sin_l_neg)**2
sqrt_neg = (discriminant)**0.5
R1_neg = first_part_neg+sqrt_neg
# Now for R1_neg in kpc
R_neg_kpc = R1_neg / KPC_KM

# Separate positive velocities
index_pos_vel = []
pos_vels = []
for index, vel in enumerate(df['v_obs (km/s)']):
    if vel > 0:
        index_pos_vel.append(index)
        pos_vels.append(vel)
        
radius_sun_km_pos = []
relevant_longitudes_pos = []
for ind in index_pos_vel:
    radius_pos_vel = df.iloc[ind, 2]
    longitudes_pos_vel = df.iloc[ind, 0]
    radius_sun_km_pos.append(radius_pos_vel)
    relevant_longitudes_pos.append(longitudes_pos_vel)
        
rad_sun_km_pos_array = np.array(radius_sun_km_pos)
rel_long_array_pos = np.array(relevant_longitudes_pos)

sin_l_pos = np.sin(rel_long_array_pos*(np.pi/180))

cos_l_pos = np.cos(rel_long_array_pos*(np.pi/180))
first_part_pos = R0_KM*cos_l_pos
discriminant = (rad_sun_km_pos_array)**2-(R0_KM**2)*(sin_l_pos)**2
sqrt_pos = (discriminant)**0.5
R1_pos = first_part_pos+sqrt_pos
# Now for R1_neg in kpc
R_pos_kpc = R1_pos / KPC_KM


# Plot polar curve with neg and pos velocities
cloud_thetas_pos = rel_long_array_pos*(np.pi/180)       
cloud_thetas_neg = rel_long_array*(np.pi/180)  

plot = plt.subplot(111, projection = 'polar')
plt.scatter(cloud_thetas_neg, R_neg_kpc, c="blue", label='Negative Velocities (Blue-shifted)')
plt.scatter(cloud_thetas_pos, R_pos_kpc, c="red", label='Positive Velocities (Red-shifted)')
plt.title("Galaxy plot showing H cloud positions", va = 'bottom')
plt.annotate('Sun', xy=(0, 0), xytext=(10, 10),
            arrowprops=dict(facecolor='black', shrink=0.05, width=1), 
            fontsize=18)
plt.annotate('GC', xy=(0, 8.5), xytext=(5, 5),
            arrowprops=dict(facecolor='black', shrink=0.05, width=1), 
            fontsize=18)
plt.legend(prop={'size': 14})
plt.figure(figsize=(20,20))
#plt.rcParams['figure.figsize']=(11,11)
plot.set_theta_zero_location("S")
#plt.rcParams['font.size']= 20
plt.rcParams['axes.titlesize'] = 20
plt.savefig('polar_distinction.png')
plt.show()


# ALTERNATIVELY, the code below just does the same as above, BUT does NOT distinguish between pos and neg vels.

# Arguments for plt.scatter with NO distinction between neg and pos velocities:
cloud_thetas = df['longitude']*np.pi/180
cloud_r = df['R1 from Sun (kpc)']  # Remember that you need to compute R1 first

plot = plt.subplot(111, projection = 'polar')
# Perhaps separate +ve and -ve vels into colour coded dots? Hmm...
plt.scatter(cloud_thetas, cloud_r, c="red")

plt.title("Galaxy plot showing H cloud positions", va = 'bottom')
plt.annotate('Sun', xy=(0, 0), xytext=(10, 10),
            arrowprops=dict(facecolor='black', shrink=0.05, width=1), 
            fontsize=18)
plt.annotate('GC', xy=(0, 8.5), xytext=(5, 5),
            arrowprops=dict(facecolor='black', shrink=0.05, width=1), 
            fontsize=18)
#plt.rcParams['figure.figsize']=(20,20)
plt.figure(figsize=(20,20))
plot.set_theta_zero_location("S")
#plt.rcParams['font.size']= 20
plt.rcParams['axes.titlesize'] = 20
plt.savefig('polar.png')
plt.show()
