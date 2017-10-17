package ec.app.GECCOReplication01;
import ec.*;
import ec.gp.*;
import ec.util.*;
import java.util.*;

public class CompareYield extends GPNode {
	public String toString() {
		return "CompareYield";
	}

	public int expectedChildren() {
		return 0;
	}
	
	public void eval(final EvolutionState state, final int thread, final GPData input, final ADFStack stack,
			final GPIndividual individual, final Problem problem) {
		NetlogoData data = ((NetlogoData)(input));
		
		data.netlogoString.append(" (yield / 1201) ");
		
	}
}