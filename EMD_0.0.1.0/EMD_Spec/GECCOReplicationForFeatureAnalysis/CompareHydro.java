package GECCOReplicationForFeatureAnalysis;
import ec.*;
import ec.gp.*;
import ec.util.*;
import java.util.*;

public class CompareHydro extends GPNode {
	public String toString() {
		return "CompareWater";
	}

	public int expectedChildren() {
		return 0;
	}
	
	public void eval(final EvolutionState state, final int thread, final GPData input, final ADFStack stack,
			final GPIndividual individual, final Problem problem) {
		NetlogoData data = ((NetlogoData)(input));
		
		data.netlogoString.append(" ((mean [hydro] of patches in-radius (water-source-distance * 2)) / 10)");
		data.logicString.append("<CompareWater>");
	}
}