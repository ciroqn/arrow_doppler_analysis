import pandas as pd
from bokeh.plotting import figure, output_notebook, show
#from bokeh.plotting import reset_output

from IPython.display import display, clear_output

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

from astropy import constants as const
from astropy import units as u

# Definition to take in a filename and return the header details in a var, and the rest of the file (the actual data) for it to be processed
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

# Function to convert frequency to radial velocity. The 'freq' is the placeholder for a numpy array or, in this case a dataframe. No need to loop through the 
# frequencies

def freq_to_vel(freq, f0=1420.4e6):
    ''' Takes a frequency value (or Pandas Dataframe column or Series) and returns
    a velocity value (or new Dataframe column of values). f0 is the rest
    frequency and defaults to 1420.4 MHz'''
    
    # We need a value for 'c' - thespeed of light. 
    # You can either define it explicitly here or alternatively, use the 
    # Astropy constants
    c = const.c  #m/s
    
    #
    # use km/s for convenience 
    v = -(c/1000)*(freq)/(freq+f0)
    #
    
    return v  #(km/s)  
