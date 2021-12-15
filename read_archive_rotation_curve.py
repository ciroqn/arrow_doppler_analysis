# Reading archive data to read max. positive velocities and then displaying each graph at longitudes 0 -90 

import pandas as pd

df = pd.read_csv('archive_data.csv', sep=',', header=1, skiprows=[2],skipfooter=2, usecols=range(11), engine='python')

df
