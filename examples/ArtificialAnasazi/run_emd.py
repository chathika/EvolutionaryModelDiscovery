from EvolutionaryModelDiscovery import *
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 
import argparse
import sys
from scoop import futures

parser = argparse.ArgumentParser(description="Evolutionary Model Discovery Example: Farm Selection of the Artificial Anasazi")
parser.add_argument("NETLOGO_PATH", help="Please provide the path to the top level of your NetLogo installation.")
args = parser.parse_args()

modelPath = "./Artificial Anasazi Ver 6.nlogo"
var = 0.05
setup = ["set harvest-adjustment (0.64 + ((" + str(2*var) + " * 0.64) * random-float 1 - (" + str(var) + " * 0.64)) )",
"set harvest-variance (0.44 + ((" + str(2*var) + " * 0.44) * random-float 1 - (" + str(var) + " * 0.44)) )",
"set base-nutrition-need (185 + ((" + str(2*var) + " * 185) * random-float 1 - (" + str(var) + " * 185)) )",
"set min-death-age (40  + ((" + str(2*var) + " * 40) * random-float 1 - (" + str(var) + " * 40)) )",
"set death-age-span (10 + ((" + str(2*var) + " * 10) * random-float 1 - (" + str(var) + " * 10)) )",
"set min-fertility-ends-age (29 + ((" + str(2*var) + " * 29) * random-float 1 - (" + str(var) + " * 29)) )",
"set fertility-ends-age-span (5 +  ((" + str(2*var) + " * 5) * random-float 1 - (" + str(var) + " * 5)) )",
"set min-fertility (0.17 + ((" + str(2*var) + " * 0.17) * random-float 1 - (" + str(var) + "  * 0.17)) )",
"set fertility-span (0.03 + ((" + str(2*var) + " * 0.03) * random-float 1 - (" + str(var) + "  * 0.03)) )",
"set maize-gift-to-child (0.47 + ((" + str(2*var) + " * 0.47) * random-float 1 - (" + str(var) + "  * 0.47)) )",
"set water-source-distance (11.5  + ((" + str(2*var) + " * 11.5) * random-float 1 - (" + str(var) + "  * 11.5)) )",
'setup']
measurements = ["L2-error"]
ticks = 550
emd = EvolutionaryModelDiscovery(args.NETLOGO_PATH, modelPath,setup, measurements, ticks)
emd.setMutationRate(0.1)
emd.setCrossoverRate(0.8)
emd.setGenerations(20)
emd.setReplications(1)
emd.setDepth(4,8)
emd.setPopulationSize(4)
emd.setIsMinimize(True)
def cindexObjective(results):
    #print(results.iloc[-1][0])
    return (results.iloc[-1][0])

emd.setObjectiveFunction(cindexObjective)

if __name__ == '__main__':    
    print(emd.evolve()) #Results are written to FactorScores.csv
    emd.shutdown()