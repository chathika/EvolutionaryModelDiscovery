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
def defaultObjective(results):
    return results.iloc[0].sum()
_objectiveFunction = defaultObjective
class ABMEvaluator:
    _setupCommands = None
    _measurementCommands = None
    _ticksToRun = -1    
    #returns pandas dataframe
    def evaluateABM(self, modelPath):        
        rawMeasures = self._runAndReturnResults(modelPath, self._setupCommands, self._measurementCommands, self._ticksToRun)
        measures = pd.DataFrame(rawMeasures)
        measures = measures.apply(pd.to_numeric, errors='ignore')
        measures.columns = self._measurementCommands
        result = _objectiveFunction(measures)
        return result

    def initialize (self, setupCommands, measurementCommands, ticksToRun):
        self._setupCommands = setupCommands
        self._measurementCommands = measurementCommands
        self._ticksToRun = ticksToRun

    def _runAndReturnResults(self, modelname, setupCommands, metricCommands, ticksToRun):
        with open(modelname, "r") as f:
            workspace = nl4py.newNetLogoHeadlessWorkspace()
            workspace.openModel(modelname)
            #workspace.setParamsRandom()
            for setupCommand in setupCommands:
                workspace.command(setupCommand)
            #workspace.command("setup")
            if ticksToRun < 0:
                ticksToRun = math.pow(2,31)
            #print(metricCommands)
            workspace.scheduleReportersAndRun(metricCommands, 0,1,ticksToRun, "go")
            workspaceResults = workspace.getScheduledReporterResults()
            #print(workspaceResults)
            while len(workspaceResults) == 0:
                workspaceResults = workspace.getScheduledReporterResults()
                time.sleep(2)
            #nl4py.getAllHeadlessWorkspaces().remove(workspace)
            workspace.deleteWorkspace()
            workspace = None
            return workspaceResults

    def setObjectiveFunction(self, objectiveFunction):
        global _objectiveFunction 
        _objectiveFunction = objectiveFunction
###############################

