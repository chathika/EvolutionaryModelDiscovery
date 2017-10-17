package ec.app.myApp4;
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
		NetlogoData rd = ((NetlogoData)(input));
		rd.netlogoString = rd.netlogoString.append( " potential-farms ");
	}
}