
classNames = ["combine","subtract","divide","multiply","get_max_one_of","get_min_one_of","compare_quality","compare_dryness","compare_yeild","compare_distance","compare_water_availability","desire_social_presence","homophily_age","homophily_agricultural_productivity","desire_migration","all_potential_farms","potential_farms_near_best_performers","potential_family_farms","potential_neighborhood_farms"]
negativeOps = {}
measureableFactors = ['combine', 'subtract', 'divide', 'multiply', 'get_max_one_of', 'get_min_one_of', 'compare_quality', 'compare_dryness', 'compare_yeild', 'compare_distance', 'compare_water_availability', 'desire_social_presence', 'homophily_age', 'homophily_agricultural_productivity', 'desire_migration', 'all_potential_farms', 'potential_farms_near_best_performers', 'potential_family_farms', 'potential_neighborhood_farms']
interactions = []
class combine:
	__name__ = "combine"
	def __init__(self, emdcomparator0, emdcomparator1):
		self.__name__ = "( combine (" + str(emdcomparator0) + ") (" + str(emdcomparator1) + ") " + " ) "
	def __str__(self):
		return self.__name__
	def __repr__(self):
		return self.__name__
class subtract:
	__name__ = "subtract"
	def __init__(self, emdcomparator0, emdcomparator1):
		self.__name__ = "( subtract (" + str(emdcomparator0) + ") (" + str(emdcomparator1) + ") " + " ) "
	def __str__(self):
		return self.__name__
	def __repr__(self):
		return self.__name__
class divide:
	__name__ = "divide"
	def __init__(self, emdcomparator0, emdcomparator1):
		self.__name__ = "( divide (" + str(emdcomparator0) + ") (" + str(emdcomparator1) + ") " + " ) "
	def __str__(self):
		return self.__name__
	def __repr__(self):
		return self.__name__
class multiply:
	__name__ = "multiply"
	def __init__(self, emdcomparator0, emdcomparator1):
		self.__name__ = "( multiply (" + str(emdcomparator0) + ") (" + str(emdcomparator1) + ") " + " ) "
	def __str__(self):
		return self.__name__
	def __repr__(self):
		return self.__name__
class get_max_one_of:
	__name__ = "get_max_one_of"
	def __init__(self, emdfarmplots0, emdcomparator1):
		self.__name__ = "( get-max-one-of (" + str(emdfarmplots0) + ") (" + str(emdcomparator1) + ") " + " ) "
	def __str__(self):
		return self.__name__
	def __repr__(self):
		return self.__name__
class get_min_one_of:
	__name__ = "get_min_one_of"
	def __init__(self, emdfarmplots0, emdcomparator1):
		self.__name__ = "( get-min-one-of (" + str(emdfarmplots0) + ") (" + str(emdcomparator1) + ") " + " ) "
	def __str__(self):
		return self.__name__
	def __repr__(self):
		return self.__name__
class compare_quality:
	__name__ = "compare_quality"
	def __init__(self,):
		self.__name__ = "( compare-quality " + " ) "
	def __str__(self):
		return self.__name__
	def __repr__(self):
		return self.__name__
class compare_dryness:
	__name__ = "compare_dryness"
	def __init__(self,):
		self.__name__ = "( compare-dryness " + " ) "
	def __str__(self):
		return self.__name__
	def __repr__(self):
		return self.__name__
class compare_yeild:
	__name__ = "compare_yeild"
	def __init__(self,):
		self.__name__ = "( compare-yeild " + " ) "
	def __str__(self):
		return self.__name__
	def __repr__(self):
		return self.__name__
class compare_distance:
	__name__ = "compare_distance"
	def __init__(self,):
		self.__name__ = "( compare-distance " + " ) "
	def __str__(self):
		return self.__name__
	def __repr__(self):
		return self.__name__
class compare_water_availability:
	__name__ = "compare_water_availability"
	def __init__(self,):
		self.__name__ = "( compare-water-availability " + " ) "
	def __str__(self):
		return self.__name__
	def __repr__(self):
		return self.__name__
class desire_social_presence:
	__name__ = "desire_social_presence"
	def __init__(self,):
		self.__name__ = "( desire-social-presence " + " ) "
	def __str__(self):
		return self.__name__
	def __repr__(self):
		return self.__name__
class homophily_age:
	__name__ = "homophily_age"
	def __init__(self,):
		self.__name__ = "( homophily-age " + " ) "
	def __str__(self):
		return self.__name__
	def __repr__(self):
		return self.__name__
class homophily_agricultural_productivity:
	__name__ = "homophily_agricultural_productivity"
	def __init__(self,):
		self.__name__ = "( homophily-agricultural-productivity " + " ) "
	def __str__(self):
		return self.__name__
	def __repr__(self):
		return self.__name__
class desire_migration:
	__name__ = "desire_migration"
	def __init__(self,):
		self.__name__ = "( desire-migration " + " ) "
	def __str__(self):
		return self.__name__
	def __repr__(self):
		return self.__name__
class all_potential_farms:
	__name__ = "all_potential_farms"
	def __init__(self,):
		self.__name__ = "( all-potential-farms " + " ) "
	def __str__(self):
		return self.__name__
	def __repr__(self):
		return self.__name__
