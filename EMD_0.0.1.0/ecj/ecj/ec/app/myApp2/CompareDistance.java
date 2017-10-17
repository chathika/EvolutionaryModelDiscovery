package ec.app.myApp2;
import ec.*;
import ec.gp.*;
import ec.util.*;
import java.util.*;

public class CompareDistance extends GPNode {
	public String toString() {
		return "CompareDistance";
	}

	public int expectedChildren() {
		return 1;
	}
	static long id = 0;
	Random rand = new Random();
	public void eval(final EvolutionState state, final int thread, final GPData input, final ADFStack stack,
			final GPIndividual individual, final Problem problem) {
                //String result;
		NetlogoData data = ((NetlogoData)(input));
        id = System.currentTimeMillis() + rand.nextInt(1000);
        children[0].eval(state, thread, input, stack, individual, problem);
        StringBuffer result = new StringBuffer(data.netlogoString.toString());
		data.netlogoString.insert(0, " [first" + id + " second" + id + "] -> [distance ");
		data.netlogoString.append( " ] of first" + id + " > [distance ");
		data.netlogoString.append(result);
		data.netlogoString.append(" ] of second" + id + " ");
		
		result = null;
		;
		System.gc();
	}
}