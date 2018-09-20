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