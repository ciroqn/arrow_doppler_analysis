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
