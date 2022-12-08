import pandas as pd
import pyswmm
import random
import swmm.toolkit
import sys

# Clean file path inp
str_inp_clean = '/home/matthewdshen/GitHub/fatberg_detector/swmm_files/clean/Test_Network_clean.inp'

# Dirty path file inp
str_inp_dirty = '/home/matthewdshen/GitHub/fatberg_detector/swmm_files/dirty/Test_Network_dirty1.inp'

# Set up clean simulation
sim_clean = pyswmm.Simulation(str_inp_clean)
# Run clean simulation
for steps in sim_clean:
        pass

# Set up dirty simulation
sim_dirty = pyswmm.Simulation(str_inp_dirty)
# Run dirty simulation
for steps in sim_dirty:
        pass

# Get nodes from simulation
lst_nodes = pyswmm.nodes.Nodes(sim_clean)

# Pull links from simulation
lst_links = pyswmm.Links(sim_clean)
    
# List of nodes with sensors
lst_sensor_nodes = ['J1','J9']

# Loop through each 

print(lst_nodes['J1'].cumulative_inflow)


















