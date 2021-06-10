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
from .Util import *

class PrimitiveSetGenerator:    
    
    model_factor_path = ""
    
    def __init__(self):
        self.model_factor_path = get_model_factors_path()
    
    def generate(self, factors, final_return_type):
        with open(self.model_factor_path, "a+") as f:
            f.write('\nclass EMD_model_evaluation:')
            f.write('\n\t__name__ = ""')
            f.write('\n\tdef __init__(self, nl_string):')
            f.write('\n\t\tself.__name__ = "{0}\\n".format(str(nl_string))')
            f.write('\n\tdef __str__(self):')
            f.write('\n\t\treturn self.__name__')
            f.write('\n\tdef __repr__(self):')
            f.write('\n\t\treturn self.__name__')
            f.write('\nfrom deap import gp')            
            f.write('\ndef get_DEAP_primitive_set():')            
            f.write('\n\tpset = gp.PrimitiveSetTyped("main", [], EMD_model_evaluation)')
            for factor in factors:
                parameter_string = " [ "
                for parameter_type in factor.get_parameter_types():
                    parameter_string = parameter_string + "{0},".format(parameter_type)
                parameter_string = '{0} ]'.format(parameter_string[:-1])
                if len(factor.get_parameter_types()) == 0 :
                    f.write('\n\tpset.addTerminal({1}({0}()), {1}, name = "{0}")'.format(factor.get_safe_name(),factor.get_return_type()))
                    f.write('\n\tpset.addPrimitive({0}, [{0}], {0})'.format(factor.get_return_type()))
                else:
                    f.write('\n\tpset.addPrimitive({0}, {1}, {2}, name = "{0}")'.format(factor.get_safe_name(),parameter_string,factor.get_return_type()))
            f.write('\n\tpset.addPrimitive(EMD_model_evaluation, [{0}], EMD_model_evaluation)'.format(final_return_type))
            f.write('\n\treturn pset')
