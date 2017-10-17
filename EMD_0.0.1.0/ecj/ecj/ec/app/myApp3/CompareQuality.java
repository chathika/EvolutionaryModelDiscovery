package ec.app.myApp3;
import ec.*;
import ec.gp.*;
import ec.util.*;
import java.util.*;

public class CompareQuality extends GPNode {
	public String toString() {
		return "CompareQuality";
	}

	public int expectedChildren() {
		return 0;
	}
	static long id = 0;
	Random rand = new Random();
	public void eval(final EvolutionState state, final int thread, final GPData input, final ADFStack stack,
			final GPIndividual individual, final Problem problem) {
		NetlogoData data = ((NetlogoData)(input));
		id = System.currentTimeMillis()+ rand.nextInt(1000);
		StringBuffer result = new StringBuffer(data.netlogoString.toString());
		data.netlogoString.append(" [first" + id + " second" + id + "] -> [quality] of first" + id + "  > [quality] of second" + id + "");
		
		id++;
	}
}