package ec.app.myApp64;
import ec.*;
import ec.gp.*;
import ec.util.*;

public class Min extends GPNode {

	
	public String toString() {return "Min";	} // returns Patch
 //static int con = 0;int visits = 0;
	public int expectedChildren() { // takes a patch set
		return 2;
	}

	public void eval(final EvolutionState state, final int thread, final GPData input, final ADFStack stack,
			final GPIndividual individual, final Problem problem) {
		
		NetlogoData data1 = ((NetlogoData) (input));
		NetlogoData data2 = ((NetlogoData)data1.clone());
		
		children[0].eval(state, thread, data1, stack, individual, problem);
		StringBuffer patchSet = new StringBuffer(data1.netlogoString);
		children[1].eval(state, thread, data2, stack, individual, problem);
		StringBuffer comparator = new StringBuffer(data2.netlogoString);
		
		data1.netlogoString.insert(0, " min-one-of (" ) ;
		data1.netlogoString.append(")[");
		data1.netlogoString.append(comparator);
		data1.netlogoString.append("]");
		
		
           
	}
}