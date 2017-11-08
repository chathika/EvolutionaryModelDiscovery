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
import ec.util.*;
import ec.*;
import ec.gp.*;

public class NetlogoData extends GPData
{
	public StringBuffer netlogoString = new StringBuffer();
	public StringBuffer logicString = new StringBuffer();

	public void copyTo(final GPData gpd)   // copy my stuff to another PatchData
		{ 
			((NetlogoData)gpd).netlogoString = netlogoString;
			((NetlogoData)gpd).logicString = logicString;
		}
		
	public Object clone() {
		NetlogoData other = (NetlogoData)(super.clone());
		other.netlogoString = (StringBuffer)(new StringBuffer(netlogoString));
		other.logicString = (StringBuffer)(new StringBuffer(logicString));
		return other;
	}

}