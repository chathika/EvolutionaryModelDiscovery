
classNames = ["calc_fraction_of_friends","happy","same_color_group","similar_tolerance","requires_more_friends_than_me","less_tolerant_than_me","getneighbor"]
class calc_fraction_of_friends:
	__name__ = "calc_fraction_of_friends"
	def __init__(self, patch,):
		self.__name__ = "( calc-fraction-of-friends " + str(patch)  + " ) "
	def __str__(self):
		return self.__name__
	def __repr__(self):
		return self.__name__
class happy:
	__name__ = "happy"
	def __init__(self,):
		self.__name__ = "( happy? " + " ) "
	def __str__(self):
		return self.__name__
	def __repr__(self):
		return self.__name__
class same_color_group:
	__name__ = "same_color_group"
	def __init__(self, patch,):
		self.__name__ = "( same-color-group? " + str(patch)  + " ) "
	def __str__(self):
		return self.__name__
	def __repr__(self):
		return self.__name__
class similar_tolerance:
	__name__ = "similar_tolerance"
	def __init__(self, patch,):
		self.__name__ = "( similar-tolerance? " + str(patch)  + " ) "
	def __str__(self):
		return self.__name__
	def __repr__(self):
		return self.__name__
class requires_more_friends_than_me:
	__name__ = "requires_more_friends_than_me"
	def __init__(self, patch,):
		self.__name__ = "( requires-more-friends-than-me? " + str(patch)  + " ) "
	def __str__(self):
		return self.__name__
	def __repr__(self):
		return self.__name__
class less_tolerant_than_me:
	__name__ = "less_tolerant_than_me"
	def __init__(self, patch,):
		self.__name__ = "( less-tolerant-than-me? " + str(patch)  + " ) "
	def __str__(self):
		return self.__name__
	def __repr__(self):
		return self.__name__
class getneighbor:
	__name__ = "getneighbor"
	def __init__(self,):
		self.__name__ = "( getneighbor " + " ) "
	def __str__(self):
		return self.__name__
	def __repr__(self):
		return self.__name__
class patch:
	__name__ = "patch"
	def __init__(self):
		self.__name__ = patch
	def __str__(self):
		return self.__name__
	def __repr__(self):
		return self.__name__
class float:
	__name__ = "float"
	def __init__(self):
		self.__name__ = float
	def __str__(self):
		return self.__name__
	def __repr__(self):
		return self.__name__
class boolean:
	__name__ = "boolean"
	def __init__(self):
		self.__name__ = boolean
	def __str__(self):
		return self.__name__
	def __repr__(self):
		return self.__name__
from deap import gp
pset = gp.PrimitiveSetTyped("main", [], float)
pset.addPrimitive(calc_fraction_of_friends,  [ patch ], float)
pset.addTerminal(happy, float)
pset.addPrimitive(same_color_group,  [ patch ], float)
pset.addPrimitive(similar_tolerance,  [ patch ], boolean)
pset.addPrimitive(requires_more_friends_than_me,  [ patch ], boolean)
pset.addPrimitive(less_tolerant_than_me,  [ patch ], boolean)
pset.addTerminal(getneighbor, patch)
def getDEAPPrimitiveSet():
	return pset