package GECCOReplicationForFeatureAnalysis;
import ec.*;
import ec.gp.*;
import ec.util.*;

public class PotentialFarms extends GPNode
{
	public String toString() { return "PotentialFarms"; }

	public int expectedChildren() { return 0; }

	public void eval(final EvolutionState state,
				 final int thread,
				 final GPData input,
				 final ADFStack stack,
				 final GPIndividual individual,
				 final Problem problem)
	{
		NetlogoData data = ((NetlogoData)(input));
		data.netlogoString.append(" potential-farm-set ");
		data.logicString.append("<AllPotentialFarms>");
	}
}