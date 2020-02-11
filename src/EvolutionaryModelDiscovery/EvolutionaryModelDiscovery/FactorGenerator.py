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
    _factors = None
    _operators = None
    _negativeOps = None
    _typeSignatures = None # map of return types to possible parameters 
    _types = None
    _modelFactorsPath = ""
    def __init__(self):        
        self._factors = []
        self._operators = []
        self._negativeOps = {}
        self._interactions = []
        self._typeSignatures = {}
        self._types = set([])
        self._modelFactorsPath = getModelFactorsPath()
    def generate(self,factorFilePath):
        self.readNetLogoFunctionFile(factorFilePath)    
        self.extractNLTypes()
        self.writePythonClasses()        
    # Read the factors from a .nls file
    def readNetLogoFunctionFile(self,factorFilePath):
        with open(str(factorFilePath.replace("\"","").replace("'","")),"r") as f: 
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
                        emd_parameters = netLogoEMDLineToArray(line)[3:]
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
                                print("Invalid EMD annotation argument at line {0}.".format(lineNumber))
                elif "to" in line or "to-report" in line:
                    factor = Factor(re.sub("[\s]+"," ",line).split(" ")[1])
                    factor.setReturnType(factor_return_type)
                    for factor_parameter_type in factor_parameter_types:
                        factor.addParameterType(factor_parameter_type)
                    self._factors.append(factor)
                    if operator_identified:
                        if "-" in parameter_contributions_to_fitness:
                            self._negativeOps[factor.getSafeName()] = [ -1 if sgn == "-" else 1 for sgn in parameter_contributions_to_fitness]
                        self._operators.append(factor)
                    if interaction_identified:
                        self._interactions.append(factor.getSafeName())
                    factor_identified = False
                    operator_identified = False
                    interaction_identified = False
                    factor = None
            self._interactions = list(set(self._interactions))
    #define the factor classes 
    '''def extractNLTypeSignatures(self):        
        for factor in self._factors:
            if factor.getReturnType() in self._typeSignatures.keys() :
                parameters = self._typeSignatures[str(factor.getReturnType())]
                parameters.append(factor.getParameterTypes())                
                self._typeSignatures[str(factor.getReturnType())] = [ii for n,ii in enumerate(parameters) if ii not in parameters[:n]]
            else:
                self._typeSignatures[str(factor.getReturnType())] = [factor.getParameterTypes()]
        print(self._typeSignatures)'''
    def extractNLTypes(self):
        for factor in self._factors:
            self._types.add(factor.getReturnType())
            self._types = self._types.union(set(factor.getParameterTypes()))
        #print(self._typeSignatures)
    def writePythonClasses(self):
        if os.path.exists(self._modelFactorsPath):
            os.remove(self._modelFactorsPath)
        self.writeClassNames()
        self.writeNegativeOpsDictionary()
        self.writeMeasureableFactors()
        self.writeInteractions()
        for factor in self._factors:
            self.writePythonClassFromFactor(factor)
        for nlType in self._types:
            self.writePythonClassFromNLType(nlType)
    def writeClassNames(self):
        classNamesString = "\nclassNames = ["
        with open(self._modelFactorsPath, "a+") as f:
            for factor in self._factors:
                classNamesString = '{0}"{1}",'.format(classNamesString,factor.getSafeName())
            classNamesString = classNamesString[:(len(classNamesString)-1)] + "]"
            f.write(classNamesString)
    def writePythonClassFromFactor(self, factor):
        # Compile the NetLogo String for the factor
        parameterString = " "
        occurances = 0
        for parameterType in factor.getParameterTypes():            
            parameterString = parameterString + "{0}, ".format((parameterType + str(occurances)))
            occurances = occurances + 1
        parameterString = parameterString[:-2]
        netlogoString = '"( {0} '.format(str(factor.getName()))
        occurances = 0
        for parameterType in factor.getParameterTypes():
            netlogoString = netlogoString +  '(" + str({0}) + ") '.format((parameterType +  str(occurances))) 
            occurances = occurances + 1
        netlogoString = netlogoString + '"'
        netlogoString = '{0} + " ) "'.format(netlogoString)
        with open(self._modelFactorsPath, "a+") as f:
            f.write ("\nclass {0}:".format(factor.getSafeName()))
            f.write('\n\t__name__ = "{0}"'.format(factor.getSafeName()))
            f.write('\n\tdef __init__(self,{0}):'.format(parameterString))
            f.write('\n\t\tself.__name__ = {0}'.format(netlogoString))
            f.write('\n\tdef __str__(self):')
            f.write('\n\t\treturn self.__name__')
            f.write('\n\tdef __repr__(self):')
            f.write('\n\t\treturn self.__name__')
            f.flush()
            f.close()
    def writePythonClassFromNLType(self,nlType):
        with open(self._modelFactorsPath, "a+") as f:
            f.write ("\nclass {0}:".format(nlType))
            f.write('\n\t__name__ = "{0}"'.format(nlType))
            f.write('\n\tdef __init__(self, nlString):')
            f.write('\n\t\tself.__name__ = str(nlString)')
            f.write('\n\tdef __str__(self):')
            f.write('\n\t\treturn self.__name__')
            f.write('\n\tdef __repr__(self):')
            f.write('\n\t\treturn self.__name__')
            f.flush()
            f.close()
    def writeNegativeOpsDictionary(self):
        with open(self._modelFactorsPath, "a+") as f:
            f.write("\nnegativeOps = ")
            f.write(str(self.getNegativeOps()))
            f.flush()
            f.close()
    def writeMeasureableFactors(self):
        with open(self._modelFactorsPath, "a+") as f:
            f.write("\nmeasureableFactors = ")
            f.write(str(self.getMeasureableFactors()))
            f.flush()
            f.close()
    def writeInteractions(self):
        with open(self._modelFactorsPath, "a+") as f:
            f.write("\ninteractions = ")
            f.write(str(self.getInteractions()))
            f.flush()
            f.close()
    def getFactors(self):
        return self._factors
    def getOperators(self):
        return self._operators
    def getNegativeOps(self):
        return self._negativeOps
    def getMeasureableFactors(self):
        measureableFactors = []        
        for f in [ fac.getSafeName() for fac in self._factors]:
            if not f in [op.getSafeName() for op in self._operators]:
                measureableFactors.append(f)
        return measureableFactors
    def getInteractions(self):
        return self._interactions
