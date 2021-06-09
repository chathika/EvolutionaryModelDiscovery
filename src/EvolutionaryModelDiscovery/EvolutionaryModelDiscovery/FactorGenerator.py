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
from .Factor import Factor 
import re
import os
from .Util import *
#Uses annotations as follows:
# @EMD: return-type: what type is returned
# @EMD: parameter-type: parameter types
class FactorGenerator:
    
    def __init__(self):        
        self._factors = []
        self._operators = []
        self._negativeOps = {}
        self._interactions = []
        self._typeSignatures = {}
        self._types = set([])
        self.model_factor_path = get_model_factors_path()
    def generate(self,factor_file_path):
        self.read_netlogo_function_file(factor_file_path)    
        self.extract_NL_types()
        self.write_python_classes()        
    # Read the factors from a .nls file
    def read_netlogo_function_file(self,factor_file_path):
        with open(str(factor_file_path.replace("\"","").replace("'","")),"r") as f: 
            factor_identified = False
            operator_identified = False
            interaction_identified = False
            factor_return_type = ""
            factor_parameter_types = []
            parameter_contributions_to_fitness = []
            lineNumber = 0
            for line in f: 
                line = line.lower()
                lineNumber = lineNumber + 1                
                if not factor_identified:                    
                    if "@emd" in line and ("@factor" in line  or "@operator" in line)  and not ("@evolvenextline" in line) :
                        factor_identified = True
                        if "@operator" in line:
                            operator_identified = True
                        factor_return_type = ""
                        factor_parameter_types = []
                        emd_parameters = netlogo_EMD_line_to_array(line)[3:]
                        for emd_parameter in emd_parameters:
                            if "return-type=" in emd_parameter:
                                factor_return_type = "EMD" + emd_parameter.replace("return-type=", "")
                            elif "parameter-type=" in emd_parameter:
                                parameter_type = emd_parameter.replace("parameter-type=", "")
                                factor_parameter_types.append("EMD" + parameter_type )
                            elif "structure=" in emd_parameter:
                                parameter_contributions_to_fitness = emd_parameter.replace("structure=", "")[1:-1].split(",")
                            elif "interaction" in emd_parameter:
                                interaction_identified = True
                            else:
                                raise Exception("Invalid EMD annotation argument {1} at line {0}.".format(lineNumber, emd_parameter))
                elif "to" in line or "to-report" in line:
                    factor = Factor(re.sub("[\s]+"," ",line).split(" ")[1])
                    factor.set_return_type(factor_return_type)
                    for factor_parameter_type in factor_parameter_types:
                        factor.add_parameter_type(factor_parameter_type)
                    self._factors.append(factor)
                    if operator_identified:
                        if "-" in parameter_contributions_to_fitness:
                            self._negativeOps[factor.get_safe_name()] = [ -1 if sgn == "-" else 1 for sgn in parameter_contributions_to_fitness]
                        self._operators.append(factor)
                    if interaction_identified:
                        self._interactions.append(factor.get_safe_name())
                    factor_identified = False
                    operator_identified = False
                    interaction_identified = False
                    factor = None
            self._interactions = list(set(self._interactions))
    
    def extract_NL_types(self):
        for factor in self._factors:
            self._types.add(factor.get_return_type())
            self._types = self._types.union(set(factor.get_parameter_types()))
    def write_python_classes(self):
        #if os.path.exists(self.model_factor_path):
        #    os.remove(self.model_factor_path)
        self.write_class_names()
        self.write_negative_ops_dictionary()
        self.write_measureable_factors()
        self.write_interactions()
        for factor in self._factors:
            self.write_python_class_from_factor(factor)
        for nlType in self._types:
            self.write_python_class_from_nl_type(nlType)
    def write_class_names(self):
        classNamesString = "\nclassNames = ["
        with open(self.model_factor_path, "a+") as f:
            for factor in self._factors:
                classNamesString = '{0}"{1}",'.format(classNamesString,factor.get_safe_name())
            classNamesString = classNamesString[:(len(classNamesString)-1)] + "]"
            f.write(classNamesString)
    def write_python_class_from_factor(self, factor):
        # Compile the NetLogo String for the factor
        parameterString = " "
        occurances = 0
        for parameterType in factor.get_parameter_types():            
            parameterString = parameterString + "{0}, ".format((parameterType + str(occurances)))
            occurances = occurances + 1
        parameterString = parameterString[:-2]
        netlogoString = '"( {0} '.format(str(factor.get_name()))
        occurances = 0
        for parameterType in factor.get_parameter_types():
            netlogoString = netlogoString +  '(" + str({0}) + ") '.format((parameterType +  str(occurances))) 
            occurances = occurances + 1
        netlogoString = netlogoString + '"'
        netlogoString = '{0} + " ) "'.format(netlogoString)
        with open(self.model_factor_path, "a+") as f:
            f.write ("\nclass {0}:".format(factor.get_safe_name()))
            f.write('\n\t__name__ = "{0}"'.format(factor.get_safe_name()))
            f.write('\n\tdef __init__(self,{0}):'.format(parameterString))
            f.write('\n\t\tself.__name__ = {0}'.format(netlogoString))
            f.write('\n\tdef __str__(self):')
            f.write('\n\t\treturn self.__name__')
            f.write('\n\tdef __repr__(self):')
            f.write('\n\t\treturn self.__name__')
            f.flush()
            f.close()
    def write_python_class_from_nl_type(self,nlType):
        with open(self.model_factor_path, "a+") as f:
            f.write ("\nclass {0}:".format(nlType))
            f.write('\n\t__name__ = "{0}"'.format(nlType))
            f.write('\n\tdef __init__(self, nl_string):')
            f.write('\n\t\tself.__name__ = str(nl_string)')
            f.write('\n\tdef __str__(self):')
            f.write('\n\t\treturn self.__name__')
            f.write('\n\tdef __repr__(self):')
            f.write('\n\t\treturn self.__name__')
            f.flush()
            f.close()
    def write_negative_ops_dictionary(self):
        with open(self.model_factor_path, "a+") as f:
            f.write("\nnegativeOps = ")
            f.write(str(self.get_negative_ops()))
            f.flush()
            f.close()
    def write_measureable_factors(self):
        with open(self.model_factor_path, "a+") as f:
            f.write("\nmeasureable_factors = ")
            f.write(str(self.get_measureable_factors()))
            f.flush()
            f.close()
    def write_interactions(self):
        with open(self.model_factor_path, "a+") as f:
            f.write("\ninteractions = ")
            f.write(str(self.get_interactions()))
            f.flush()
            f.close()
    def get_factors(self):
        return self._factors
    def get_operators(self):
        return self._operators
    def get_negative_ops(self):
        return self._negativeOps
    def get_measureable_factors(self):
        measureable_factors = []        
        for f in [ fac.get_safe_name() for fac in self._factors]:
            if not f in [op.get_safe_name() for op in self._operators]:
                measureable_factors.append(f)
        return measureable_factors
    def get_interactions(self):
        return self._interactions
