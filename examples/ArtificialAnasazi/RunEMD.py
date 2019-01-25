from EvolutionaryModelDiscovery import *
modelPath = "Artificial Anasazi Ver 6.nlogo"
setup = ['setup']
measurements = ["L2-error"]
ticks = 500
emd = EvolutionaryModelDiscovery("C:/Program Files/NetLogo 6.0.4", modelPath,setup, measurements, ticks)
emd.setMutationRate(0.1)
emd.setCrossoverRate(0.8)
emd.setGenerations(3)
emd.setDepth(4,8)
emd.setPopulationSize(5)
emd.setIsMinimize(True)
def cindexObjective(results):
    #print(results.iloc[-1][0])
    return (results.iloc[-1][0])
emd.setObjectiveFunction(cindexObjective)
if __name__ == '__main__':
    emd.evolve()