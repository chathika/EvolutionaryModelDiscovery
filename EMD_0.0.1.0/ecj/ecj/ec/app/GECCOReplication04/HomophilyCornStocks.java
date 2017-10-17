package ec.app.GECCOReplication01;
import ec.*;
import ec.gp.*;
import ec.util.*;
import java.util.*;

public class HomophilyCornStocks extends GPNode {
	public String toString() {
		return "HomophilyCornStocks";
	}

	public int expectedChildren() {
		return 0;
	}
	
	public void eval(final EvolutionState state, final int thread, final GPData input, final ADFStack stack,
			final GPIndividual individual, final Problem problem) {
		NetlogoData data = ((NetlogoData)(input));
			
		data.netlogoString.append(" (abs ([reduce + aged-corn-stocks ] of myself -  ifelse-value (count households in-radius water-source-distance != 0 ) [mean [ifelse-value (is-list? aged-corn-stocks)  [reduce + aged-corn-stocks][0]] of households in-radius water-source-distance] [0])) / (0.0001 + max [ifelse-value (is-list? aged-corn-stocks)  [reduce + aged-corn-stocks][0]] of households )");		
	}
}