/**
* Evolutionary Model Discovery
* Implemented as part of Chathika Gunaratne's PhD dissertation work
* @author Chathika Gunaratne <chathikagunaratne@gmail.com> , <chathika@knights.ucf.edu>
* @date Dec 2016
*
*	@Copyright Notice:
*	This program is free software: you can redistribute it and/or modify
*   it under the terms of the GNU General Public License as published by
*   the Free Software Foundation, either version 3 of the License, or
*   (at your option) any later version.
*
*   This program is distributed in the hope that it will be useful,
*   but WITHOUT ANY WARRANTY; without even the implied warranty of
*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*   GNU General Public License for more details.
*
*   You should have received a copy of the GNU General Public License
*   along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

package GECCOReplicationForFeatureAnalysis;
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
		StringBuffer comparator2Logic = new StringBuffer(data2.logicString);
		
		data1.netlogoString.append(" - " ) ;
		data1.logicString.append("<->");
		data1.netlogoString.append(comparator2);
		data1.logicString.append(comparator2Logic);        

		//surround with brackets
		data1.netlogoString.insert(0,"(");
		data1.netlogoString.append(")");
		data1.logicString.insert(0,"(");
		data1.logicString.append(")");
	}
}