package ec.app.myApp3;
import ec.util.*;
import ec.*;
import ec.gp.*;

public class NetlogoData extends GPData
{
	public StringBuffer netlogoString = new StringBuffer();
	//public String logicString;

	public void copyTo(final GPData gpd)   // copy my stuff to another PatchData
		{ 
			((NetlogoData)gpd).netlogoString = netlogoString;
			//((NetlogoData)gpd).logicString = logicString;
		}
		
	public Object clone() {
		NetlogoData other = (NetlogoData)(super.clone());
		other.netlogoString = (StringBuffer)(new StringBuffer(netlogoString));
		return other;
	}

}