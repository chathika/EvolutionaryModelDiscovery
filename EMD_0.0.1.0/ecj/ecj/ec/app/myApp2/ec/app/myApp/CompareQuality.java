package ec.app.myApp;
import ec.*;
import ec.gp.*;
import ec.util.*;

public class CompareQuality extends GPNode {
	public String toString() {
		return "CompareQuality";
	}

	public int expectedChildren() {
		return 0;
	}

	public void eval(final EvolutionState state, final int thread, final GPData input, final ADFStack stack,
			final GPIndividual individual, final Problem problem) {
		NetlogoData rd = ((NetlogoData)(input));
		rd.netlogoString += " [ [quality] of ?1  > [quality] of ?2] ";
	}
}