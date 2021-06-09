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

from typing import List

from .Util import slugify

class Factor(object):
    """
    Represents an evolutionary model discovery factor. 

    """
    def __init__(self, factor_name: str) -> None:
        """
        Factors have a name, parameters types, and a return type.

        :param factor_name: str name of the Factor.
        """
        if (factor_name == None or factor_name == ""):
            raise Exception("Invalid factor name: {}".format(factor_name))
        self._factor_name = factor_name
        self._parameter_types = []
    
    def __repr__(self) -> str:
        return str(self._factor_name) + " " + str(self._parameter_types) + " " + str(self._return_type)
    
    def add_parameter_type(self, parameter_type : str):
        self._parameter_types.append(slugify(parameter_type))

    def remove_parameter_type(self, parameter_type : str):
        self._parameter_types.remove(parameter_type)
    
    def set_return_type(self, return_type : str):
        self._return_type = slugify(return_type)
    
    def get_return_type(self) -> str:
        return self._return_type

    def get_name(self) -> str:
        return self._factor_name

    def get_parameter_types(self) -> List[str]:
        return self._parameter_types
    
    def get_safe_name(self) -> str:
        return slugify(self._factor_name)
