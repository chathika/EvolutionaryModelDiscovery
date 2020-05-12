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

import multiprocessing
import random
from inspect import isclass
from deap import algorithms, gp, creator, base, tools
import pandas as pd
import numpy as np
from .Util import *
from .ABMEvaluator import ABMEvaluator
import importlib

class SimpleDEAPGP:

    def __init__(self, netlogo_writer, model_init_data):
        self.model_init_data = model_init_data
        self.mutation_rate = 0.2
        self.crossover_rate = 0.8
        self.generations = 10
        self.run_count = 20
        self.pop_init_size = 5
        global ModelFactors
        with open(get_model_factors_path()) as f:
            ModelFactors = importlib.import_module("EvolutionaryModelDiscovery.ModelFactors")
        self.pset = ModelFactors.get_DEAP_primitive_set()
        self.setup_DEAP_GP()
        self.netlogo_writer = netlogo_writer
    
    def setup_DEAP_GP(self):
        '''
        Sets up a DEAP GP
        '''
        print('-- Setting up genetic program')
        # Setup DEAP GP
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("IndividualMin", gp.PrimitiveTree, fitness=creator.FitnessMin)
        creator.create("IndividualMax", gp.PrimitiveTree, fitness=creator.FitnessMax)
        self.toolbox = base.Toolbox()
        # Attribute generator
        self.toolbox.register("expr_init", genGrow, pset=self.pset, min_=2, max_=10)
        # Structure initializers
        self.toolbox.register("individual", tools.initIterate, creator.IndividualMin, self.toolbox.expr_init)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        #self.toolbox.register("setupCommands", tools.initRepeat, setupCommands )
        self.toolbox.register("evaluate", self.evaluate)
        self.toolbox.register("select", tools.selTournament, tournsize=7)
        self.toolbox.register("mate", gp.cxOnePoint)
        self.toolbox.register("expr_mut", genGrow, min_=2, max_=3)
        self.toolbox.register("mutate", gp.mutUniform, expr=self.toolbox.expr_mut, pset=self.pset)
        self.hof = tools.HallOfFame(1)
        #global self.stats
        self.stats = tools.Statistics(get_values)#
        self.stats.register("avg", np.mean)
        self.stats.register("std", np.std)
        self.stats.register("min", np.min)
        self.stats.register("max", np.max)
        self.isInitialized = True
        self.evolved = False
        print('-- Genetic program setup successfully')  
    
    
    def set_mutation_rate(self, mutation_rate):
            self.mutation_rate = mutation_rate
    def set_crossover_rate(self, crossover_rate):
        self.crossover_rate = crossover_rate
    def set_generations(self, generations):
        self.generations = generations
    def set_population_size(self, population_size):
        self.pop_init_size = population_size
    def set_objective_function(self, objective_function):
        self.objective_function = objective_function
    def set_depth (self, min, max):
        self.toolbox.register("expr_init", genGrow, pset=self.pset, min_=min, max_=max)
    def set_is_minimize(self, is_minimize ):
        if is_minimize:
            self.toolbox.register("individual", tools.initIterate, 
                                    creator.IndividualMin, self.toolbox.expr_init)
        else:
            self.toolbox.register("individual", tools.initIterate, 
                                        creator.Individual, self.toolbox.expr_init)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)                
            
    def evolve(self, verbose=__debug__, num_procs=multiprocessing.cpu_count()):
        '''
        Chathika: made logging, stat collection, and multiprocessing related
        changes to this functions
        '''
        """This algorithm reproduce the simplest evolutionary algorithm as
        presented in chapter 7 of [Back2000]_.

        :param verbose: Whether or not to log the statistics.
        :param num_procs: number of processes.
        :returns: The final population
        :returns: A class:`~deap.tools.Logbook` with the statistics of the
                evolution
        :returns: The factor scores in a pandas dataframe. 

        The algorithm takes in a population and evolves it in place using the
        :meth:`varAnd` method. It returns the optimized population and a
        :class:`~deap.tools.Logbook` with the statistics of the evolution. The
        logbook will contain the generation number, the number of evalutions for
        each generation and the statistics if a :class:`~deap.tools.Statistics` is
        given as argument. The *crossover_rate* and *mutation_rate* arguments are passed to the
        :func:`varAnd` function. The pseudocode goes as follow ::

            evaluate(population)
            for g in range(self.generations):
                population = select(population, len(population))
                offspring = varAnd(population, toolbox, crossover_rate, mutation_rate)
                evaluate(offspring)
                population = offspring

        As stated in the pseudocode above, the algorithm goes as follow. First, it
        evaluates the individuals with an invalid fitness. Second, it enters the
        generational loop where the selection procedure is applied to entirely
        replace the parental population. The 1:1 replacement ratio of this
        algorithm **requires** the selection procedure to be stochastic and to
        select multiple times the same individual, for example,
        :func:`~deap.tools.selTournament` and :func:`~deap.tools.selRoulette`.
        Third, it applies the :func:`varAnd` function to produce the next
        generation population. Fourth, it evaluates the new individuals and
        compute the statistics on this population. Finally, when *self.generations*
        generations are done, the algorithm returns a tuple with the final
        population and a :class:`~deap.tools.Logbook` of the evolution.

        .. note::

            Using a non-stochastic selection method will result in no selection as
            the operator selects *n* individuals from a pool of *n*.

        This function expects the :meth:`toolbox.mate`, :meth:`toolbox.mutate`,
        :meth:`toolbox.select` and :meth:`toolbox.evaluate` aliases to be
        registered in the toolbox.

        .. [Back2000] Back, Fogel and Michalewicz, "Evolutionary Computation 1 :
        Basic Algorithms and Operators", 2000.
        """
        population = self.toolbox.population(n=self.pop_init_size)
        logbook = tools.Logbook()
        logbook.header = ['gen', 'nevals'] + (self.stats.fields if self.stats else [])
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in population if not ind.fitness.valid]
        factorScores = pd.DataFrame()
        num_procs = multiprocessing.cpu_count() if num_procs < 1 else num_procs
        with multiprocessing.Pool(num_procs) as pool:
            results = list(pool.map(self.toolbox.evaluate, invalid_ind))
            fitnesses = []
            factorScores = pd.DataFrame()
            for result in results:
                fitnesses.append(result[0])
                fs = result[1]
                fs["Gen"] = 0
                factorScores = factorScores.append(fs,ignore_index=True, sort=False)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit

            if self.hof is not None:
                self.hof.update(population)

            record = self.stats.compile(population) if self.stats else {}
            logbook.record(gen=0, nevals=len(invalid_ind), **record)
            if verbose:
                print(logbook.stream)

            # Begin the generational process
            for gen in range(1, self.generations + 1):
                # Select the next generation individuals
                offspring = self.toolbox.select(population, len(population))

                # Vary the pool of individuals
                offspring = algorithms.varAnd(offspring, self.toolbox, self.crossover_rate, self.mutation_rate)
                for off in offspring:
                    del off.fitness.values
                
                # Evaluate the individuals with an invalid fitness
                invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
                results = list(pool.map(self.toolbox.evaluate, invalid_ind))
                fitnesses = []
                for result in results:
                    fitnesses.append(result[0])
                    fs = result[1]
                    fs["Gen"] = gen
                    factorScores = factorScores.append(fs,ignore_index=True, sort=False)
                for ind, fit in zip(invalid_ind, fitnesses):
                    ind.fitness.values = fit

                # Update the hall of fame with the generated individuals
                if self.hof is not None:
                    self.hof.update(offspring)

                # Replace the current population by the offspring
                population[:] = offspring

                # Append the current generation statistics to the logbook
                record = self.stats.compile(population) if self.stats else {}
                logbook.record(gen=gen, nevals=len(invalid_ind), **record)
                if verbose:
                    print(logbook.stream)
                purge(".",".*.EMD.nlogo") 
        return population, logbook, factorScores,

    def evaluate(self,individual):
        global ModelFactors
        scores = score_factors(individual, ModelFactors)
        newRule = str(gp.compile(individual, self.pset))
        newModelPath = self.netlogo_writer.inject_new_rule(newRule)
        abmEvaluator = ABMEvaluator()
        abmEvaluator.initialize (self.model_init_data["setup_commands"], self.model_init_data["measurement_commands"], 
                    self.model_init_data["ticks_to_run"], self.model_init_data["go_command"])
        if self.objective_function != None:
            abmEvaluator.set_objective_function(self.objective_function)
        fitness = abmEvaluator.evaluate_ABM(newModelPath)
        #print(str(fitness) + " <- " + newRule)
        scores["Fitness"] = fitness
        scores["Rule"] = newRule[:-1]
        scores = pd.Series(list(scores.values()),index=scores.keys())
        return [(fitness,),scores]



