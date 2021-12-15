import pandas as pd

df = pd.read_csv('vobs_archive_21.csv', sep=',',skipfooter=11, usecols=range(3), engine='python')

df
