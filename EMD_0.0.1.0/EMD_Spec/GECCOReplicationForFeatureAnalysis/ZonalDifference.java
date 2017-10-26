package GECCOReplicationForFeatureAnalysis;
import ec.*;
import ec.gp.*;
import ec.util.*;
import java.util.*;

public class ZonalDifference extends GPNode {
	public String toString() {
		return "ZonalDifference";
	}

	public int expectedChildren() {
		return 0;
	}
	
	public void eval(final EvolutionState state, final int thread, final GPData input, final ADFStack stack,
			final GPIndividual individual, final Problem problem) {
		NetlogoData data = ((NetlogoData)(input));
			
		data.netlogoString.append(" ifelse-value (zone = [zone] of patch-at ([farm-x] of myself) ([farm-y] of myself))  [0] [1] ");
		data.logicString.append("<flee-migrate>");
	}
}