'''The ABM with all its flexibility as EMD sees it'''
'''EMD can use this class to control, set parameters, query results from'''
'''and most importantly, change rules within the NetLogo model specified'''
class ABM_NetLogo:
    path_to_model = ""
    model_as_text = ""
    parameters = []
    __nlogo_writer = None 
    def __init__(self, path_to_model):
        self.path_to_model = path_to_model
        __nlogo_writer = NetLogo_Writer(path_to_model)
        #Read in the model to memory (instead of repeated disk reads)
        print()
    def inject_new_rule(self, new_rule):
        #locate tag comment
        __nlogo_writer.injectNewRule(new_rule)
        #Replace line under tag with new_rule
        
        #Write model 
        
        #Flush, close
        print()
    def set_parameters(self, parameter_values):
        print()
    def get_parameter_names(self):
        #Return parameter names
        print()
    def run_abm(self):
        #Run the ABM
        print()