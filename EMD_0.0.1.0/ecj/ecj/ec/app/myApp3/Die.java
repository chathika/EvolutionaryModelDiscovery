package ec.app.myApp3;
import ec.*;
import ec.gp.*;
import ec.util.*;

public class Die extends GPNode
{
	public String toString() { return "die"; }

	public int expectedChildren() { return 0; }

	public void eval(final EvolutionState state,
				 final int thread,
				 final GPData input,
				 final ADFStack stack,
				 final GPIndividual individual,
				 final Problem problem)
	{
		NetlogoData rd = ((NetlogoData)(input));
		rd.netlogoString = rd.netlogoString.append( " if still-hunting? [ ");
		rd.netlogoString.append( " ask patch farm-x farm-y [ set num-occupying-farms 0 ]");
		rd.netlogoString.append( " die");
		rd.netlogoString.append( " ]");
	}
}