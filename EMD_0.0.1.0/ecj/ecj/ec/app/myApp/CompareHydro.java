package ec.app.myApp;
import ec.*;
import ec.gp.*;
import ec.util.*;
import java.util.*;
public class CompareHydro extends GPNode {
	public String toString() {
		return "CompareHydro";
	}

	public int expectedChildren() {
		return 0;
	}

	public void eval(final EvolutionState state, final int thread, final GPData input, final ADFStack stack,
			final GPIndividual individual, final Problem problem) {
		NetlogoData rd = ((NetlogoData)(input));
		
		Random rand = new Random();
		long id = System.currentTimeMillis() + rand.nextInt(1000);     
		rd.netlogoString.append(" [ first" + id + " second" + id + " ] -> [hydro] of first" + id + "   > [hydro] of second" + id + " ");
	}
}