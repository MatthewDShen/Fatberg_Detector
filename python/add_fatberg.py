import pyswmm
import swmm_api



'''
Summary: The following function runs the input file and changes a pipe from circular to filled circular
Inputs: path of input file
Output: report file
'''



str_path = '/home/matthewdshen/GitHub/Fatberg_Detector/test/Test_Network_clear.inp'

inp = swmm_api.SwmmInput.read_file(str_path)

inp[swmm_api.input_file.section_labels.XSECTIONS]['1'].shape = 'FILLED_CIRCULAR'

inp[swmm_api.input_file.section_labels.XSECTIONS]['1'].transect = 0.75

inp.write_file('new_inputfile.inp')













# with pyswmm.Simulation(str_path) as sim:
#     lst_linkids = []

#     for link in pyswmm.Links(sim):
#         lst_linkids.append(link.linkid)

#     print(lst_linkids)







