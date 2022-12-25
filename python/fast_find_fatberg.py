import pandas as pd
import pyswmm
import random
import swmm.toolkit
import sys
from collections import subtract

# Clean file path inp
str_inp_clean = '/home/matthewdshen/GitHub/fatberg_detector/swmm_files/clean/Test_Network_clean.inp'

# Dirty path file inp
str_inp_dirty = '/home/matthewdshen/GitHub/fatberg_detector/swmm_files/dirty/Test_Network_dirty'+str(random.randint(1,22))+'.inp'

# List of nodes with sensors
lst_sensor_nodes = ['J1','J2','J3','J4','J5','J6','J7','J8','J9']


# Set up clean simulation
with pyswmm.Simulation(str_inp_clean) as sim_clean:
    # Run clean simulation
    for steps in sim_clean:
            pass

    # Get nodes from simulation
    lst_nodes_clean = pyswmm.nodes.Nodes(sim_clean)

    # # Pull links from simulation
    # lst_links_clean = pyswmm.Links(sim_clean)

    # Save cumulative inflow at each node
    dic_clean_flows = {}
    for node in lst_nodes_clean:
        dic_clean_flows[node.nodeid] = node.cumulative_inflow
        



with pyswmm.Simulation(str_inp_dirty) as sim_dirty:

    # Run dirty simulation
    for steps in sim_dirty:
            pass
    
    # Pull dirty nodes from simulation
    lst_nodes_dirty = pyswmm.nodes.Nodes(sim_dirty)

    # Pull dirty links from simulation
    lst_links_dirty = pyswmm.links.Links(sim_dirty)

    # Save cumulative inflow at each node
    dic_dirty_flows = {}
    for node in lst_nodes_dirty:
        dic_dirty_flows[node.nodeid] = node.cumulative_inflow

    # Get change in flow rate from clean and dirty network
    # print(subtract(dic_clean_flows) - subtract(dic_dirty_flows))
    # for link in lst_links_dirty:
    #     print(link.connections[0])
    #     print()











