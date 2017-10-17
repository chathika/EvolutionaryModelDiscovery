package ec.app.myApp4;
import ec.*;
import ec.gp.*;
import ec.util.*;
import java.util.*;

public class CompareNearbyWater extends GPNode {
	public String toString() {
		return "CompareNearbyWater";
	}

	public int expectedChildren() {	return 0;}
	
	public void eval(final EvolutionState state, final int thread, final GPData input, final ADFStack stack,
			final GPIndividual individual, final Problem problem) {
		NetlogoData data = ((NetlogoData)(input));
			
		Random rand = new Random();
		long id = System.currentTimeMillis() + rand.nextInt(1000);
		StringBuffer result = new StringBuffer(data.netlogoString.toString());
		data.netlogoString.append(" [first" + id + " second" + id + "] -> length [num-occupying-households] of patches with [distance ( min-one-of patches with [water-source = 1] [distance first" + id + " ]) <= water-source-distance] > length [num-occupying-households] of patches with [distance ( min-one-of patches with [water-source = 1] [distance second" + id + " ]) <= water-source-distance]");
		
	}
}

