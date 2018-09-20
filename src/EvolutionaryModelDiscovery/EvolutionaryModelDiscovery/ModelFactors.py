
classNames = ["calc_fraction_of_friends","happy","same_color_group","similar_tolerance","requires_more_friends_than_me","less_tolerant_than_me","getneighbor","gethomepatch"]
class calc_fraction_of_friends:
	__name__ = "calc_fraction_of_friends"
	def __init__(self, EMDpatch):
		self.__name__ = "( calc-fraction-of-friends " + str(EMDpatch)  + " ) "
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
	def __init__(self, EMDpatch):
		self.__name__ = "( same-color-group? " + str(EMDpatch)  + " ) "
	def __str__(self):
		return self.__name__
	def __repr__(self):
		return self.__name__
class similar_tolerance:
	__name__ = "similar_tolerance"
	def __init__(self, EMDpatch):
		self.__name__ = "( similar-tolerance? " + str(EMDpatch)  + " ) "
	def __str__(self):
		return self.__name__
	def __repr__(self):
		return self.__name__
class requires_more_friends_than_me:
	__name__ = "requires_more_friends_than_me"
	def __init__(self, EMDpatch):
		self.__name__ = "( requires-more-friends-than-me? " + str(EMDpatch)  + " ) "
	def __str__(self):
		return self.__name__
	def __repr__(self):
		return self.__name__
class less_tolerant_than_me:
	__name__ = "less_tolerant_than_me"
	def __init__(self, EMDpatch):
		self.__name__ = "( less-tolerant-than-me? " + str(EMDpatch)  + " ) "
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
class gethomepatch:
	__name__ = "gethomepatch"
	def __init__(self,):
		self.__name__ = "( gethomepatch " + " ) "
	def __str__(self):
		return self.__name__
	def __repr__(self):
		return self.__name__
class EMDpatch:
	__name__ = "EMDpatch"
	def __init__(self, nlString):
		self.__name__ = str(nlString)
	def __str__(self):
		return self.__name__
	def __repr__(self):
		return self.__name__
class EMDfloat:
	__name__ = "EMDfloat"
	def __init__(self, nlString):
		self.__name__ = str(nlString)
	def __str__(self):
		return self.__name__
	def __repr__(self):
		return self.__name__
class EMDboolean:
	__name__ = "EMDboolean"
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
	pset.addPrimitive(calc_fraction_of_friends,  [ EMDpatch ], EMDfloat, name = "calc_fraction_of_friends")
	pset.addTerminal(EMDboolean(happy()), EMDboolean, name = "happy")
	pset.addPrimitive(EMDboolean, [EMDboolean], EMDboolean)
	pset.addPrimitive(same_color_group,  [ EMDpatch ], EMDboolean, name = "same_color_group")
	pset.addPrimitive(similar_tolerance,  [ EMDpatch ], EMDboolean, name = "similar_tolerance")
	pset.addPrimitive(requires_more_friends_than_me,  [ EMDpatch ], EMDboolean, name = "requires_more_friends_than_me")
	pset.addPrimitive(less_tolerant_than_me,  [ EMDpatch ], EMDboolean, name = "less_tolerant_than_me")
	pset.addTerminal(EMDpatch(getneighbor()), EMDpatch, name = "getneighbor")
	pset.addPrimitive(EMDpatch, [EMDpatch], EMDpatch)
	pset.addTerminal(EMDpatch(gethomepatch()), EMDpatch, name = "gethomepatch")
	pset.addPrimitive(EMDpatch, [EMDpatch], EMDpatch)
	pset.addPrimitive(EMD_ModelEvaluation, [EMDfloat], EMD_ModelEvaluation)
	return pset