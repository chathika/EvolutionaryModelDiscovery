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
isInitialized = False
evolved = False
class EvolutionaryModelDiscovery:
    mutationRate_ = 0.2
    crossoverRate_ = 0.8
    generations_ = 10
    objectiveFunction_ = None
    def __init__(self,modelPath, setupCommands, measurementCommands, ticksToRun):
        # Initialize ABM
        self.initialize(modelPath, setupCommands, measurementCommands, ticksToRun)
        # Define hyperparameters
        mutationRate_ = 0.2
        crossoverRate_ = 0.8
        generations_ = 10
    def initialize(self,modelPath, setupCommands, measurementCommands, ticksToRun):
        self.startup(modelPath)
        #if __name__ == '__main__':
            
        global modelPath_
        modelPath_ = modelPath
        global pset
        modelFactorsPath =  getModelFactorsPath()
        with open(modelFactorsPath) as f:
            ModelFactors = importlib.import_module("EvolutionaryModelDiscovery.ModelFactors")
        pset = ModelFactors.getDEAPPrimitiveSet()

        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)
        global toolbox
        toolbox = base.Toolbox()
        # Attribute generator
        toolbox.register("expr_init", gp.genHalfAndHalf, pset=pset, min_=2, max_=4)
        # Structure initializers
        toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr_init)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        global setupCommands_
        global measurementCommands_
        global ticksToRun_
        setupCommands_ = setupCommands
        measurementCommands_ = measurementCommands
        ticksToRun_ = ticksToRun
        #toolbox.register("setupCommands", tools.initRepeat, setupCommands )

        toolbox.register("evaluate", self.evaluate)
        toolbox.register("select", tools.selTournament, tournsize=7)
        toolbox.register("mate", gp.cxOnePoint)
        toolbox.register("expr_mut", gp.genFull, min_=2, max_=5)
        toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)
        toolbox.register("map", futures.map)
        global pop
        pop = toolbox.population(n=10)
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
    def setObjectiveFunction(self, objectiveFunction):
        self.objectiveFunction_ = objectiveFunction
    def evolve(self):
        global isInitialized
        global evolved
        try:
            isScoopMain = scoop.IS_ORIGIN and scoop.IS_RUNNING
        except:
            isScoopMain = True
        if isScoopMain and isInitialized and not evolved:
            print('Evolving!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            evolved = True
            initialized = False
            algorithms.eaSimple(pop, toolbox, self.crossoverRate_, self.mutationRate_, self.generations_, stats, halloffame=hof)
            self.visualize(hof[0])        
            return pop, hof, stats       
        nl4py.stopServer() 
    def startup(self,modelPath):
        global isInitialized
        global evolved
        try:
            isScoopMain = scoop.IS_ORIGIN and scoop.IS_RUNNING
        except:
            isScoopMain = True
        if isScoopMain and not isInitialized:
            print('Starting!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            nl4py.startServer("C:/Program Files/NetLogo 6.0.2")
            netLogoWriter = NetLogoWriter(modelPath)
            #Read in annotations from .nlogo file and generate EMD factors
            factorGenerator = FactorGenerator()
            factorGenerator.generate(netLogoWriter.getFactorsFilePath())
            #Generate the ModelFactors.py file
            primitiveSetGenerator = PrimitiveSetGenerator()
            primitiveSetGenerator.generate(factorGenerator.getFactors(), netLogoWriter.getEMDReturnType())  
            isInitialized = True
            evolved = False
    def evaluate(self,individual):
        newRule = str(gp.compile(individual, pset))
        print(newRule)
        netLogoWriter = NetLogoWriter(modelPath_)
        newModelPath = netLogoWriter.injectNewRule(newRule)
        abmEvaluator = ABMEvaluator()
        abmEvaluator.initialize (setupCommands_, measurementCommands_, ticksToRun_)
        if self.objectiveFunction_ != None:
            abmEvaluator.setObjectiveFunction(self.objectiveFunction_)
        fitness = abmEvaluator.evaluateABM(newModelPath)
        return fitness,

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

    