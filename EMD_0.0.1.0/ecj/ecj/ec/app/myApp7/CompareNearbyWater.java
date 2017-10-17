package ec.app.myApp7;
import ec.*;
import ec.gp.*;
import ec.util.*;
import java.util.*;

public class CompareNearbyWater extends GPNode {
	public String toString() {
		return "CompareNearbyWater";
	}

	public int expectedChildren() {	return 0;}
	
	public void eval(final EvolutionState state, final int thread, final GPData input, final ADFStack stack,
			final GPIndividual individual, final Problem problem) {
		NetlogoData data = ((NetlogoData)(input));
			

		data.netlogoString.append("((sum [num-occupying-households] of patches in-radius (water-source-distance * 2)) / 230)");
		
	}
}

//old version
/*
data.netlogoString.append(" ifelse-value ");
		data.netlogoString.append("\n(min-one-of patches with [water-source = 1] [distance self] != nobody)[");
		data.netlogoString.append("sum [num-occupying-households] of patches with [distance ( min-one-of patches with [water-source = 1] [distance self]) <= water-source-distance] ");
		data.netlogoString.append("]\n[0]");
		data.netlogoString.append("");
		
		*/