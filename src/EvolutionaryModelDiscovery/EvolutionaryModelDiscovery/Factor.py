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
from .Util import slugify
class Factor(object):
    
    def __repr__(self):
        return str(self.factor_name) + " " + str(self.parameter_types) + " " + str(self.return_type)
    def __init__(self, factorName):
        if (factorName == None or factorName == ""):
            print("Invalid factor name!")
        self.factor_name = factorName
        self.parameter_types = []
    def add_parameter_type(self, parameterType):
        self.parameter_types.append(slugify(parameterType))
    def remove_parameter_type(self, parameterType):
        self.parameter_types.remove(parameterType)
    
    def set_return_type(self, returnType):
        self.return_type = slugify(returnType)
    def get_return_type(self):
        return self.return_type

    def get_name(self):
        return self.factor_name

    def get_parameter_types(self):
        return self.parameter_types
    
    def get_safe_name(self):
        return slugify(self.factor_name)
