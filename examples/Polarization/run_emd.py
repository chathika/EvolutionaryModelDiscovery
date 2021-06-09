from EvolutionaryModelDiscovery import EvolutionaryModelDiscovery

netlogo_path = 'C:/Program Files/NetLogo 6.2.0'
model_path = "polarization.nlogo"
setup = ['setup']
measurements = ["ticks", "polarization"]
ticks = 1
emd = EvolutionaryModelDiscovery(netlogo_path=netlogo_path, model_path=model_path, setup_commands=setup, measurement_reporters=measurements, ticks_to_run=100)

def averageNumberOfAgents(results):
    return results.iloc[-1].polarization

emd.set_objective_function(averageNumberOfAgents)
emd.set_mutation_rate(0.05)
emd.set_crossover_rate(0.8)
emd.set_generations(10)
emd.set_population_size(16)
emd.set_replications(10)
emd.set_depth(1,20)
emd.set_is_minimize(False)
if __name__ == '__main__':
    emd.evolve()
    fi = emd.get_factor_importances_calculator("FactorScores.csv")
    GI = fi.get_gini_importances(interactions=True)
    PI = fi.get_permutation_accuracy_importances(interactions=True)
    print(GI)
    print(PI)
