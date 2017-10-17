package ec.app.myApp;
import ec.*;
import ec.gp.*;
import ec.util.*;

public class CompareDistance extends GPNode {
	public String toString() {
		return "CompareQuality";
	}

	public int expectedChildren() {
		return 1;
	}

	public void eval(final EvolutionState state, final int thread, final GPData input, final ADFStack stack,
			final GPIndividual individual, final Problem problem) {
                String result;
		NetlogoData data = ((NetlogoData)(input));
                
                children[0].eval(state, thread, input, stack, individual, problem);
                result = data.netlogoString;
                System.out.println("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$");
		data.netlogoString += " [ [distance "  + result  +  " ] of ?1  > [distance " + result + " ] of ?2] ";
	}
}