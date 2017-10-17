package ec.app.myApp4;
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
		
		Random rand = new Random();
		long id = System.currentTimeMillis() + rand.nextInt(1000);
		StringBuffer result = new StringBuffer(data.netlogoString.toString());
		data.netlogoString.append(" [first" + id + " second" + id + "] -> [yield] of first" + id + "  > [yield] of second" + id + "");
		
	}
}