import pyswmm, random
from nodes_total_inflow import combine_allnodes, node_list

str_clean = 'swmm_files/clean/Test_Network_clean.inp'

str_dirty = 'swmm_files/dirty/Test_Network_dirty' + str(random.randint(0,22)) + '.inp'

print(combine_allnodes(str_clean,node_list(str_clean)))