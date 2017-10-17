package ec.app.myApp72;
import ec.*;
import ec.gp.*;
import ec.util.*;
import java.util.*;

public class CompareDistance extends GPNode {
	public String toString() {
		return "CompareDistance";
	}

	public int expectedChildren() {
		return 0;
	}
	
	public void eval(final EvolutionState state, final int thread, final GPData input, final ADFStack stack,
			final GPIndividual individual, final Problem problem) {
				
		NetlogoData data = ((NetlogoData)(input));
			
        //children[0].eval(state, thread, data, stack, individual, problem);
		
		data.netlogoString.insert(0, " ((distance patch x-of-farm y-of-farm) / 144)");
		
		//data.netlogoString.append("] of self ");
		System.gc();
	}
}