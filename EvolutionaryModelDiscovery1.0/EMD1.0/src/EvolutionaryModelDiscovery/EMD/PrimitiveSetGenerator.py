from Factor import Factor
class PrimitiveSetGenerator:
    _FUNCTIONS_FILE_PATH = "ModelFactors.py"
    def generate(self, factors):
        with open(self._FUNCTIONS_FILE_PATH, "a+") as f:
            f.write('\nfrom deap import gp')
            f.write('\npset = gp.PrimitiveSetTyped("main", [], float)')
            for factor in factors:
                parameterString = " [ "
                for parameterType in factor.getParameterTypes():
                    parameterString = parameterString + "{0},".format(parameterType)
                parameterString = '{0} ]'.format(parameterString[:-1])
                if len(factor.getParameterTypes()) == 0 :
                    f.write('\npset.addTerminal({0}, {1})'.format(factor.getSafeName(),factor.getReturnType()))
                else:
                    f.write('\npset.addPrimitive({0}, {1}, {2})'.format(factor.getSafeName(),parameterString,factor.getReturnType()))
            f.write('\ndef getDEAPPrimitiveSet():')
            f.write('\n\treturn pset')
        '''f.write('\npset.addPrimitive(InjectRuleAndEvaluateABM, [nlAgent], float)')
        f.write('\npset.addPrimitive(nlMinOneOf, [nlComparator, nlAgentSet], nlAgent)')

        #Terminals
        agent_sets = ["sheep","wolves","turtles"]
        for agent_set in agent_sets:    
            pset.addTerminal(nlAgentSet(agent_set), nlAgentSet,name = " '" + agent_set + "'")
        pset.addPrimitive(nlAgentSet,[nlAgentSet],nlAgentSet)
        comparator_str_set = ["energy", "distance myself"]
        for comparator_str in comparator_str_set:    
            pset.addTerminal(nlComparator(comparator_str), nlComparator, name = " '" + comparator_str + "'")
        pset.addPrimitive(nlComparator,[nlComparator],nlComparator)
        pset.addTerminal("nobody",nlAgent)
        pset.addTerminal(0,float)
        #Primitives'''