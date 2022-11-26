import random, pyswmm, pandas as pd, swmm.toolkit

# Clean file path inp
str_inp_clean = 'swmm_files/clean/Test_Network_clean.inp'

# Dirty path file inp
str_inp_dirty = 'swmm_files/dirty/Test_Network_dirty' + str(random.randint(0,22)) + '.inp'

# Run clean simulation
sim_clean = pyswmm.Simulation(str_inp_clean)

# Run dirty simulation
sim_dirty = pyswmm.Simulation(str_inp_clean)

# Get nodes from simulation
nodes = pyswmm.Nodes(sim_clean)

# Initialize list of nodes
lst_nodes = []

# Add nodes to list
for node in nodes:
    lst_nodes.append(node.nodeid)

# Pull links from simulation
links = pyswmm.Links(sim_clean)

# Initialize list of links
lst_links = []

# Add links to a list
for link in links:
    lst_links.append(link.linkid)

# Initialize lists
upstream_node = []
downstream_node = []

# Get upstream and downstream links
for link in pyswmm.Links(sim_clean):
    # Append upstream node to link
    upstream_node.append(link.connections[0])

    # Append downstream node to link
    downstream_node.append(link.connections[1])


# Clean path file out    
str_out_clean = str_inp_clean[:-4] + '.out'  
    
# Dirty path file out    
str_out_dirty = str_inp_dirty[:-4] + '.out'   

# Save inflows to dataframe
lst_inflow = []

out = pyswmm.output.Output(str_out_dirty)

# Get total inflow from output file
data = out.node_attribute(swmm.toolkit.shared_enum.NodeAttribute.TOTAL_INFLOW)

# Store inflow data
for object in data:
    # print(object, data[object]) 
    lst_inflow.append(data[object]) 

print(lst_inflow)



df_sim = pd.DataFrame(data = {
    'Link ID': lst_links,
    'upstream node': upstream_node,
    'downstream node': downstream_node,
})

print('')