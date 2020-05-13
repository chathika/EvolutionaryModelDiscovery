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
from .NetLogoWriter import NetLogoWriter
from .FactorGenerator import FactorGenerator
from .PrimitiveSetGenerator import PrimitiveSetGenerator
from .FactorImportances import FactorImportances
from .SimpleDEAPGP import *
from .Util import *

from os import path
import nl4py
import pandas as pd
from deap import algorithms, gp, creator, base, tools

class EvolutionaryModelDiscovery:
    
    def __init__(self,netlogo_path, model_path, setup_commands, 
                    measurement_commands, ticks_to_run, go_command = "go"):
        # Initialize ABM
        self.model_init_data = {
            "model_path" : model_path,
            "setup_commands" : setup_commands,
            "measurement_commands" : measurement_commands,
            "ticks_to_run" : ticks_to_run,
            "go_command" : go_command
        }
        self.parse_model_into_factors(netlogo_path)
        self.gp = SimpleDEAPGP(self.netLogoWriter, self.model_init_data)
        self.factor_scores_file_name = os.path.join("FactorScores.csv")
    
    def set_mutation_rate(self, mutation_rate):
        self.gp.set_mutation_rate(mutation_rate)
    def set_crossover_rate(self, crossover_rate):
        self.gp.set_crossover_rate(crossover_rate)
    def set_generations(self, generations):
        self.gp.set_generations(generations)
    def set_replications(self, replications):
        self.replications = replications
    def set_population_size(self, population_size):
        self.gp.set_population_size(population_size)
    def set_objective_function(self, objective_function):
        self.gp.set_objective_function(objective_function)
    def set_depth(self, min, max):
        self.gp.set_depth(min,max)
    def set_factor_scores_file_name (self, name):
        self.factor_scores_file_name = os.path.join(name)
    def set_is_minimize(self, is_minimize ):
        self.gp.set_is_minimize(is_minimize)
        
    def parse_model_into_factors(self, netlogoPath):
        '''
        Parses NetLogo model and EMD annotations into Python classes 
        for syntax tree representation
        '''
        self.isInitialized = False
        self.netLogoWriter = NetLogoWriter(self.model_init_data["model_path"])
        if not self.isInitialized:
            #  Evolutionary Model Discovery Initializing
            # Starting NL4Py
            nl4py.startServer(netlogoPath)
            #Remove temporary model files
            purge(".",".*.EMD.nlogo")
            #Reset Factors files
            remove_model_factors_file()
            create_model_factors_file()
            # Parsing NetLogo model into syntax tree primitives and Python classes
            # by reading in annotations from .nlogo file and generate EMD factors
            self.factorGenerator = FactorGenerator()
            self.factorGenerator.generate(self.netLogoWriter.get_factors_file_path())
            # Generate the ModelFactors.py file, Loading parsed primitives as Python classes
            self.primitiveSetGenerator = PrimitiveSetGenerator()
            self.primitiveSetGenerator.generate(self.factorGenerator.get_factors(),
                    self.netLogoWriter.get_EMD_return_type())
    
    def evolve(self, num_procs = -1):
        '''
        Conduct evolution using initialized genetic program
        '''
        # Begining evolution
        self.evolved = True
        self.initialized = False
        for run in range(self.replications):
            print("--- Starting GP Run {} ---".format(run))                
            self.population, self.logbook, self.factor_scores = self.gp.evolve(num_procs=num_procs)
            #self.visualize(hof[0])
            self.factor_scores["Run"] = run
            for priority_col in ["Rule","Gen","Run"]:
                col = self.factor_scores[priority_col]
                self.factor_scores.drop(labels=[priority_col], axis=1,inplace = True)
                self.factor_scores.insert(0, priority_col, col)
            if path.isfile(self.factor_scores_file_name):
                old_factor_scores = pd.read_csv(self.factor_scores_file_name)
                old_factor_scores.append(self.factor_scores,ignore_index=True, 
                            sort=False).to_csv(self.factor_scores_file_name,index=False)
            else:
                self.factor_scores.to_csv(self.factor_scores_file_name,  header=True,index=False)
        print("--- Genetic program runs finished, output written to {} ---".format(self.factor_scores_file_name))
        return self.factor_scores
        
    def get_factor_importances_calculator(self, factor_scores=None):
        try:
            if factor_scores is None:
                return FactorImportances(self.factor_scores)
            else:
                return FactorImportances(factor_scores)
        except AttributeError:
            raise Exception("Either factor scores do not exist or GP not run. Do EvolutionaryModelDiscovery.evolve() first.")
        
    def shutdown(self):
        nl4py.stopServer()
        remove_model_factors_file()     


    @deprecated("Replaced with PEP 8 compliant variant {}".format("set_mutation_rate"))
    def setMutationRate(self, mutationRate):
        self.set_mutation_rate(mutationRate)
    @deprecated("Replaced with PEP 8 compliant variant {}".format("set_crossover_rate"))
    def setCrossoverRate(self, crossoverRate):
        self.set_crossover_rate(crossoverRate)
    @deprecated("Replaced with PEP 8 compliant variant {}".format("set_generations"))
    def setGenerations(self, generations):
        self.set_generations(generations)
    @deprecated("Replaced with PEP 8 compliant variant {}".format("set_replications"))
    def setReplications(self, replications):
        self.set_replications(replications)
    @deprecated("Replaced with PEP 8 compliant variant {}".format("set_population_size"))
    def setPopulationSize(self, populationSize):
        self.set_population_size(populationSize)
    @deprecated("Replaced with PEP 8 compliant variant {}".format("set_objective_function"))
    def setObjectiveFunction(self, objectiveFunction):
        self.set_objective_function(objectiveFunction)
    @deprecated("Replaced with PEP 8 compliant variant {}".format("set_depth"))
    def setDepth(self, min, max):
        self.set_depth(min,max)
    @deprecated("Replaced with PEP 8 compliant variant {}".format("set_factor_scores_file_name"))
    def setFactorScoresFileName (self, name):
        self.set_factor_scores_file_name(name)
    @deprecated("Replaced with PEP 8 compliant variant {}".format("set_is_minimize"))
    def setIsMinimize(self, isMinimize ):
        self.set_is_minimize(isMinimize)



    