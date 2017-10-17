package ec.app.myApp2;
import ec.*;
import ec.gp.*;
import ec.util.*;

public class IfAnySetBestFarmElse extends GPNode {
	public String toString() {
		return "IfAnySetBestFarmElse";
	}

	public int expectedChildren() {
		return 2;
	}

	public void eval(final EvolutionState state, final int thread, final GPData input, final ADFStack stack,
			final GPIndividual individual, final Problem problem) {
		//String result;
		NetlogoData data1 = ((NetlogoData) (input));
		NetlogoData data2 = (NetlogoData)(data1.clone());
		
		children[0].eval(state, thread, data1, stack, individual, problem);
		StringBuffer patchString = new StringBuffer(data1.netlogoString);//potential farm
		
        data1.netlogoString.insert( 0, "\n if (" );
		//data1.netlogoString.append(patchString);
		data1.netlogoString.append(" != nobody ) [ \n set best-farm ");
		data1.netlogoString.append(patchString);
		data1.netlogoString.append(" \n let best-yield [ yield ] of best-farm \n");
		data1.netlogoString.append(" set farm-x [ pxcor ] of best-farm \n");
		data1.netlogoString.append(" set farm-y [ pycor ] of best-farm \n");
		data1.netlogoString.append(" set farm-plot best-farm \n");
		data1.netlogoString.append(" ask patch farm-x farm-y [ \n");
		data1.netlogoString.append(" set num-occupying-farms 1 \n");
		data1.netlogoString.append(" ] \n");
		
		//
		data1.netlogoString.append(" ] \n");
		
        children[1].eval(state, thread, data2, stack, individual, problem);
		
		data1.netlogoString.append(data2.netlogoString);
	}
}