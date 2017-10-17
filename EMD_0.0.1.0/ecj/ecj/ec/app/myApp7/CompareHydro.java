package ec.app.myApp7;
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
		NetlogoData data = ((NetlogoData)(input));
		
		
		//data.netlogoString.append(" ifelse-value ");
		//data.netlogoString.append("\n(patches with [distance (patch x-of-farm y-of-farm) <= water-source-distance] != nobody)");
		data.netlogoString.append(" ((mean [hydro] of patches in-radius (water-source-distance * 2)) / 10)");
		//data.netlogoString.append("\n[0]");
	}
}

//old way
/*
data.netlogoString.append(" ifelse-value ");
		data.netlogoString.append("\n(patches with [distance (patch x-of-farm y-of-farm) <= water-source-distance] != nobody)");
		data.netlogoString.append("[[hydro] of patches with [distance  (patch x-of-farm y-of-farm) <= water-source-distance]] ");
		data.netlogoString.append("\n[0]"); */