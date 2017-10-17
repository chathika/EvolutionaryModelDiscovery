package ec.app.GECCOReplication01;
import ec.*;
import ec.gp.*;
import ec.util.*;
import java.util.*;

public class PotentialFarmsNearFamily extends GPNode {
	public String toString() {
		return "PotentialFarmsNearFamily";
	}

	public int expectedChildren() {
		return 0;
	}
	
	public void eval(final EvolutionState state, final int thread, final GPData input, final ADFStack stack,
			final GPIndividual individual, final Problem problem) {
		NetlogoData data = ((NetlogoData)(input));
			
		data.netlogoString.append(" potential-family-farms ");
		
	}
}