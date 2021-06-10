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

from typing import Dict, List, Callable, Any
import math
import nl4py
import pandas as pd
from deap import gp

from .Util import *
from .NetLogoWriter import NetLogoWriter

def default_objective(results : pd.DataFrame) -> float:
    return 0

OBJECTIVE_FUNCTION = default_objective

def set_objective_function(objective_function : Callable):
    """
    Sets a custom callable as the objective function for the GP. 

    :param objective_function: Callable to be executed by GP. Must return a fitness value.
    """
    global OBJECTIVE_FUNCTION 
    OBJECTIVE_FUNCTION = objective_function

def set_model_factors(model_factors : 'EvolutionaryModelDiscovery.ModelFactors'):
    global MODEL_FACTORS
    MODEL_FACTORS = model_factors

def set_model_init_data(model_init_data : Dict[str, Any]):
    global MODEL_INIT_DATA
    MODEL_INIT_DATA = model_init_data

def set_netlogo_writer(netlogo_writer : NetLogoWriter):
    global NETLOGO_WRITER
    NETLOGO_WRITER = netlogo_writer

def evaluate(individual : List[Any]) -> pd.Series:
    scores = score_factors(individual, MODEL_FACTORS)
    newRule = str(gp.compile(individual, MODEL_FACTORS.get_DEAP_primitive_set()))
    newModelPath = NETLOGO_WRITER.inject_new_rule(newRule)
    fitness = simulate(newModelPath, MODEL_INIT_DATA["setup_commands"], 
    MODEL_INIT_DATA["measurement_commands"], MODEL_INIT_DATA["ticks_to_run"], 
    MODEL_INIT_DATA["go_command"])
    remove_model(newModelPath)
    scores["Fitness"] = fitness
    scores["Rule"] = newRule[:-1]
    scores = pd.Series(list(scores.values()),index=scores.keys())
    return scores

def simulate( model_path : str, setup_commands : List[str], measurement_reporters : List[str], 
                                            ticks_to_run : int, go_command : str) -> pd.DataFrame:
    """
    Creates a workspace for the NetLogo model and runs it by specified parameters, returning workspace results as pandas dataframe

    :param model_path: str file path to .nlogo model file.
    :param setup_commands: list of str NetLogo commands for simulation setup.
    :param measurement_reporters: list of str NetLogo reporters to measure simulation state per tick.
    :param ticks_to_run: int number of ticks to run simulation for.
    :param go_command: str NetLogo command to run simulation.
    :returns: List of Lists of measurements sampled per tick of simulation.

    """
    
    workspace = nl4py.create_headless_workspace()
    workspace.open_model(model_path)
    for setup_command in setup_commands:
        workspace.command(setup_command)
    if ticks_to_run < 0:
        ticks_to_run = math.pow(2,31) # Run "forever" because no stop condition provided.
    measures = workspace.schedule_reporters(measurement_reporters, 0,1,ticks_to_run, go_command)
    workspace.deleteWorkspace()
    measures = pd.DataFrame(measures, columns=measurement_reporters)
    result = OBJECTIVE_FUNCTION(measures)
    return result,


def score_factors(ind, ModelFactors):
    """
    Scores factor presence by coefficient of simplified rule.

    :param ModelFactors: ModelFactors module generated and loaded by EMD.
    """
    factor_interactions = ModelFactors.interactions
    factors = ModelFactors.measureable_factors
    presence = {}
    for factor in factors:
        presence[factor] = 0
    stack = [[0, ind[0]]]
    coef = 1
    interaction = None
    interactionRoot = None
    for child in range(1,len(ind)):
        childString = ind[child].name
        childArity = ind[child].arity
        ######Update presence counts
        #Check negate
        parent = stack[-1] 
        if interaction == None:            
            if parent[1].name in ModelFactors.negativeOps.keys():                
                coef = coef * ModelFactors.negativeOps[parent[1].name][parent[0]]
            #Count child        
            if childString in factors :
                #Countable
                presence[childString] = presence[childString] + coef
                coef = 1
            ### If interaction
            if childString in factor_interactions:
                interaction = [childString]
                interactionRoot = len(stack)
        elif type(interaction) == list:
            interaction.append(childString)
        ######Traverse
        #Tell parent a child has been found...
        stack[-1][0] = stack[-1][0] + 1
        parent = stack[-1] 
        #Resolve children if any
        if childArity == 0 :
            #Terminal found. 
            #Travel up the stack and pop any completed parents
            while parent[0] == parent[1].arity:
                root = stack.pop()
                if len(stack) == 0:
                    break
                parent = stack[-1]
                #Now, if all this parent removal revealed an interaction root, process it
                if len(stack) == interactionRoot:
                    #Interaction is done processing 
                    interactionString = str(gp.compile(interaction, pset))
                    presence[interactionString] = presence.get(interactionString,0) + coef
                    interaction = None
                    interactionRoot = None
                    coef = 1
        else:
            #primitive found. Add to family stack with arity
            stack.append( [0, ind[child]])
    return presence

