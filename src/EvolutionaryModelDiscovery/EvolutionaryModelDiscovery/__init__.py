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
from .NetLogoWriter import purge
from .FactorGenerator import FactorGenerator
from .PrimitiveSetGenerator import PrimitiveSetGenerator
from .ABMEvaluator import ABMEvaluator
import math 
import time
import importlib
import nl4py
import numpy
from deap import algorithms
from deap import gp
from deap import creator
from deap import base
from deap import tools
from scoop import futures
import scoop
from multiprocessing import Process, current_process
import matplotlib.pyplot as plt
import networkx as nx
from .Util import *
from os import path
import random
import sys
from inspect import isclass
import pandas as pd
from collections import OrderedDict

isInitialized = False
evolved = False
netLogoWriter = None
ModelFactors = None
MeasureableFactors = None
NegativeOps = None
pop_init_size = 5
class EvolutionaryModelDiscovery:
    mutationRate_ = 0.2
    crossoverRate_ = 0.8
    generations_ = 10
    run_count = 20
    objectiveFunction_ = None
    factorGenerator_ = None
    factorScores = pd.DataFrame()
    def __init__(self,netlogoPath, modelPath, setupCommands, measurementCommands, ticksToRun, goCommand = "go"):
        # Initialize ABM
        self.initialize(netlogoPath, modelPath, setupCommands, measurementCommands, ticksToRun, goCommand)
        # Define hyperparameters
        mutationRate_ = 0.2
        crossoverRate_ = 0.8
        generations_ = 10
    def initialize(self, netlogoPath, modelPath, setupCommands, measurementCommands, ticksToRun, goCommand):
        self.startup(netlogoPath, modelPath)
        #if __name__ == '__main__':
            
        global modelPath_
        modelPath_ = modelPath
        global pset
        modelFactorsPath =  getModelFactorsPath()
        with open(modelFactorsPath) as f:
            global ModelFactors
            ModelFactors = importlib.import_module("EvolutionaryModelDiscovery.ModelFactors")
        pset = ModelFactors.getDEAPPrimitiveSet()
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("IndividualMin", gp.PrimitiveTree, fitness=creator.FitnessMin)
        creator.create("IndividualMax", gp.PrimitiveTree, fitness=creator.FitnessMax)
        global toolbox
        toolbox = base.Toolbox()
        # Attribute generator
        toolbox.register("expr_init", genGrow, pset=pset, min_=2, max_=10)
        # Structure initializers
        toolbox.register("individual", tools.initIterate, creator.IndividualMin, toolbox.expr_init)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        global setupCommands_
        global measurementCommands_
        global ticksToRun_
        global goCommand_
        setupCommands_ = setupCommands
        measurementCommands_ = measurementCommands
        ticksToRun_ = ticksToRun
        goCommand_ = goCommand
        #toolbox.register("setupCommands", tools.initRepeat, setupCommands )

        toolbox.register("evaluate", self.evaluate)
        toolbox.register("select", tools.selTournament, tournsize=7)
        toolbox.register("mate", gp.cxOnePoint)
        toolbox.register("expr_mut", genGrow, min_=2, max_=3)
        toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)
        toolbox.register("map", futures.map)
        global pop
        global pop_init_size
        pop = toolbox.population(n=pop_init_size)
        global hof
        hof = tools.HallOfFame(1)
        global stats
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", numpy.mean)
        stats.register("std", numpy.std)
        stats.register("min", numpy.min)
        stats.register("max", numpy.max)    
    def setMutationRate(self, mutationRate):
        self.mutationRate_ = mutationRate
    def setCrossoverRate(self, crossoverRate):
        self.crossoverRate_ = crossoverRate
    def setGenerations(self, generations):
        self.generations_ = generations
    def setReplications(self, replications):
        self.run_count = replications
    def setPopulationSize(self, populationSize):
        global pop
        global pop_init_size
        pop_init_size = populationSize
        pop = toolbox.population(n=pop_init_size)
    def setObjectiveFunction(self, objectiveFunction):
        self.objectiveFunction_ = objectiveFunction
    def setDepth (self, min__, max__):
        toolbox.register("expr_init", genGrow, pset=pset, min_=min__, max_=max__)
    def setIsMinimize(self, isMinimize ):
        if isMinimize:
            toolbox.register("individual", tools.initIterate, creator.IndividualMin, toolbox.expr_init)
        else:
            toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr_init)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)                
    def evolve(self):
        global isInitialized
        global evolved
        try:
            isScoopMain = scoop.IS_ORIGIN and scoop.IS_RUNNING
        except:
            isScoopMain = True
        pop = None
        if isScoopMain and isInitialized and not evolved:
            print('Evolving...')
            evolved = True
            initialized = False
            global pop_init_size
            for run in range(self.run_count):
                print("Starting run " + str(run))
                pop = toolbox.population(n=pop_init_size)
                population, logbook, factorScores = EMDEA(pop, toolbox, self.crossoverRate_, self.mutationRate_, self.generations_, stats, halloffame=hof, verbose=True)
                #self.visualize(hof[0])
                factorscores_filename = "FactorScores.csv"
                factorScores["Run"] = run
                for priority_col in ["Rule","Gen","Run"]:
                    col = factorScores[priority_col]
                    factorScores.drop(labels=[priority_col], axis=1,inplace = True)
                    factorScores.insert(0, priority_col, col)
                #factorScores = factorScores.set_index("Run")
                #with open(factorscores_filename,"a") as f:
                if path.isfile(factorscores_filename):
                    factorScores.to_csv(factorscores_filename, mode='a', header=False,index=False)
                else:
                    factorScores.to_csv(factorscores_filename,  header=True,index=False)
        print("GP Finished.")
        return pop, hof, stats
        
    def startup(self, netlogoPath, modelPath):
        global isInitialized
        global evolved
        global netLogoWriter
        global MeasureableFactors
        global NegativeOps
        netLogoWriter = NetLogoWriter(modelPath)
        try:
            isScoopMain = scoop.IS_ORIGIN and scoop.IS_RUNNING
        except:
            isScoopMain = True
        if isScoopMain and not isInitialized:
            print('Initializing...')
            nl4py.startServer(netlogoPath)
            purge(".",".*.EMD.nlogo")
            #Read in annotations from .nlogo file and generate EMD factors
            factorGenerator_ = FactorGenerator()
            factorGenerator_.generate(netLogoWriter.getFactorsFilePath())
            #Generate the ModelFactors.py file
            primitiveSetGenerator = PrimitiveSetGenerator()
            primitiveSetGenerator.generate(factorGenerator_.getFactors(), netLogoWriter.getEMDReturnType())  
            isInitialized = True
            evolved = False
    
    def shutdown(self):
        nl4py.stopServer()
        futures.shutdown(False)
        

    def evaluate(self,individual):
        scores = scoreFactors(individual)
        newRule = str(gp.compile(individual, pset))
        newModelPath = netLogoWriter.injectNewRule(newRule)
        abmEvaluator = ABMEvaluator()
        abmEvaluator.initialize (setupCommands_, measurementCommands_, ticksToRun_, goCommand_)
        if self.objectiveFunction_ != None:
            abmEvaluator.setObjectiveFunction(self.objectiveFunction_)
        fitness = abmEvaluator.evaluateABM(newModelPath)
        #print(str(fitness) + " <- " + newRule)
        scores["Fitness"] = fitness
        scores["Rule"] = newRule[:-1]
        scores = pd.Series(list(scores.values()),index=scores.keys())
        return [(fitness,),scores]

    def visualize(self,expr):
        nodes, edges, labels = gp.graph(expr)        
        g = nx.Graph()
        g.add_nodes_from(nodes)
        g.add_edges_from(edges)
        pos = self.custom_tree_layout(g)
        nx.draw_networkx_nodes(g, pos)
        nx.draw_networkx_edges(g, pos)
        nx.draw_networkx_labels(g, pos, labels)
        plt.show()
    def custom_tree_layout(self,g):
        level = 0
        nodes_considered = set()
        nodes_considered.add(0)
        pos = {}
        pos[0] = numpy.array([0,0])
        while len(nodes_considered) != len(g.nodes):
            nodes_in_this_level = set()
            for node in g.nodes:
                for neighbor in g.neighbors(level):
                    if neighbor not in nodes_considered:
                        nodes_in_this_level.add(neighbor)
            nodes_considered = nodes_in_this_level | nodes_considered
            level = level + 1
            for i,node in enumerate(nodes_in_this_level):
                pos[node] = numpy.array([(len(nodes_in_this_level) + i) - len(nodes_in_this_level),-level])
        return pos

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
                    raise IndexError("The gp.generate function tried to add a terminal and a primitive of type '%s', but there is none available." % (type_,)).with_traceback(traceback)
            else:
                try:
                    prim = random.choice(pset.primitives[type_])
                    expr.append(prim)
                    for arg in reversed(prim.args):
                        stack.append((depth + 1, arg))
                except IndexError:
                    _, _, traceback = sys.exc_info()
                    raise IndexError("The gp.generate function tried to add a primitive of type '%s', but there is none available." % (type_,)).with_traceback(traceback)
    return expr

