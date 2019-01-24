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
import pkg_resources
def netLogoEMDLineToArray(netlogoEMDLine):
    netlogoEMDLine = netlogoEMDLine.lower()
    if "@emd" in netlogoEMDLine:
        return re.sub("[\s;]","",netlogoEMDLine).split("@")
    else:
        print("Not and EMD annotated line!")

def getModelFactorsPath():
    modelFactorsFilePath = pkg_resources.resource_filename('EvolutionaryModelDiscovery', 'ModelFactors.py')    
    return modelFactorsFilePath

def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens."""
    value = str(re.sub('[^\w\s-]', '', value).strip().lower())
    value = str(re.sub('[-\s]+', '_', value).lower())
    return value