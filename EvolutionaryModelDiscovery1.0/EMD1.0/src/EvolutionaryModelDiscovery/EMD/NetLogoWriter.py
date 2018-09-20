import os.path
import re
import unicodedata
import Util
'''Responsible for Writing Customized NetLogo models for EMD'''
class NetLogoWriter:
    __original_model_path = ""
    __rule_injected_model_path = ""
    __factorsFile = ""
    __terminalsByTypes = None
    __EMD_line = -1000
    
    '''locate the NetLogo file, read it in, and identify the line to be experimented with as EMD_line.'''
    def __init__(self, model_string):
        self.__terminalsByTypes = {}
        self.__original_model_path = model_string
        #find EMD entry point
        with  open(self.__original_model_path, 'r') as file_reader:#should probably catch an exception here
            for i, line in enumerate(file_reader):
                if "@emd" in line and "@evolvenextline" in line.lower():
                    self.__EMD_line = i + 1
                    emd_parameters = Util.netLogoEMDLineToArray(line)[3:]
                    for emd_parameter in emd_parameters:
                        if "factors-file=" in emd_parameter:
                            self.__factorsFile = emd_parameter.replace("factors-file=", "")
                        elif "terminal=" in emd_parameter:
                            terminalType = emd_parameter.replace("terminal=", "")[0]
                            terminal = emd_parameter.replace("terminal=", "")[1]
                            if terminalType in self.__terminalsByTypes.keys():
                                self.__terminalsByTypes[terminalType].append(terminal)
                            else:
                                self.__terminalsByTypes[terminalType] = [terminal]
                    
    def getTerminalsByTypes(self):
        return self.__terminalsByTypes
    def getFactorsFiles(self):
        return self.__factorsFile
    '''if EMD annotation exists, then inject the new rule string'''
    def injectNewRule (self, new_rule):
        # with is like your try .. finally block in this case
        with open(self.__original_model_path, 'r') as file:  #should probably catch an exception here
            # read a list of lines into data
            data = file.readlines()
            file.close()
        self.__rule_injected_model_path = self.__original_model_path[:-5] + slugify(new_rule) + ".nlogo"
        if not (os.path.isfile(self.__rule_injected_model_path)):
            #print("Model already injected with this rule. Using cached version.")
            if self.__EMD_line >= 0:
                #print( "Your line: " + data[self.__EMD_line])
                data[self.__EMD_line] = new_rule
                # and write everything back
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