def EMDEA(population, toolbox, cxpb, mutpb, ngen, stats=None,
             halloffame=None, verbose=__debug__):
    """This algorithm reproduce the simplest evolutionary algorithm as
    presented in chapter 7 of [Back2000]_.

    :param population: A list of individuals.
    :param toolbox: A :class:`~deap.base.Toolbox` that contains the evolution
                    operators.
    :param cxpb: The probability of mating two individuals.
    :param mutpb: The probability of mutating an individual.
    :param ngen: The number of generation.
    :param stats: A :class:`~deap.tools.Statistics` object that is updated
                  inplace, optional.
    :param halloffame: A :class:`~deap.tools.HallOfFame` object that will
                       contain the best individuals, optional.
    :param verbose: Whether or not to log the statistics.
    :returns: The final population
    :returns: A class:`~deap.tools.Logbook` with the statistics of the
              evolution

    The algorithm takes in a population and evolves it in place using the
    :meth:`varAnd` method. It returns the optimized population and a
    :class:`~deap.tools.Logbook` with the statistics of the evolution. The
    logbook will contain the generation number, the number of evalutions for
    each generation and the statistics if a :class:`~deap.tools.Statistics` is
    given as argument. The *cxpb* and *mutpb* arguments are passed to the
    :func:`varAnd` function. The pseudocode goes as follow ::

        evaluate(population)
        for g in range(ngen):
            population = select(population, len(population))
            offspring = varAnd(population, toolbox, cxpb, mutpb)
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
    compute the statistics on this population. Finally, when *ngen*
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
    logbook = tools.Logbook()
    logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])
    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in population if not ind.fitness.valid]
    factorScores = pd.DataFrame()
    results = list(toolbox.map(toolbox.evaluate, invalid_ind))
    fitnesses = []
    factorScores = pd.DataFrame()
    for result in results:
        fitnesses.append(result[0])
        fs = result[1]
        fs["Gen"] = 0
        factorScores = factorScores.append(fs,ignore_index=True)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    if halloffame is not None:
        halloffame.update(population)

    record = stats.compile(population) if stats else {}
    logbook.record(gen=0, nevals=len(invalid_ind), **record)
    if verbose:
        print(logbook.stream)

    # Begin the generational process
    for gen in range(1, ngen + 1):
        # Select the next generation individuals
        offspring = toolbox.select(population, len(population))

        # Vary the pool of individuals
        offspring = algorithms.varAnd(offspring, toolbox, cxpb, mutpb)
        for off in offspring:
            del off.fitness.values
        
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        results = list(toolbox.map(toolbox.evaluate, invalid_ind))
        fitnesses = []
        for result in results:
            fitnesses.append(result[0])
            fs = result[1]
            fs["Gen"] = gen
            factorScores = factorScores.append(fs,ignore_index=True)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # Update the hall of fame with the generated individuals
        if halloffame is not None:
            halloffame.update(offspring)

        # Replace the current population by the offspring
        population[:] = offspring

        # Append the current generation statistics to the logbook
        record = stats.compile(population) if stats else {}
        logbook.record(gen=gen, nevals=len(invalid_ind), **record)
        if verbose:
            print(logbook.stream)
        purge(".",".*.EMD.nlogo") 
    return population, logbook, factorScores,


def scoreFactors(ind):
    factor_interactions = ModelFactors.interactions
    factors = ModelFactors.measureableFactors#factorGenerator.getMeasureableFactors()#["compare_quality","compare_dryness","compare_yeild","compare_distance","compare_water_availability","desire_social_presence","homophily_age","homophily_agricultural_productivity","desire_migration","all_potential_farms","potential_farms_near_best_performers","potential_family_farms","potential_neighborhood_farms"]
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