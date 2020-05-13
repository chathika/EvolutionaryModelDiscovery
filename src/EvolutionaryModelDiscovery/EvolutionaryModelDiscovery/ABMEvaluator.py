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
import math 
import time
import nl4py
import operator
from deap import gp
from deap import creator
from deap import base
from deap import tools
import pandas as pd
import numpy as np
def default_objective(results):
    return results.iloc[0].sum()
objective_function = default_objective
class ABMEvaluator:
    
    #returns pandas dataframe
    def evaluate_ABM(self, model_path):        
        raw_measures = self.run_and_return_results(model_path, self.setup_commands, self.measurement_commands, self.ticks_to_run, self.go_command)
        measures = pd.DataFrame(raw_measures)
        measures = measures.apply(pd.to_numeric, errors='ignore')
        measures.columns = self.measurement_commands
        result = objective_function(measures)
        return result

    def initialize (self, setup_commands, measurement_commands, ticks_to_run, go_command = "go"):
        self.setup_commands = setup_commands
        self.measurement_commands = measurement_commands
        self.ticks_to_run = ticks_to_run
        self.go_command = go_command

    def run_and_return_results(self, model_name, setup_commands, metric_commands, ticks_to_run, go_command):
        with open(model_name, "r") as f:
            workspace = nl4py.newNetLogoHeadlessWorkspace()
            workspace.openModel(model_name)
            for setup_command in setup_commands:
                workspace.command(setup_command)
            if ticks_to_run < 0:
                ticks_to_run = math.pow(2,31) # Run "forever" because no stop condition provided.
            workspace.scheduleReportersAndRun(metric_commands, 0,1,ticks_to_run, go_command)
            workspace_results = workspace.awaitScheduledReporterResults()
            workspace.deleteWorkspace()
            workspace = None
            return workspace_results

    def set_objective_function(self, objective_function_):
        global objective_function 
        objective_function = objective_function_
###############################

