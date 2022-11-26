import pyswmm, random
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

    # Specify the node we are interested in monitoring
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

    print(df_node)

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
  '''Get list of nodes given the input file'''
  # Run simulation
  sim = pyswmm.Simulation(input_file)

  # Pull nodes from simulation
  nodes = pyswmm.Nodes(sim)

  # Initialize list of nodes
  node_lst = []

  # Add nodes to a list
  for node in nodes:
    node_lst.append(node.nodeid)
    
  return node_lst

def link_list(input_file):
  '''Get list of links given the input file'''
  # Run simulation
  sim = pyswmm.Simulation(input_file)

  # Pull nodes from simulation
  links = pyswmm.Links(sim)

  # Initialize list of nodes
  link_lst = []

  # Add nodes to a list
  for link in links:
    link_lst.append(link.linkid)
    
  return link_lst

def get_fatberg_dataframe(str_clean_input_file,str_dirty_input_file,node_lst):

  # Get dataframe with all flows without fatberg
  df_clean_flows = combine_allnodes(str_clean_input_file,node_lst)

  # Get dataframe with all flows with fatberg
  df_dirty_flows = combine_allnodes(str_dirty_input_file,node_lst)

  # Get the difference in flows between clean and dirty with the mean
  df_delta_flows = df_clean_flows.mean() - df_dirty_flows.mean()

  # Get downstream node of fatberg link
  str_downstream_fatberg_node = df_delta_flows.idxmax()

  # Run simulation
  sim = pyswmm.Simulation(str_clean_input_file)

  # Initialize lists
  upstream_node = []
  downstream_node = []

  for link in pyswmm.Links(sim):
    # Append upstream node to link
    upstream_node.append(link.connections[0])

    # Append downstream node to link
    downstream_node.append(link.connections[1])

  # Get list of all links in system
  lst_links = link_list(str_clean_input_file)

  # Create dataframe with link names, upstream nodes, and downstream nodes
  df_links = pd.DataFrame(data = {'link name': lst_links,'upstream node': upstream_node,'downstream node': downstream_node})

  # Get name of starting links with a suspected fatberg
  df_search_links = df_links[df_links['downstream node'] == str_downstream_fatberg_node].reset_index()

  # initalize variables for loop
  df_suspect_links = pd.DataFrame()


  # loop through search links dataframe until empty
  while len(df_search_links) > 0:

    # Check if upstream values need to be added to search
    if df_delta_flows[df_search_links['upstream node'][0]] != 0: # If the flow delta between clean and dirty at the search junction is equal to 0 
      
      # Find links that are upstream of the search link
      df_upstream = df_links[df_links['downstream node'] == df_search_links['upstream node'][0]]

      # Add upstream links to search dataframe
      df_search_links = pd.concat([df_search_links,df_upstream], ignore_index= True)

    # add searched link to suspected link
    df_suspect_links = pd.concat([df_suspect_links,df_search_links.iloc[0]])

    # Drop searched row
    df_search_links = df_search_links.iloc[1: , :]


  return df_suspect_links


get_inflow('swmm_files/clean/Test_Network_clean.inp')


