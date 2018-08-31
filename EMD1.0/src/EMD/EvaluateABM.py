import math 
import time
import nl4py
netlogo_home = "C:/Program Files/NetLogo 6.0.2"
nl4py.startServer(netlogo_home)
def EvaluateABM(modelname, setupCommands ,metricCommands, ticksToRun = -1):
    workspace = nl4py.newNetLogoHeadlessWorkspace()
    workspace.openModel(modelname)
    workspace.setParamsRandom()
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
    nl4py.getAllHeadlessWorkspaces().remove(workspace)
    workspace.deleteWorkspace()
    workspace = None
    return workspaceResults

from deap import gp
from deap import creator
from deap import base
from deap import tools
from NetLogoWriter import NetLogoWriter

def InjectRuleAndEvaluateABM(rule):
    rule = str(rule)
    modelPath='./SimpleSchellingTwoSubgroups_HatnaAdaption.nlogo'
    modelWriter = NetLogoWriter(modelPath)
    modelPath = modelWriter.injectNewRule(rule)
    print(modelPath)
    setup = ['set model-version "sheep-wolves-grass"', 'setup']
    measurementStrings = ["count sheep", "count wolves"]
    result = EvaluateABM(modelPath, setup, measurementStrings, 100)
    #aggregateMetric = abs(( int(float(result[-1][0])) / (float(result[-1][1]) + 0.0000001) ))
    aggregateMetric =  int(float(result[-1][1]))
    return aggregateMetric


###############################

from FactorGenerator import FactorGenerator
fg = FactorGenerator()
fg.generate("util/Functions.nls")

from PrimitiveSetGenerator import PrimitiveSetGenerator
pg = PrimitiveSetGenerator()
pg.generate(fg.getFactors())
from ModelFactors import *
pset.primitives