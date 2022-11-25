import pyswmm
import pandas as pd
import matplotlib.pyplot as plt
from swmm.toolkit.shared_enum import NodeAttribute

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

def combine_allnodes(input_file, node_list):
  ''' function to combine inflow and time step data from all nodes from input file into one dataframe 
      Inputs are simulation file path and list of node numbers'''

  # initialize dataframe
  df_allflow = pd.DataFrame()

  # itterate through each node
  for s in node_list:

    # run get_inflow function on current node and add it to that column in dataframe
    df_allflow[s]=(get_inflow(input_file, s))

  return df_allflow

def plot_flows(input_file,node_list):
  '''plot the flows over time given an input file and list of nodes you are observing'''
  
  # create dataframe with simulation data for all nodes
  allflow = combine_allnodes(input_file, node_list)

  # Set up figure
  plt.figure(figsize=(20, 5), dpi=100)

  # plot the flows of each node
  for n in node_list:
    plt.plot(allflow[n], linewidth=2.0, label = n)

  # plot formatting
  plt.title("flows at each node") # title
  plt.ylabel("Flow (CFS)") # y-axis label
  plt.xlabel("Simulation Time") # x-axis label
  plt.legend(loc="upper right") # create legend
  plt.savefig("images/flow_fig.png") # save figure

def node_list(input_file):
  
  sim = pyswmm.Simulation(input_file)
  nodes = pyswmm.Nodes(sim)
  node_lst = []

  for node in nodes:
    node_lst.append(node.nodeid)
  return node_lst