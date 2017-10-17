package ec.app.myApp2;
import ec.*;
import ec.gp.*;
import ec.util.*;

public class PotentialFarms extends GPNode
{
	public String toString() { return "potential-farms"; }

	public int expectedChildren() { return 1; }

	public void eval(final EvolutionState state,
				 final int thread,
				 final GPData input,
				 final ADFStack stack,
				 final GPIndividual individual,
				 final Problem problem)
	{
		NetlogoData rd = ((NetlogoData)(input));
		
		children[0].eval(state, thread, input, stack, individual, problem);
		
		rd.netlogoString = rd.netlogoString.insert(0, " ");
		rd.netlogoString.append(" with [(zone != \"Empty\") and (num-occupying-farms = 0) and (num-occupying-households = 0) and (base-yield >= household-min-nutrition-need) ] ");
	}
}