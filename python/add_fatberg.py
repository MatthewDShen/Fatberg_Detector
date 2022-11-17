import pyswmm
import swmm_api
import random




str_path = '/home/matthewdshen/GitHub/Fatberg_Detector/test/Test_Network_clear.inp'

def func_add_fatberg(str_path):
    
    '''
    Summary: The following function runs the input file and changes a pipe from circular to filled circular
    Inputs: path of input file
    Output: report file
    '''
    with pyswmm.Simulation(str_path) as sim:
        lst_linkids = []

        for link in pyswmm.Links(sim):
            lst_linkids.append(link.linkid)

        inp = swmm_api.SwmmInput.read_file(str_path)

        fatberg_link = random.choice(lst_linkids)

        # inp[swmm_api.input_file.section_labels.XSECTIONS][fatberg_link].shape = 'FILLED_CIRCULAR'

        inp[swmm_api.input_file.section_labels.XSECTIONS][fatberg_link].transect = .75

        inp.write_file('/home/matthewdshen/GitHub/Fatberg_Detector/test/Test_Network_fatberg.inp')


func_add_fatberg(str_path)




