from Factor import Factor 
import re
import os
import Util
#Uses annotations as follows:
# @EMD: return-type: what type is returned
# @EMD: parameter-type: parameter types
class FactorGenerator:
    _factors = None
    _typeSignatures = None # map of return types to possible parameters 
    _types = None
    _FUNCTIONS_FILE_PATH = "ModelFactors.py"
    def __init__(self):
        self._factors = []
        self._typeSignatures = {}
        self._types = set([])
    def generate(self,factorFilePath):
        self.readNetLogoFunctionFile(factorFilePath)    
        self.extractNLTypes()
        self.writePythonClasses()        
    # Read the factors from a .nls file
    def readNetLogoFunctionFile(self,factorFilePath):
        with open(factorFilePath) as f: 
            factor_identified = False
            factor_return_type = ""
            factor_parameter_types = []
            for line in f: 
                line = line.lower()
                if not factor_identified:
                    if "@emd" in line and "@factor" in line:
                        factor_identified = True
                        factor_return_type = ""
                        factor_parameter_types = []
                        emd_parameters = Util.netLogoEMDLineToArray(line)[3:]
                        for emd_parameter in emd_parameters:
                            if "return-type=" in emd_parameter:
                                factor_return_type = emd_parameter.replace("return-type=", "")
                            elif "parameter-type=" in emd_parameter:
                                factor_parameter_types.append(emd_parameter.replace("parameter-type=", ""))
                            else:
                                print("Invalid EMD annotation argument.")
                elif "to" in line or "to-report" in line:
                    factor = Factor(re.sub("[\s]+"," ",line).split(" ")[1])
                    factor.setReturnType(factor_return_type)
                    for factor_parameter_type in factor_parameter_types:
                        factor.addParameterType(factor_parameter_type)
                    self._factors.append(factor)
                    factor_identified = False
                    factor = None
    #define the factor classes 
    def extractNLTypeSignatures(self):        
        for factor in self._factors:
            if factor.getReturnType() in self._typeSignatures.keys() :
                parameters = self._typeSignatures[str(factor.getReturnType())]
                parameters.append(factor.getParameterTypes())                
                self._typeSignatures[str(factor.getReturnType())] = [ii for n,ii in enumerate(parameters) if ii not in parameters[:n]]
            else:
                self._typeSignatures[str(factor.getReturnType())] = [factor.getParameterTypes()]
        print(self._typeSignatures)
    def extractNLTypes(self):
        for factor in self._factors:
            self._types.add(factor.getReturnType())
            self._types = self._types.union(set(factor.getParameterTypes()))
        #print(self._typeSignatures)
    def writePythonClasses(self):
        if os.path.exists(self._FUNCTIONS_FILE_PATH):
            os.remove(self._FUNCTIONS_FILE_PATH)
        self.writeClassNames()
        for factor in self._factors:
            self.writePythonClassFromFactor(factor)
        for nlType in self._types:
            self.writePythonClassFromNLType(nlType)
    def writeClassNames(self):
        classNamesString = "\nclassNames = ["
        with open(self._FUNCTIONS_FILE_PATH, "a+") as f:
            for factor in self._factors:
                classNamesString = '{0}"{1}",'.format(classNamesString,factor.getSafeName())
            classNamesString = classNamesString[:(len(classNamesString)-1)] + "]"
            f.write(classNamesString)
    def writePythonClassFromFactor(self, factor):
        # Compile the NetLogo String for the factor
        parameterString = " "
        for parameterType in factor.getParameterTypes():
            parameterString = parameterString + "{0}, ".format(parameterType)
        parameterString = parameterString[:-1]
        netlogoString = '"( {0} "'.format(str(factor.getName()))
        for parameterType in factor.getParameterTypes():
            netlogoString = netlogoString + ' + str({0}) '.format(parameterType)
        netlogoString = '{0} + " ) "'.format(netlogoString)
        with open(self._FUNCTIONS_FILE_PATH, "a+") as f:
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
        with open(self._FUNCTIONS_FILE_PATH, "a+") as f:
            f.write ("\nclass {0}:".format(nlType))
            f.write('\n\t__name__ = "{0}"'.format(nlType))
            f.write('\n\tdef __init__(self):')
            f.write('\n\t\tself.__name__ = {0}'.format(nlType))
            f.write('\n\tdef __str__(self):')
            f.write('\n\t\treturn self.__name__')
            f.write('\n\tdef __repr__(self):')
            f.write('\n\t\treturn self.__name__')
            f.flush()
            f.close()
    def getFactors(self):
        return self._factors