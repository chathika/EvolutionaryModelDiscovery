'''EvolutionaryModelDiscovery: Automated agent rule generation and 
importance evaluation for agent-based models with Genetic Programming.
Copyright (C) 2018  Chathika Gunaratne
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.'''
import os.path
import re
import unicodedata
from .Util import *
import os, re
import time
import uuid
'''Responsible for Writing Customized NetLogo models for EMD'''
class NetLogoWriter:
    
    '''locate the NetLogo file, read it in, and identify the line to be experimented with as EMD_line.'''
    def __init__(self, model_string):
        self.EMD_return_type = None
        self.EMD_line = -1000
        self.terminal_by_type = {}
        self.original_model_path = model_string
        model_dir = os.path.relpath(os.path.dirname(model_string))

        #find EMD entry point
        wait_for_files([self.original_model_path])
        with  open(self.original_model_path, 'r') as file_reader:#should probably catch an exception here
            for i, line in enumerate(file_reader):      
                line = line.lower()          
                if "@emd" in line and "@evolvenextline" in line:
                    self.EMD_line = i + 1
                    emd_parameters = netlogo_EMD_line_to_array(line)[3:]
                    for emd_parameter in emd_parameters:
                        if "factors-file=" in emd_parameter:
                            self.rel_factors_file_path = emd_parameter.replace("factors-file=", "")
                            self.factors_file_path = os.path.join(model_dir,self.rel_factors_file_path)
                            '''elif "terminal=" in emd_parameter:
                                terminalType = emd_parameter.replace("terminal=", "")[0]
                                terminal = emd_parameter.replace("terminal=", "")[1]
                                if terminalType in self.terminal_by_type.keys():
                                    self.terminal_by_type[terminalType].append(terminal)
                                else:
                                    self.terminal_by_type[terminalType] = [terminal]'''
                        elif "return-type=" in emd_parameter:
                            self.EMD_return_type = "EMD" + emd_parameter.replace("return-type=", "")     
                            self.EMD_return_type = slugify(self.EMD_return_type)
            file_reader.close()
        if (self.EMD_line < 0):
            raise ValueError("No @EMD annotation detected!")
        if (self.rel_factors_file_path == ""):
            raise ValueError("No @factors-file annotation was detected!")
                    
    '''def getTerminalsByTypes(self):
        return self.terminal_by_type'''
    def get_factors_file_path(self):
        return self.factors_file_path
    def get_EMD_return_type(self):
        return self.EMD_return_type
    '''if EMD annotation exists, then inject the new rule string'''
    def inject_new_rule (self, new_rule):
        # with is like your try .. finally block in this case
        #wait_for_files([self.original_model_path])
        with open(self.original_model_path, 'r') as file:  #should probably catch an exception here
            # read a list of lines into data
            data = file.readlines()
            file.close()
        self.rule_injected_model_path = self.original_model_path[:-5] + slugify(uuid.uuid4().hex) + ".EMD.nlogo"
        if not (os.path.isfile(self.rule_injected_model_path)):
            #print("Model already injected with this rule. Using cached version.")
            if self.EMD_line >= 0:
                #print( "Your line: " + data[self.EMD_line])
                data[self.EMD_line] = new_rule
                # and write everything back
                #wait_for_files([self.rule_injected_model_path])
                with open(self.rule_injected_model_path, 'w') as file:
                    file.writelines( data )
                    file.flush()
                    file.close()
        return self.rule_injected_model_path
