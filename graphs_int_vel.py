import pandas as pd
from bokeh.plotting import figure, output_notebook, show
#from bokeh.plotting import reset_output

from IPython.display import display, clear_output

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

from astropy import constants as const
from astropy import units as u

from bokeh.models.tools import HoverTool

def read_ARROW_data(filename):
    """Reads in and partially processes an  ARROW spectrum
    
    The spectrum file contains a number of header lines indicated by `#' or blanks. 
    This function splits these from the main data and returns both 
            
    Parameters
    ----------
    filename : str
        Name of the spectrum file
    
    Returns
    -------
    dat : class: pandas.DataFrame
        Spectrum data
    Header lines : list of str
        List of header lines
    """
    
    # Read lines till first line not starting with #, or whitespace.
    # Store these as a list
    header_list = []
    number_header_lines = 0
    dat = None
    with open(filename) as f:
        line = f.readline()
        while line[0] == '#' or line[0] == ',' or line[0].isspace():
            header_list.append(line)
            number_header_lines += 1
            line = f.readline()
        dat = pd.read_csv(filename, header = number_header_lines, skipinitialspace = True)

    return dat, header_list
  
# Function to convert frequency to radial velocity.

def freq_to_vel(freq, f0=1420.4e6):
    ''' Takes a frequency value (or Pandas Dataframe column or Series) and returns
    a velocity value (or new Dataframe column of values). f0 is the rest
    frequency and defaults to 1420.4 MHz'''
    
    # We need a value for 'c'
    # Astropy constant
    c = const.c  #m/s
    
    #
    # use km/s for convenience 
    v = -(c/1000)*(freq)/(freq+f0)
    #
    
    return v  #(km/s)    

############################### OBTAIN DATA #########################################

# Prompt the user for a file name (we'll call it file_name)
# You should know how to do this by now
file_name = input("Please input a filename in the format 'filename.csv'")

# spectrum_df is equal to the 'dat' returned variable, and header_lines to the returned 'header_list'
spectrum_df, header_lines = read_ARROW_data(file_name)

# Just to check, this should show a list of all the header lines in the 'file_name' given by the user input
print(header_lines)

# Display the first few lines - does it look reasonable?
spectrum_df.head(12)



# For Jupyter interface
output_notebook()

raw_data_array = ['long_030.csv', 'long_040.csv', 'long_050.csv', 'long_060.csv', 'long_070.csv', 'long_080.csv', 'long_090.csv']
bg_data_0 = ['scan_NGP02.csv', 'scan_NGP03.csv', 'scan_NGP04.csv', 'scan_NGP05.csv', 'scan_NGP06.csv', 'scan_NGP07.csv', 'scan_NGP08.csv', 'scan_NGP09.csv', 'scan_NGP10.csv']

# Replace the above with team's scans 

# A loop to read each file in the raw csv files so data can be readily used to process graphs
read_csv_list_0 = []
for raw_data in raw_data_array:
    read_csv_list_0.append(pd.read_csv(raw_data, header=12, skipinitialspace = True))
    
print(read_csv_list_0[0])
    
# This for loop does the same as above, but it is for the data in the background scans
bg_data_read = []
for raw_bg_data in bg_data_0:
    bg_data_read.append(pd.read_csv(raw_bg_data, header=12, skipinitialspace = True))

# Individual graph for a particular spectrum
s0 = figure(plot_width=850, plot_height=500, title='Scans at: l = 30',
            x_axis_label='Frequency/Hz', 
            y_axis_label='Intensity')
s0.line(read_csv_list_0[0]['frequency'],read_csv_list_0[0]['intensity'], color='red', legend='l = 30')
s0.legend.location = "top_left"
show(s0)

# Now that each file can be 'read', a graph is plotted showing ALL of the graphs to see commonalities/differences
s1 = figure(plot_width=850, plot_height=500, title='Scans at: l = 40, 50, 60, 70, 80, 90',
            x_axis_label='Frequency/Hz', 
            y_axis_label='Intensity')
s1.line(read_csv_list_0[0]['frequency'],read_csv_list_0[0]['intensity'], color='red', legend='l = 30')
s1.line(read_csv_list_0[1]['frequency'],read_csv_list_0[1]['intensity'], color='green',legend='l = 40')
s1.line(read_csv_list_0[2]['frequency'],read_csv_list_0[2]['intensity'], color='blue', legend='l = 50')
s1.line(read_csv_list_0[3]['frequency'],read_csv_list_0[3]['intensity'], color='yellow', legend='l = 60')
s1.line(read_csv_list_0[4]['frequency'],read_csv_list_0[4]['intensity'], color='black', legend='l = 70')
s1.line(read_csv_list_0[5]['frequency'],read_csv_list_0[5]['intensity'], color='gray', legend='l = 80')
s1.line(read_csv_list_0[6]['frequency'],read_csv_list_0[6]['intensity'], color='orange', legend='l = 90')
s1.line(bg_data_read[0]['frequency'],bg_data_read[0]['intensity'], color='magenta', legend='Baseline')
s1.line(bg_data_read[1]['frequency'],bg_data_read[1]['intensity'], color='magenta')
s1.line(bg_data_read[2]['frequency'],bg_data_read[2]['intensity'], color='magenta')
s1.line(bg_data_read[3]['frequency'],bg_data_read[3]['intensity'], color='magenta')
s1.line(bg_data_read[4]['frequency'],bg_data_read[4]['intensity'], color='magenta')
s1.legend.location = "top_left"
show(s1)
