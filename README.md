# Analysis of Intensity vs Frequency (ARROW Project)

This is the analysis stage for the results from ARROW radio astronomy on 4/11/21. The tables show targets from longitudes 40 to 90. The initial plan was to scan 50 - 100 longitudes, but the radio frequency interference (RFI) was particularly bad at longitude 100.

The frequencies recorded for these longitudes are *centred* around the rest frequency of hydrogen.

Contents:

- Reading raw data from *csv* files and plotting graphs and saving ameneded *csv* files with background-subtracted intensities and associated velocities: [here](https://github.com/ciroqn/arrow_doppler_analysis/blob/main/graphs_int_vel.py)
- Read archival data and plot each (intensity vs frequency): [here](https://github.com/ciroqn/arrow_doppler_analysis/blob/main/read_archive_rotation_curve.py)
- Reading maximum radial velocities from graphs and plotting against radius from GC: [here](https://github.com/ciroqn/arrow_doppler_analysis/blob/main/read_archive_rotation_curve.py)
- Plot spiral arms (Cygnus & Perseus) using distance of hydrogen clouds from Solar System (as opposed to GC) and their associated orbital velocities: [here](https://github.com/ciroqn/arrow_doppler_analysis/blob/main/spiral_arms_plot.py)
