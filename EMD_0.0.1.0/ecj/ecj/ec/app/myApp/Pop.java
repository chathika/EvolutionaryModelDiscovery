package ec.app.myApp;
import ec.*;
import ec.gp.*;
import ec.util.*;

public class Pop extends GPNode {

	
	public String toString() {
		return "Pop";
	}
 //static int con = 0;int visits = 0;
	public int expectedChildren() {
		return 1;
	}

	public void eval(final EvolutionState state, final int thread, final GPData input, final ADFStack stack,
			final GPIndividual individual, final Problem problem) {
		
		NetlogoData rd = ((NetlogoData) (input));
		
		children[0].eval(state, thread, input, stack, individual, problem);
		
		rd.netlogoString.insert(0, " first " ) ;
           
	}
}