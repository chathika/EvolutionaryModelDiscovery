package ec.app.myApp75;
import ec.*;
import ec.gp.*;
import ec.util.*;

public class Negate extends GPNode {

	
	public String toString() {return "Negate";	} // returns Patch
 //static int con = 0;int visits = 0;
	public int expectedChildren() { // takes two comparators
		return 2;
	}

	public void eval(final EvolutionState state, final int thread, final GPData input, final ADFStack stack,
			final GPIndividual individual, final Problem problem) {
		
		NetlogoData data1 = ((NetlogoData) (input));
		NetlogoData data2 = ((NetlogoData)data1.clone());
		
		children[0].eval(state, thread, data1, stack, individual, problem); //comparator1
		
		children[1].eval(state, thread, data2, stack, individual, problem);//comparator2
		StringBuffer comparator2 = new StringBuffer(data2.netlogoString);
		
		data1.netlogoString.append(" - " ) ;
		data1.netlogoString.append(comparator2);
		
		
           
	}
}