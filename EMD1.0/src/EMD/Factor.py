import re
class Factor(object):
    _parameterTypes = None
    _returnType = None
    _factorName = None
    _factorFunctionCode = None
    def __repr__(self):
        return str(self._factorName) + " " + str(self._parameterTypes) + " " + str(self._returnType)
    def __init__(self, factorName):
        if (factorName == None or factorName == ""):
            print("Invalid factor name!")
        self._factorName = factorName
        self._parameterTypes = []
    def addParameterType(self, parameterType):
        self._parameterTypes.append(parameterType)
    
    def removeParameterType(self, parameterType):
        self._parameterTypes.remove(parameterType)
    
    def setReturnType(self, returnType):
        self._returnType = returnType

    def getReturnType(self):
        return self._returnType

    def getName(self):
        return self._factorName

    def getParameterTypes(self):
        return self._parameterTypes
    
    def getSafeName(self):
        return self.slugify(self._factorName)

    def slugify(self, value):
        """
        Normalizes string, converts to lowercase, removes non-alpha characters,
        and converts spaces to hyphens."""
        value = str(re.sub('[^\w\s-]', '', value).strip().lower())
        value = str(re.sub('[-\s]+', '_', value))
        return value