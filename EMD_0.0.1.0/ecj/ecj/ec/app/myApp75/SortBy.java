package ec.app.myApp75;
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
		//String result;
		NetlogoData data1 = ((NetlogoData) (input));
		NetlogoData data2 = (NetlogoData)(data1.clone());
		
		children[0].eval(state, thread, data1, stack, individual, problem);
		
        data1.netlogoString.insert( 0, " sort-by [ " );
		data1.netlogoString.append(" ] ");
		
        children[1].eval(state, thread, data2, stack, individual, problem);
		
		data1.netlogoString.append(data2.netlogoString);
		
	}
}