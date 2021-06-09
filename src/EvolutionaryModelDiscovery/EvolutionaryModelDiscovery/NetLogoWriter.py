"""EvolutionaryModelDiscovery: Automated agent rule generation and 
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
along with this program.  If not, see <http://www.gnu.org/licenses/>."""

from .Util import *
from pathlib import Path
import uuid

class NetLogoWriter:
    """
    Responsible for reading from original .nlogo and .nls files and writing modified NetLogo models
    
    """    
    
    def __init__(self, model_path : str) -> None:
        """
        Locate the NetLogo file, read it in, and identify the line to be experimented with.

        :params model_path: location of .nlogo model file.
        """
        self._EMD_return_type = None
        self._EMD_line = -1000
        self._original_model_path = model_path
        self._factors_file_path = model_path

        #find EMD entry point
        wait_for_files([self._original_model_path])
        with  open(self._original_model_path, 'r') as file_reader:
            for i, line in enumerate(file_reader):      
                line = line.lower()         
                if "@emd" in line and "@evolvenextline" in line:
                    self._EMD_line = i + 1
                    emd_parameters = netlogo_EMD_line_to_array(line)[3:]
                    for emd_parameter in emd_parameters:
                        if "factors-file=" in emd_parameter:
                            rel_factors_file_path = Path(emd_parameter.replace("factors-file=", ""))
                            assert rel_factors_file_path == "", "No @factors-file annotation was detected!"
                            self._factors_file_path = str(rel_factors_file_path.absolute())
                        elif "return-type=" in emd_parameter:
                            self._EMD_return_type = "EMD" + emd_parameter.replace("return-type=", "")     
                            self._EMD_return_type = slugify(self._EMD_return_type)
            file_reader.close()
        assert (self._EMD_line > 0) , "No @EMD @EvolveNextLine annotation detected!"
    
    def get_factors_file_path(self) -> str:
        """
        Where the factors file is located. Could be in the .nlogo file or a .nls file.

        :returns: location of factors file.
        """
        return self._factors_file_path

    def get_EMD_return_type(self) -> str:
        """
        Gets the annotated return type required by the root node of the syntax tree.

        :returns: required root return type as str.
        """
        return self._EMD_return_type

    def inject_new_rule (self, new_rule : str) -> str:
        """
        Injects new rule into the line following the @EvolveNextLine annotation and saves it as a 
        .EMD.nlogo model file. 

        :param new_rule: new rule to be injected into the model.
        :returns: path to modified model file.
        """
    
        with open(self._original_model_path, 'r') as file:
            data = file.readlines()
            file.close()
        dir = Path(self._original_model_path).parent.absolute()
        model_name = Path(self._original_model_path).stem
        uniq = slugify(uuid.uuid4().hex)
        rule_injected_model_path = Path(dir,'.cache',f'{model_name}_{uniq}.EMD.nlogo')
        rule_injected_model_path.parent.absolute().mkdir(parents=True, exist_ok=True)
        if not (Path.is_file(rule_injected_model_path)):
            # Model already injected with this rule. Using cached version.
            if self._EMD_line >= 0:
                data[self._EMD_line] = new_rule
                # And write everything to new model file.
                with open(rule_injected_model_path, 'w') as file:
                    file.writelines(data)
                    file.flush()
                    file.close()
        return str(rule_injected_model_path)


"""
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
        model_dir = os.path.abspath(os.path.dirname(model_string))

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
                        elif "return-type=" in emd_parameter:
                            self.EMD_return_type = "EMD" + emd_parameter.replace("return-type=", "")     
                            self.EMD_return_type = slugify(self.EMD_return_type)
            file_reader.close()
                    
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
            # Model already injected with this rule. Using cached version.
            if self.EMD_line >= 0:
                data[self.EMD_line] = new_rule
                # and write everything back
                #wait_for_files([self.rule_injected_model_path])
                with open(self.rule_injected_model_path, 'w') as file:
                    file.writelines( data )
                    file.flush()
                    file.close()
        return self.rule_injected_model_path

"""