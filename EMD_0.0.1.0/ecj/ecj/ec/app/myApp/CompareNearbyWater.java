package ec.app.myApp;
import ec.*;
import ec.gp.*;
import ec.util.*;
import java.util.*;
public class CompareNearbyWater extends GPNode {
	public String toString() {
		return "CompareNearbyWater";
	}

	public int expectedChildren() {
		return 0;
	}

	public void eval(final EvolutionState state, final int thread, final GPData input, final ADFStack stack,
			final GPIndividual individual, final Problem problem) {
		NetlogoData rd = ((NetlogoData)(input));
		
		Random rand = new Random();
		long id = System.currentTimeMillis() + rand.nextInt(1000);     
		rd.netlogoString.append(" [ first" + id + " second" + id + " ] -> [sum [num-occupying-households] of patches in-radius (5)] of first" + id + "   > [sum [num-occupying-households] of patches in-radius (5)] of second" + id + " ");
	}
}