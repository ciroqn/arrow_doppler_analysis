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

######################################### CODE TO DISPLAY SUERPOSED RAW DATA (I.E. INTENSITY VS FREQ. SHIFT) #############################################

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



######################################### CODE FOR BASELINE REMOVAL ################################################
# Read in the background spectra, average and subtract from the spectrum
# Here we use  hard-wired file names but you could use a file list, or manually enter them
number_header_lines = 12

# Dr Cayless' scans for our team:
raw_data_array = ['long_030.csv', 'long_040.csv', 'long_050.csv', 'long_060.csv', 'long_070.csv', 'long_080.csv', 'long_090.csv']
park_bg = ['scan_NGP01.csv', 'scan_NGP02.csv', 'scan_NGP03.csv', 'scan_NGP04.csv', 'scan_NGP05.csv', 'scan_NGP06.csv', 'scan_NGP07.csv', 'scan_NGP08.csv', 'scan_NGP09.csv', 'scan_NGP10.csv']

#bgdata_array = ['nepscan1_csv.csv', 'nepscan2_csv.csv', 'nepscan3_csv.csv', 'nepscan4_csv.csv', 'nepscan5_csv.csv', 'nepscan6_csv.csv', 'nepscan7_csv.csv', 'nepscan8_csv.csv']

# These are bg scans from the Park position that can be used instead of the above array:
#park_bg = ['bg1.csv', 'bg2.csv', 'bg3.csv', 'bg4.csv', 'bg5.csv']

# We again use skipinitialspace = True to ignore the space in the 'intensity' column name

#read_csv_list = []
#for bg_data in bgdata_array:
#    read_csv_list.append(pd.read_csv(bg_data, header = number_header_lines, skipinitialspace = True))
   
# For park_bg only
read_csv_list_2 = []
for bg_data in park_bg:
    read_csv_list_2.append(pd.read_csv(bg_data, header = number_header_lines, skipinitialspace = True))
    
# This is the long way of averaging the bg scans. Instead, I used a for loop...
#bg1 = pd.read_csv('nepscan1_csv.csv', header = number_header_lines, skipinitialspace = True)
#bg2 = pd.read_csv('nepscan2_csv.csv', header = number_header_lines, skipinitialspace = True)
#bg3 = pd.read_csv('nepscan3_csv.csv', header = number_header_lines, skipinitialspace = True)
#bg4 = pd.read_csv('nepscan4_csv.csv', header = number_header_lines, skipinitialspace = True)
#bg5 = pd.read_csv('nepscan5_csv.csv', header = number_header_lines, skipinitialspace = True)
#bg6 = pd.read_csv('nepscan6_csv.csv', header = number_header_lines, skipinitialspace = True)
#bg7 = pd.read_csv('nepscan7_csv.csv', header = number_header_lines, skipinitialspace = True)
#bg8 = pd.read_csv('nepscan8_csv.csv', header = number_header_lines, skipinitialspace = True)

# For bgdata_array only
#bg_sum = 0 
#for data in read_csv_list:
#    bg_sum += data['intensity']

# For park_bg only: adding the intensities for each bg scan
bg_sum_2 = 0
for data in read_csv_list_2:
    bg_sum_2 += data['intensity']

bg_av = bg_sum_2/10

# Compute average intensity values
# bg_av = (bg1['intensity']+bg2['intensity']+bg3['intensity']+bg4['intensity']+bg5['intensity']+bg6['intensity']+bg7['intensity']+bg8['intensity'])/8
print(type(bg_av))
# Subract from spectrum intensity
spectrum_df['intensity'] = spectrum_df['intensity']-bg_av.values

spectrum_df.head(20)

spectrum_df.tail(10)

s01 = figure(plot_width=850, plot_height=500, title='Scans at: l = 40, 50, 60, 70, 80, 90',
            x_axis_label='Frequency/Hz', 
            y_axis_label='Intensity')
s01.line(spectrum_df['frequency'],spectrum_df['intensity'], color='red', legend='l = 30')
s01.legend.location = "top_left"
show(s01)

# Section for inputted file only. See below for velocity calculation for ALL files in the loop
# Convert frequency to radial velocity values using this function
spectrum_v = freq_to_vel(spectrum_df['frequency'])

# Add a new 'velocity' column with these values
spectrum_df['velocity'] = spectrum_v

spectrum_df['velocity']

######################################### CODE FOR PRINTING INDIV. GRAPH FOR EACH LONG. + GRIDPLOT OF ALL LONG. + GRAPH FOR INPUTTED FILE ########################

# This block of code can be split up into three sections: 1) prints out individual graph for each longitude; 
# 2) prints a gridplot of all the longitudes 3) prints the graph for the inputted file.

from bokeh.layouts import gridplot
from bokeh.models import Range1d

# Dr Cayless' scans for our team
scandata_array = ['long_030.csv', 'long_040.csv', 'long_050.csv', 'long_060.csv', 'long_070.csv', 'long_080.csv', 'long_090.csv']
bg_data_0 = ['scan_NGP02.csv', 'scan_NGP03.csv', 'scan_NGP04.csv', 'scan_NGP05.csv', 'scan_NGP06.csv', 'scan_NGP07.csv', 'scan_NGP08.csv', 'scan_NGP09.csv', 'scan_NGP10.csv']

