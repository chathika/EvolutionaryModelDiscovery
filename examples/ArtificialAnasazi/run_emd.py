from EvolutionaryModelDiscovery import EvolutionaryModelDiscovery
import argparse

parser = argparse.ArgumentParser(description="Evolutionary Model Discovery Example: Farm Selection of the Artificial Anasazi")
parser.add_argument("NETLOGO_PATH", help="Please provide the path to the top level of your NetLogo installation.")
args = parser.parse_args()

model_path = "./Artificial Anasazi Ver 6.nlogo"
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

emd = EvolutionaryModelDiscovery(netlogo_path=args.NETLOGO_PATH, model_path=model_path, setup_commands=setup, 
                                                                        measurement_reporters=measurements, ticks_to_run=1)
emd.set_mutation_rate(0.1)
emd.set_crossover_rate(0.8)
emd.set_generations(20)
emd.set_depth(4,8)
emd.set_population_size(4)
emd.set_is_minimize(True)

def simulation_error(results):
    return results.iloc[-1][0]

emd.set_objective_function(simulation_error)

if __name__ == '__main__':    
    emd.evolve()
    fi = emd.get_factor_importances_calculator("FactorScores.csv")
    GI = fi.get_gini_importances(interactions=True)
    PI = fi.get_permutation_accuracy_importances(interactions=True)
    print(GI)
    print(PI)