def genGrow(pset, min_, max_, type_=None):
    """Generate an expression where each leaf might have a different depth
    between *min* and *max*.

    :param pset: Primitive set from which primitives are selected.
    :param min_: Minimum height of the produced trees.
    :param max_: Maximum Height of the produced trees.
    :param type_: The type that should return the tree when called, when
                  :obj:`None` (default) the type of :pset: (pset.ret)
                  is assumed.
    :returns: A grown tree with leaves at possibly different depths.
    """
    def condition(height, depth):
        """Expression generation stops when the depth is equal to height
        or when it is randomly determined that a a node should be a terminal.
        """
        return depth >= height or \
            (depth >= min_ and random.random() < pset.terminalRatio)
    return generate(pset, min_, max_, condition, type_)

def generate(pset, min_, max_, condition, type_=None):
    """Generate a Tree as a list of list. The tree is build
    from the root to the leaves, and it stop growing when the
    condition is fulfilled.

    :param pset: Primitive set from which primitives are selected.
    :param min_: Minimum height of the produced trees.
    :param max_: Maximum Height of the produced trees.
    :param condition: The condition is a function that takes two arguments,
                    the height of the tree to build and the current
                    depth in the tree.
    :param type_: The type that should return the tree when called, when
                :obj:`None` (default) the type of :pset: (pset.ret)
                is assumed.
    :returns: A grown tree with leaves at possibly different depths
            dependending on the condition function.
    """
    validTree = False
    while (not validTree):
        if type_ is None:
            type_ = pset.ret
        expr = []
        height = random.randint(min_, max_)
        stack = [(0, type_)]    
        validTree = True
        while len(stack) != 0:
            depth, type_ = stack.pop()        
            if condition(height, depth):
                try:
                    if  len(pset.terminals[type_]) > 0:
                        term = random.choice(pset.terminals[type_])
                        if isclass(term):
                            term = term()
                        expr.append(term)
                    else:
                        #No terminal for this type available. Invalid tree... try again.
                        validTree = False
                        break 
                except IndexError:
                    raise IndexError("The gp.generate function tried to add a terminal \
                            and a primitive of type '%s', but there is none available." 
                            % (type_,)).with_traceback(traceback)
            else:
                try:
                    prim = random.choice(pset.primitives[type_])
                    expr.append(prim)
                    for arg in reversed(prim.args):
                        stack.append((depth + 1, arg))
                except IndexError:
                    _, _, traceback = sys.exc_info()
                    raise IndexError("The gp.generate function tried to add a primitive \
                            of type '%s', but there is none available." 
                            % (type_,)).with_traceback(traceback)
    return expr


def score_factors(ind, ModelFactors):
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


def get_values(ind):
    '''
    Returns fitness values of a GP individual. Used by stats object
    '''
    return ind.fitness.values
    