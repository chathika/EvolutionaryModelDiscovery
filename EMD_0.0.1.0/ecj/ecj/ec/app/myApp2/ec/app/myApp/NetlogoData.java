package ec.app.myApp;
import ec.util.*;
import ec.*;
import ec.gp.*;

public class NetlogoData extends GPData
{
	public String netlogoString;
	public String logicString;

	public void copyTo(final GPData gpd)   // copy my stuff to another PatchData
		{ 
			((NetlogoData)gpd).netlogoString = netlogoString;
			((NetlogoData)gpd).logicString = logicString;
		}
}