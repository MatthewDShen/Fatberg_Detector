# Import libraries
import pyswmm

# Path for model
str_path = ''

# Run control
sim = pyswmm.Simulation(str_path)
sim.execute()

# Run variables estimation
with pyswmm.Simulation(str_path) as sim:
    link_object = pyswmm.Links(sim)

    #C1:C2 link instantiation
    c1c2 = link_object["C1:C2"]
    print(c1c2.flow_limit)
    print(c1c2.is_conduit())

    #Step through a simulation
    for step in sim:
        print(c1c2.flow)
        if c1c2.flow > 10.0:
            c1c2.target_setting = 0.5