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
'''Responsible for Writing Customized NetLogo models for EMD'''
class NetLogoWriter:
    __original_model_path = ""
    __rule_injected_model_path = ""
    __factorsFilePath = ""
    #__terminalsByTypes = None
    __EMDReturnType = None
    __EMD_line = -1000
    
    '''locate the NetLogo file, read it in, and identify the line to be experimented with as EMD_line.'''
    def __init__(self, model_string):
        self.__terminalsByTypes = {}
        self.__original_model_path = model_string
        #purge(".",".*.EMD.nlogo")
        #find EMD entry point
        wait_for_files([self.__original_model_path])
        with  open(self.__original_model_path, 'r') as file_reader:#should probably catch an exception here
            for i, line in enumerate(file_reader):      
                line = line.lower()          
                if "@emd" in line and "@evolvenextline" in line:
                    self.__EMD_line = i + 1
                    emd_parameters = netLogoEMDLineToArray(line)[3:]
                    for emd_parameter in emd_parameters:
                        if "factors-file=" in emd_parameter:
                            self.__factorsFilePath = emd_parameter.replace("factors-file=", "")                            
                            '''elif "terminal=" in emd_parameter:
                                terminalType = emd_parameter.replace("terminal=", "")[0]
                                terminal = emd_parameter.replace("terminal=", "")[1]
                                if terminalType in self.__terminalsByTypes.keys():
                                    self.__terminalsByTypes[terminalType].append(terminal)
                                else:
                                    self.__terminalsByTypes[terminalType] = [terminal]'''
                        elif "return-type=" in emd_parameter:
                            self.__EMDReturnType = "EMD" + emd_parameter.replace("return-type=", "")     
            file_reader.close()
        if (self.__EMD_line < 0):
            raise ValueError("No @EMD annotation detected!")
        if (self.__factorsFilePath == ""):
            raise ValueError("No @factors-file annotation was detected!")
                    
    '''def getTerminalsByTypes(self):
        return self.__terminalsByTypes'''
    def getFactorsFilePath(self):
        return self.__factorsFilePath
    def getEMDReturnType(self):
        return self.__EMDReturnType
    '''if EMD annotation exists, then inject the new rule string'''
    def injectNewRule (self, new_rule):
        # with is like your try .. finally block in this case
        wait_for_files([self.__original_model_path])
        with open(self.__original_model_path, 'r') as file:  #should probably catch an exception here
            # read a list of lines into data
            data = file.readlines()
            file.close()
        self.__rule_injected_model_path = self.__original_model_path[:-5] + slugify(new_rule) + ".EMD.nlogo"
        if not (os.path.isfile(self.__rule_injected_model_path)):
            #print("Model already injected with this rule. Using cached version.")
            if self.__EMD_line >= 0:
                #print( "Your line: " + data[self.__EMD_line])
                data[self.__EMD_line] = new_rule
                # and write everything back
                wait_for_files([self.__rule_injected_model_path])
                with open(self.__rule_injected_model_path, 'w') as file:
                    file.writelines( data )
                    file.flush()
                    file.close()
        return self.__rule_injected_model_path
def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens."""
    value = str(re.sub('[^\w\s-]', '', value).strip().lower())
    value = str(re.sub('[-\s]+', '-', value))
    return value

def purge(dir, pattern):
    for f in os.listdir(dir):
        if re.search(pattern, f):
            os.remove(os.path.join(dir, f))

def is_locked(filepath):
    """Checks if a file is locked by opening it in append mode.
    If no exception thrown, then the file is not locked.
    """
    locked = None
    file_object = None
    #if os.path.exists(filepath):
    try:
        #print("Trying to open {0}.".format( filepath))
        buffer_size = 8
        # Opening file in append mode and read the first 8 characters.
        file_object = open(filepath, 'a', buffer_size)
        if file_object:
            #print("{0} is not locked.".format(filepath))
            locked = False
    except IOError as message:
        #print("File is locked (unable to open in append mode).{0}.".format(message))
        locked = True
    finally:
        if file_object:
            file_object.close()
            #print("{0} closed.".format(filepath))
    #else:
    #    print("{0} not found.".format(filepath))
    return locked

def wait_for_files(filepaths):
    """Checks if the files are ready.

    For a file to be ready it must exist and can be opened in append
    mode.
    """
    wait_time = 0.05
    for filepath in filepaths:
        # If the file doesn't exist, wait wait_time seconds and try again
        # until it's found.
        #while not os.path.exists(filepath):
        #    print("{0} hasn't arrived. Waiting {1} seconds.".format(filepath, wait_time))
        #    time.sleep(wait_time)
        # If the file exists but locked, wait wait_time seconds and check
        # again until it's no longer locked by another process.
        while is_locked(filepath):
            #print("{0} is currently in use. Waiting {1} seconds.".format(filepath, wait_time))
            time.sleep(wait_time)