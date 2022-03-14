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

from typing import Dict, List, Callable, Any, Union
import math

import numpy as np
import pandas as pd
import nl4py
from deap import gp


from .Util import *
from .NetLogoWriter import NetLogoWriter


def default_objective(results: pd.DataFrame) -> float:
    '''
    Placeholder objective function. User must provide an objective function
    that translates simulation results to fitness for the genetic program.

    :param results: pd.DataFrame of simulation results as returned by NL4Py.
    :return: simulation results translated into fitness for genetic program.
    '''
    return 0


OBJECTIVE_FUNCTION = default_objective


def set_objective_function(objective_function: Callable) -> None:
    """
    Sets a custom callable as the objective function for the GP. 

    :param objective_function: Callable to be executed by GP. Must return a fitness value.
    """
    global OBJECTIVE_FUNCTION
    OBJECTIVE_FUNCTION = objective_function


def set_model_factors(model_factors: 'EvolutionaryModelDiscovery.ModelFactors') -> None:
    global MODEL_FACTORS
    MODEL_FACTORS = model_factors


def set_model_init_data(model_init_data: Dict[str, Any]) -> None:
    global MODEL_INIT_DATA
    MODEL_INIT_DATA = model_init_data


def set_netlogo_writer(netlogo_writer: NetLogoWriter) -> None:
    global NETLOGO_WRITER
    NETLOGO_WRITER = netlogo_writer


def evaluate(individual: Union['gp.creator.IndividualMin', 'gp.creator.IndividualMax']) -> pd.Series:
    '''
    Genetic program's evaluation function. 

    Simplifies and scores factor/factor-interaction presence.
    Compiles gp tree representation into flattened str format.
    Writes rule to new NetLogo model.
    Simulates new NetLogo model and records fitness.
    Cleans up auto-generated NetLogo model.

    :param individual: Union['gp.creator.IndividualMin', 'gp.creator.IndividualMax'] gp individual
    :return: pd.Series containing presence scores, fitness, and compiled rule of executed gp individual
    '''
    ind_record = score_factor_presence(individual, MODEL_FACTORS)
    newRule = str(gp.compile(
        individual, MODEL_FACTORS.get_DEAP_primitive_set()))
    newModelPath = NETLOGO_WRITER.inject_new_rule(newRule)
    fitness = simulate(newModelPath, MODEL_INIT_DATA["setup_commands"],
                       MODEL_INIT_DATA["measurement_commands"], MODEL_INIT_DATA["ticks_to_run"],
                       MODEL_INIT_DATA["go_command"], MODEL_INIT_DATA['agg_func'])
    remove_model(newModelPath)
    ind_record["Fitness"] = fitness
    ind_record["Rule"] = newRule[:-1]
    ind_record = pd.Series(list(ind_record.values()), index=ind_record.keys())
    return ind_record


def simulate(model_path: str, all_setup_commands: List[Any], measurement_reporters: List[str],
             ticks_to_run: int, go_command: str, agg_func: Callable = np.mean) -> pd.DataFrame:
    """
    Creates a workspace for the NetLogo model and runs it by specified parameters, returning workspace results as pandas dataframe

    :param model_path: str file path to .nlogo model file.
    :param all_setup_commands: list of str NetLogo commands for simulation setup.
    :param measurement_reporters: list of str NetLogo reporters to measure simulation state per tick.
    :param ticks_to_run: int number of ticks to run simulation for.
    :param go_command: str NetLogo command to run simulation.
    :param agg_func: function use to aggregate results of replicates.
    :returns: pd.DataFrame of simulation fitness.
    """

    workspace = nl4py.create_headless_workspace()
    workspace.open_model(model_path)
    assert (type(all_setup_commands[0]) == str or type(all_setup_commands[0]) == list), (
        f'setup_commands must be of type List[str] or List[List[str]]!')
    if type(all_setup_commands[0]) == str:
        all_setup_commands = [all_setup_commands]
    if ticks_to_run < 0:
        # Run "forever" because no stop condition provided.
        ticks_to_run = math.pow(2, 31)
    all_results = []
    for setup_commands_replicate in all_setup_commands:
        for setup_command in setup_commands_replicate:
            workspace.command(setup_command)
        measures = workspace.schedule_reporters(
            measurement_reporters, 0, 1, ticks_to_run, go_command)
        measures = pd.DataFrame(measures, columns=measurement_reporters)
        all_results.append(OBJECTIVE_FUNCTION(measures))
    workspace.deleteWorkspace()
    return agg_func(all_results),


def score_factor_presence(ind: Union['gp.creator.IndividualMin', 'gp.creator.IndividualMax'],
                          ModelFactors: 'EvolutionaryModelDiscovery.ModelFactors') -> Dict[str, int]:
    """
    Scores factor or factor interaction presence as coefficient of simplified rule.

    :param ind: 
    :param ModelFactors: ModelFactors module auto-generated and loaded by EMD.
    :return: Dict[str, int] mapping factor/factor-interaction name to presence score
    """
    factor_interactions = ModelFactors.interactions
    factors = ModelFactors.measureable_factors
    presence_dict = {}
    for factor in factors:
        presence_dict[factor] = 0
    # items on stack represent primitives being processed.
    # items have 3 elements param num considered, primitive(deap.gp.Primitive), and polarity (int)
    stack = [{'param_num': 0, 'obj': ind[0], 'polarity': 1}]
    interaction = None
    interactionRoot = None
    polarity = 1
    for child in range(1, len(ind)):
        childString = ind[child].name
        childArity = ind[child].arity
        # Update presence counts
        # Check negate
        parent = stack[-1]
        if interaction == None:
            if parent['obj'].name in ModelFactors.negativeOps.keys():
                child_position_polarity = ModelFactors.negativeOps[
                    parent['obj'].name][parent['param_num']]
                polarity = parent['polarity'] * child_position_polarity
            if childString in factors:
                # Countable
                print(childString, parent['obj'].name, polarity)
                presence_dict[childString] = presence_dict[childString] + polarity
            # If interaction found start recording
            if childString in factor_interactions:
                interaction = [childString]
                interactionRoot = len(stack)
        elif type(interaction) == list:
            # if interaction still processing, append
            interaction.append(childString)
        # Process next
        # Tell parent a child has been found...
        stack[-1]['param_num'] = stack[-1]['param_num'] + 1
        parent = stack[-1]
        # Resolve children if any
        if childArity == 0:
            # Terminal found.
            # Travel up the stack and pop any completed parents
            while parent['param_num'] == parent['obj'].arity:
                _ = stack.pop()
                if len(stack) == 0:
                    # root reached
                    break
                parent = stack[-1]
                polarity = parent['polarity']
                # Now, if all this parent removal revealed an interaction root, process it
                if len(stack) == interactionRoot:
                    # Interaction is done processing
                    interactionString = str(gp.compile(interaction, MODEL_FACTORS.get_DEAP_primitive_set()))
                    presence_dict[interactionString] = presence_dict.get(
                        interactionString, 0) + polarity
                    interaction = None
                    interactionRoot = None
                    polarity = 1
        else:
            # primitive found. Add to family stack with arity
            stack.append(
                {'param_num': 0, 'obj': ind[child], 'polarity': polarity})
    return presence_dict
