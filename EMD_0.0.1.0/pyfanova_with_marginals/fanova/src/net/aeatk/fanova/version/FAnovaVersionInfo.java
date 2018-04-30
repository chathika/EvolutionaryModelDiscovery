package net.aeatk.fanova.version;

//import org.mangosdk.spi.ProviderFor;

import ca.ubc.cs.beta.aeatk.misc.version.AbstractVersionInfo;
import ca.ubc.cs.beta.aeatk.misc.version.VersionInfo;

//@ProviderFor(VersionInfo.class)
public class FAnovaVersionInfo extends AbstractVersionInfo {

	public FAnovaVersionInfo()
	{
		super("Functional Anova", "fanova-version.txt",true);
	}
}
