package GECCOReplicationForFeatureAnalysis;
import ec.*;
import ec.gp.*;
import ec.util.*;
import java.util.*;

public class HomophilyAge extends GPNode {
	public String toString() {
		return "HomophilyAge";
	}

	public int expectedChildren() {
		return 0;
	}
	
	public void eval(final EvolutionState state, final int thread, final GPData input, final ADFStack stack,
			final GPIndividual individual, final Problem problem) {
		NetlogoData data = ((NetlogoData)(input));
			
		data.netlogoString.append(" ((abs ([age] of myself -  ifelse-value (count households in-radius water-source-distance != 0) [mean [age] of households in-radius water-source-distance] [0])) / (0.0001 + max [age] of households) )");
		data.logicString.append("<HomophilyAge>");
	}
}