package ec.app.myApp72;
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
		//data.netlogoString = data.netlogoString.append( "  ");
		
		//data.netlogoString.append(" ifelse-value ");
		//data.netlogoString.append("\n(patches with [(zone != \"Empty\") and (num-occupying-farms = 0) and (num-occupying-households = 0) and (base-yield >= household-min-nutrition-need) ] != nobody)");
		data.netlogoString.append(" potential-farm-set ");
		
		//data.netlogoString.append("\n[patch x-of-farm y-of-farm]");
		
		
	}
}