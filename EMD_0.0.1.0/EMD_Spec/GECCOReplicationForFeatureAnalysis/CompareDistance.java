package GECCOReplicationForFeatureAnalysis;
import ec.*;
import ec.gp.*;
import ec.util.*;
import java.util.*;

public class CompareDistance extends GPNode {
	public String toString() {
		return "CompareDistance";
	}

	public int expectedChildren() {
		return 0;
	}
	
	public void eval(final EvolutionState state, final int thread, final GPData input, final ADFStack stack,
			final GPIndividual individual, final Problem problem) {
				
		NetlogoData data = ((NetlogoData)(input));
		
		data.netlogoString.append(" ((distance patch x-of-farm y-of-farm) / 144)");
		data.logicString.append("<CompareDistance>");
		
		System.gc();
	}
}