# Display plots for all files using loop (these files are the 'old' files from our group's session)
# scandata_array = ['target40fs_firstcsv.csv', 'target50fs_secondcsv.csv', 'target60fs_secondcsv.csv', 'target70fs_secondcsv.csv', 'target80fs_firstcsv.csv', 'target90fs_firstcsv.csv']

# Read the files in 'scandata_array' using for loop
read_csv_list_two = []
for long_data in scandata_array:
    read_csv_list_two.append(pd.read_csv(long_data, header = number_header_lines, skipinitialspace = True))
 
# For these files, we subtract the averaged intensities of the bg scans and set the velocity column in the modified
# csv files by inputting the frequency column in the 'freq_to_vel' column. This is done for each longitude:
current_long = 30
for longitude in read_csv_list_two:
    longitude['intensity'] = longitude['intensity']-bg_av.values
    spectrum_vel = freq_to_vel(longitude['frequency'])
    longitude['velocity'] = spectrum_vel
    xvals = longitude['velocity']
    
    plot = figure(plot_width=800, plot_height=500, title='Scan at Longitude ' + str(current_long),
                 x_axis_label='Velocity / kms\u207b\u00b9',
                 y_axis_label='Intensity')
    plot.line(xvals,longitude['intensity'], color='red')
    plot.add_tools(HoverTool(mode='vline'))
    show(plot)
    current_long += 10
    
    
# print(read_csv_list_two)
    
# The above code prints out a large graph for each. But below, smaller graphs are printed for each and inserted into
# are plot grid.
s0 = figure(plot_width=250, plot_height=175, title='S0: l = 30',
            x_axis_label='Velocity / kms\u207b\u00b9', 
            y_axis_label='Intensity')
s0.line(read_csv_list_two[0]['velocity'],read_csv_list_two[0]['intensity'], color='orange')
s1 = figure(plot_width=250, plot_height=175, title='S1: l = 40',
            x_axis_label='Velocity / kms\u207b\u00b9', 
            y_axis_label='Intensity')
s1.line(read_csv_list_two[1]['velocity'],read_csv_list_two[1]['intensity'], color='red')
s2 = figure(plot_width=250, plot_height=175, title='S2: l = 50',
            x_axis_label= 'Velocity / kms\u207b\u00b9', 
            y_axis_label='Intensity')
s2.line(read_csv_list_two[2]['velocity'],read_csv_list_two[2]['intensity'], color='green')
s3 = figure(plot_width=250, plot_height=175, title='S3: l = 60',
            x_axis_label='Velocity / kms\u207b\u00b9', 
            y_axis_label='Intensity')
s3.line(read_csv_list_two[3]['velocity'],read_csv_list_two[3]['intensity'], color='blue')
s4 = figure(plot_width=250, plot_height=175, title='S4: l = 70',
            x_axis_label='Velocity / kms\u207b\u00b9', 
            y_axis_label='Intensity')
s4.line(read_csv_list_two[4]['velocity'],read_csv_list_two[4]['intensity'], color='black')
s5 = figure(plot_width=250, plot_height=175, title='S5: l = 80',
            x_axis_label='Velocity / kms\u207b\u00b9', 
            y_axis_label='Intensity')
s5.line(read_csv_list_two[5]['velocity'],read_csv_list_two[5]['intensity'], color='gray')
s6 = figure(plot_width=250, plot_height=175, title='S6: l = 90',
            x_axis_label='Velocity / kms\u207b\u00b9', 
            y_axis_label='Intensity')
s6.line(read_csv_list_two[6]['velocity'],read_csv_list_two[6]['intensity'], color='purple')

grid = gridplot([[s0,s1,s2],[s3,s4,s5], [s6]])
show(grid)

# Display plot for inputted file only
xvals = spectrum_df['velocity']

s1 = figure(plot_width=800, plot_height=400, title='l = 40',
            x_axis_label='Velocity / kms\u207b\u00b9', 
            y_axis_label='Intensity')
s1.line(xvals,spectrum_df['intensity'], color='red')
s1.add_tools(HoverTool(mode='vline'))

show(s1)


########################## IPNUTTED FILE ONLY: CREATE MODIFIED FILE WITH BASELINE SUBTRACTIONS + HEADER ######################################

# This section saves the header lines in a particular file (i.e. file inputted by user at the beginning) to a 
# modified file (which we prompt for below), and THEN appends the rest of the data (i.e. frequency, modified intensity, 
# and velocity) to the header. Note the 'mode=a' in the 'to_csv'. This ensures that the data is appended, otherwise, 
# it will just overwrite the header data, which we don't want.

# Prompt for a new file name
new_file_name = input("Provide a name for a new file to store the data in format 'filename.csv': ")

# First write the header lines that we read in earlier to the file.
# Use the .writelines() function from FileIO section 2.1
with open(new_file_name, mode='w') as newf:
    newf.writelines(header_lines)
    
# Now APPEND the modified csv data using the pandas .to_csv() method 
# UsingPandas section 3 should help
spectrum_df.to_csv(new_file_name, index=False, mode='a')