class potential_farms_near_best_performers:
	__name__ = "potential_farms_near_best_performers"
	def __init__(self,):
		self.__name__ = "( potential-farms-near-best-performers " + " ) "
	def __str__(self):
		return self.__name__
	def __repr__(self):
		return self.__name__
class potential_family_farms:
	__name__ = "potential_family_farms"
	def __init__(self,):
		self.__name__ = "( potential-family-farms " + " ) "
	def __str__(self):
		return self.__name__
	def __repr__(self):
		return self.__name__
class potential_neighborhood_farms:
	__name__ = "potential_neighborhood_farms"
	def __init__(self,):
		self.__name__ = "( potential-neighborhood-farms " + " ) "
	def __str__(self):
		return self.__name__
	def __repr__(self):
		return self.__name__
class emdfarmplot:
	__name__ = "emdfarmplot"
	def __init__(self, nlString):
		self.__name__ = str(nlString)
	def __str__(self):
		return self.__name__
	def __repr__(self):
		return self.__name__
class emdcomparator:
	__name__ = "emdcomparator"
	def __init__(self, nlString):
		self.__name__ = str(nlString)
	def __str__(self):
		return self.__name__
	def __repr__(self):
		return self.__name__
class emdfarmplots:
	__name__ = "emdfarmplots"
	def __init__(self, nlString):
		self.__name__ = str(nlString)
	def __str__(self):
		return self.__name__
	def __repr__(self):
		return self.__name__
class EMD_ModelEvaluation:
	__name__ = ""
	def __init__(self, nlString):
		self.__name__ = "{0}\n".format(str(nlString))
	def __str__(self):
		return self.__name__
	def __repr__(self):
		return self.__name__
from deap import gp
def getDEAPPrimitiveSet():
	pset = gp.PrimitiveSetTyped("main", [], EMD_ModelEvaluation)
	pset.addPrimitive(combine,  [ emdcomparator,emdcomparator ], emdcomparator, name = "combine")
	pset.addPrimitive(subtract,  [ emdcomparator,emdcomparator ], emdcomparator, name = "subtract")
	pset.addPrimitive(divide,  [ emdcomparator,emdcomparator ], emdcomparator, name = "divide")
	pset.addPrimitive(multiply,  [ emdcomparator,emdcomparator ], emdcomparator, name = "multiply")
	pset.addPrimitive(get_max_one_of,  [ emdfarmplots,emdcomparator ], emdfarmplot, name = "get_max_one_of")
	pset.addPrimitive(get_min_one_of,  [ emdfarmplots,emdcomparator ], emdfarmplot, name = "get_min_one_of")
	pset.addTerminal(emdcomparator(compare_quality()), emdcomparator, name = "compare_quality")
	pset.addPrimitive(emdcomparator, [emdcomparator], emdcomparator)
	pset.addTerminal(emdcomparator(compare_dryness()), emdcomparator, name = "compare_dryness")
	pset.addPrimitive(emdcomparator, [emdcomparator], emdcomparator)
	pset.addTerminal(emdcomparator(compare_yeild()), emdcomparator, name = "compare_yeild")
	pset.addPrimitive(emdcomparator, [emdcomparator], emdcomparator)
	pset.addTerminal(emdcomparator(compare_distance()), emdcomparator, name = "compare_distance")
	pset.addPrimitive(emdcomparator, [emdcomparator], emdcomparator)
	pset.addTerminal(emdcomparator(compare_water_availability()), emdcomparator, name = "compare_water_availability")
	pset.addPrimitive(emdcomparator, [emdcomparator], emdcomparator)
	pset.addTerminal(emdcomparator(desire_social_presence()), emdcomparator, name = "desire_social_presence")
	pset.addPrimitive(emdcomparator, [emdcomparator], emdcomparator)
	pset.addTerminal(emdcomparator(homophily_age()), emdcomparator, name = "homophily_age")
	pset.addPrimitive(emdcomparator, [emdcomparator], emdcomparator)
	pset.addTerminal(emdcomparator(homophily_agricultural_productivity()), emdcomparator, name = "homophily_agricultural_productivity")
	pset.addPrimitive(emdcomparator, [emdcomparator], emdcomparator)
	pset.addTerminal(emdcomparator(desire_migration()), emdcomparator, name = "desire_migration")
	pset.addPrimitive(emdcomparator, [emdcomparator], emdcomparator)
	pset.addTerminal(emdfarmplots(all_potential_farms()), emdfarmplots, name = "all_potential_farms")
	pset.addPrimitive(emdfarmplots, [emdfarmplots], emdfarmplots)
	pset.addTerminal(emdfarmplots(potential_farms_near_best_performers()), emdfarmplots, name = "potential_farms_near_best_performers")
	pset.addPrimitive(emdfarmplots, [emdfarmplots], emdfarmplots)
	pset.addTerminal(emdfarmplots(potential_family_farms()), emdfarmplots, name = "potential_family_farms")
	pset.addPrimitive(emdfarmplots, [emdfarmplots], emdfarmplots)
	pset.addTerminal(emdfarmplots(potential_neighborhood_farms()), emdfarmplots, name = "potential_neighborhood_farms")
	pset.addPrimitive(emdfarmplots, [emdfarmplots], emdfarmplots)
	pset.addPrimitive(EMD_ModelEvaluation, [emdfarmplot], EMD_ModelEvaluation)
	return pset