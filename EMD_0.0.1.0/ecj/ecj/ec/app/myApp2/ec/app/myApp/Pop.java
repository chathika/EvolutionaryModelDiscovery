package ec.app.myApp;
import ec.*;
import ec.gp.*;
import ec.util.*;

public class Pop extends GPNode {
	public String toString() {
		return "Pop";
	}

	public int expectedChildren() {
		return 1;
	}

	public void eval(final EvolutionState state, final int thread, final GPData input, final ADFStack stack,
			final GPIndividual individual, final Problem problem) {
		String result;
		NetlogoData rd = ((NetlogoData) (input));

		children[0].eval(state, thread, input, stack, individual, problem);
		result = " first " + rd.netlogoString ;
                
	}
}