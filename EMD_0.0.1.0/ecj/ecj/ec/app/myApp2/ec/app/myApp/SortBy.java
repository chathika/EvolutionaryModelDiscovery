package ec.app.myApp;
import ec.*;
import ec.gp.*;
import ec.util.*;

public class SortBy extends GPNode {
	public String toString() {
		return "SortBy";
	}

	public int expectedChildren() {
		return 2;
	}

	public void eval(final EvolutionState state, final int thread, final GPData input, final ADFStack stack,
			final GPIndividual individual, final Problem problem) {
		String result;
		NetlogoData data = ((NetlogoData) (input));

		children[0].eval(state, thread, data, stack, individual, problem);
                //result = data.netlogoString;
        children[1].eval(state, thread, data, stack, individual, problem);
		result = data.netlogoString;
		result = " sort-by " + result ;
	}
}