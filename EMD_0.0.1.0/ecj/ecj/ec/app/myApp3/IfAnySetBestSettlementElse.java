package ec.app.myApp3;
import ec.*;
import ec.gp.*;
import ec.util.*;

public class IfAnySetBestSettlementElse extends GPNode {
	public String toString() {
		return "IfAnySetBestSettlementElse";
	}

	public int expectedChildren() {
		return 2;
	}

	public void eval(final EvolutionState state, final int thread, final GPData input, final ADFStack stack,
			final GPIndividual individual, final Problem problem) {
		//String result;
		NetlogoData data1 = ((NetlogoData) (input));
		NetlogoData data2 = (NetlogoData)(data1.clone());
		
		children[0].eval(state, thread, data1, stack, individual, problem);//potential water source
		StringBuffer patchString = new StringBuffer(data1.netlogoString);
		
        data1.netlogoString.insert( 0, "\n if still-hunting? and (");
		//data1.netlogoString.append(patchString);
		data1.netlogoString.append(" != nobody) [ \n" );
		data1.netlogoString.append(" ask ");
		data1.netlogoString.append(patchString);
		data1.netlogoString.append("[\n");
		data1.netlogoString.append(" set x pxcor");
		data1.netlogoString.append(" set y pycor");
		data1.netlogoString.append(" set still-hunting? false");
		data1.netlogoString.append("\n]\n");
		data1.netlogoString.append(" if not still-hunting? [\n");
		data1.netlogoString.append(" ask min-one-of patches with [ num-occupying-farms = 0 and hydro <= 0 ] [ distancexy x y ] [\n");
		data1.netlogoString.append(" set x pxcor");
		data1.netlogoString.append(" set y pycor");
		data1.netlogoString.append(" set num-occupying-households num-occupying-households + 1");
		data1.netlogoString.append("\n]");
		data1.netlogoString.append("\n]");
		data1.netlogoString.append("\n]");
		
		children[1].eval(state, thread, data2, stack, individual, problem); // next statement
		data1.netlogoString.append(data2.netlogoString);
	}
}