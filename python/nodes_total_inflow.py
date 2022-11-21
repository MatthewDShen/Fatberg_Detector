import pyswmm
import pandas as pd
import matplotlib.pyplot as plt
from swmm.toolkit.shared_enum import NodeAttribute
from datetime import datetime
import matplotlib.pyplot as plt

clean_input_file = 'test/Test_Network_clear.inp'

dirty_input_file = 'test/Test_Network_dirty.inp'

def get_inflow(input_file,n_node):
  ''' function to get the total inflow from one node at all steps in the simulation and save it in a dataframe '''

  # create an Empty DataFrame object
  df_node = pd.DataFrame()
  simulation_time = []
  node_ids = []
  total_inflow = []
  
  with pyswmm.Simulation(inputfile=input_file) as sim:

    # Initialize nodes and links objects
    nodes = pyswmm.Nodes(sim)

    # Specify the link or nodes that we are interested in monitoring
    node = nodes[n_node]
  
    # itterate through each step in simulation
    for step in sim:

        # Log the simulation time
        simulation_time.append(sim.current_time)

        # Log node id and total_inflow
        #node_ids.append(node.nodeid)
        total_inflow.append(node.total_inflow)

    # create dataframe with step data for that node and update column name
    df_node = pd.DataFrame(total_inflow, simulation_time)
    df_node.columns =[n_node]

    return df_node

def combine_allnodes(input_file, node_num):
  ''' function to combine inflow and time step data from all nodes from input file into one dataframe 
      Inputs are simulation file path and list of node numbers'''

  # initialize dataframe
  df_allflow = pd.DataFrame()

  # itterate through each node
  for s in node_num:

    # run get_inflow function on current node and add it to that column in dataframe
    df_allflow[s]=(get_inflow(input_file, s))

  return df_allflow

# list of node names
node_list = ['J1','J2','J3','J4','J5','J6','J7','J8','J9','J10','J11','J12']


def plot_flows(input_file,node_list):

  
  # create dataframe with simulation data for all nodes
  allflow = combine_allnodes(input_file, node_list)

  plt.figure(figsize=(20, 5), dpi=100)

  for n in node_list:
    plt.plot(allflow[n], linewidth=2.0, label = n)

  plt.title("flows at each node")
  plt.ylabel("Flow (CFS)")
  plt.xlabel("Simulation Time")
  plt.legend(loc="upper right")
  plt.savefig("/home/matthewdshen/GitHub/Fatberg_Detector/images/imagd.png")

df_clean = combine_allnodes(clean_input_file,node_list)

df_dirty = combine_allnodes(dirty_input_file,node_list)

df_delta = df_clean - df_dirty

df_delta_avg = df_delta.mean()

print(df_delta_avg)