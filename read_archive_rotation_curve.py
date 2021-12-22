# Reading archive data to read max. positive velocities and then displaying each graph at longitudes 0 -90 

import pandas as pd

df = pd.read_csv('archive_data.csv', sep=',', header=1, skiprows=[2],skipfooter=2, usecols=range(11), engine='python')

df

# imports
from bokeh.layouts import gridplot
from bokeh.models import Range1d
from bokeh.plotting import figure, output_notebook, show
from bokeh.models.tools import HoverTool

output_notebook()  # Jupyter-specific, I believe

# Print each int vs vel graph for each longitude
long = 0
while long <= 90:
    current_longitude = 'l = ' + str(long) + ' degrees'
    x_vals = df['km per sec']
    y_vals = df[current_longitude]
    plot = figure(plot_width=800, plot_height=500, title='Scan at Longitude ' + str(long),
                 x_axis_label='Velocity / kms\u207b\u00b9',
                 y_axis_label='Intensity')
    plot.line(x_vals,y_vals, color='green')
    plot.add_tools(HoverTool(mode='vline'))
    show(plot)
    long += 10
