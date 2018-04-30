package net.aeatk.fanova;

import java.io.File;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.beust.jcommander.JCommander;
import com.beust.jcommander.ParameterException;

import ca.ubc.cs.beta.aeatk.algorithmexecutionconfiguration.AlgorithmExecutionConfiguration;
import ca.ubc.cs.beta.aeatk.algorithmrunresult.AlgorithmRunResult;
import ca.ubc.cs.beta.aeatk.misc.jcommander.JCommanderHelper;
import ca.ubc.cs.beta.aeatk.misc.version.VersionTracker;
import ca.ubc.cs.beta.aeatk.options.scenario.ScenarioOptions;
import ca.ubc.cs.beta.aeatk.parameterconfigurationspace.ParameterConfigurationSpace;
import ca.ubc.cs.beta.aeatk.probleminstance.ProblemInstance;
import ca.ubc.cs.beta.aeatk.random.SeedableRandomPool;
import ca.ubc.cs.beta.aeatk.runhistory.NewRunHistory;
import ca.ubc.cs.beta.aeatk.runhistory.RunHistory;
import ca.ubc.cs.beta.aeatk.runhistory.ThreadSafeRunHistoryWrapper;
import ca.ubc.cs.beta.aeatk.state.StateDeserializer;
import ca.ubc.cs.beta.aeatk.state.StateFactory;
import ca.ubc.cs.beta.aeatk.state.StateFactoryOptions;
import ca.ubc.cs.beta.aeatk.state.legacy.LegacyStateFactory;

import net.aeatk.fanova.model.FunctionalANOVAModelBuilder;
import net.aeatk.fanova.model.FunctionalANOVARunner;
import net.aeatk.fanova.model.FunctionalANOVAVarianceDecompose;
import net.aeatk.fanova.options.FAnovaOptions;
import net.aeatk.fanova.options.FAnovaOptions.Improvements;

public class FAnovaExecutor {
	private static Logger log;

	public static void main(String[] args) {
		String outputDir = "";
		try {
			
			SeedableRandomPool pool = null;

			try {
				FAnovaOptions fanovaOpts = new FAnovaOptions();
				JCommander jcom;
				
				//Manhandle the options to support --restoreScenario
				args = StateFactoryOptions.processScenarioStateRestore(args);
				ScenarioOptions scenarioOptions = fanovaOpts.scenOpts;
				try {
					jcom = JCommanderHelper.parseCheckingForHelpAndVersion(args, fanovaOpts);
					String runGroupName = fanovaOpts.getRunGroupName();
					scenarioOptions.makeOutputDirectory(runGroupName);
					//File outputDir = new File(options.scenarioConfig.outputDirectory);
					outputDir = scenarioOptions.outputDirectory + File.separator + runGroupName;
					fanovaOpts.loggingOptions.initializeLogging(outputDir, fanovaOpts.seedOptions.numRun);
				} finally {
					log = LoggerFactory.getLogger(FAnovaExecutor.class);
				}

				//Displays version information
				//See the TargetAlgorithmEvaluatorRunnerVersionInfo class for how to manage your own versions.
				VersionTracker.logVersions();

				for(String name : jcom.getParameterFilesToRead()) {
					log.info("Parsing (default) options from file: {} ", name);
				}

				if(fanovaOpts.rfOptions.logModel == null) {
					switch(fanovaOpts.scenOpts._runObj) {
						case RUNTIME:
							fanovaOpts.rfOptions.logModel = true;
							break;
						case QUALITY:
							fanovaOpts.rfOptions.logModel = false;
					}
				}

				//=== Load the runhistory.
				StateFactory sf = new LegacyStateFactory(null, fanovaOpts.stateFactoryOptions.restoreStateFrom);
				AlgorithmExecutionConfiguration execConfig = scenarioOptions.algoExecOptions.getAlgorithmExecutionConfigSkipDirCheck();
				ParameterConfigurationSpace configSpace = execConfig.getParameterConfigurationSpace();
				List<ProblemInstance> instances = scenarioOptions.getTrainingAndTestProblemInstances(new File(".").getAbsolutePath(), 0, 0, true, false, false, false).getTrainingInstances().getInstances();
				RunHistory rh = new ThreadSafeRunHistoryWrapper(new NewRunHistory(scenarioOptions.intraInstanceObj, scenarioOptions.interInstanceObj, scenarioOptions._runObj));
				
				if(fanovaOpts.stateFactoryOptions.restoreIteration == null)	{
					throw new ParameterException("You must specify an iteration to restore");
				}
				StateDeserializer sd = sf.getStateDeserializer("it", fanovaOpts.stateFactoryOptions.restoreIteration, configSpace, instances, execConfig, rh); // FH: counter-intuitively, this is where rh actually gets filled.
				pool = fanovaOpts.seedOptions.getSeedableRandomPool();

				//=== Subsample the runs.
				if (fanovaOpts.numTrainingSamples > 0){
					List<AlgorithmRunResult> algorithmRuns = rh.getAlgorithmRunsExcludingRedundant();
					Integer[] indices = new Integer[algorithmRuns.size()];
					for(int i=0; i<algorithmRuns.size(); i++){
						indices[i]=i;
					}
					List<Integer> shuffledIndices = Arrays.asList( indices );
				    Collections.shuffle( shuffledIndices, pool.getRandom("inputSubsample"));
				    RunHistory subsampledRH = new ThreadSafeRunHistoryWrapper(new NewRunHistory(scenarioOptions.intraInstanceObj, scenarioOptions.interInstanceObj, scenarioOptions._runObj));
				    for(int i=0; i<fanovaOpts.numTrainingSamples; i++){
				    	subsampledRH.append(algorithmRuns.get(shuffledIndices.get(i)));
				    }
				    rh = subsampledRH;
				}
				FunctionalANOVAModelBuilder famb = new FunctionalANOVAModelBuilder();
				famb.learnModel(instances, rh, configSpace, fanovaOpts.rfOptions, fanovaOpts.mbOptions, scenarioOptions, true, pool);
 

				//=== Handle fANOVA options.
				boolean compareToDef = fanovaOpts.compare.equals(Improvements.DEFAULT) ? true : false;
				double quantile = fanovaOpts.compare.equals(Improvements.QUANTILE) ? fanovaOpts.quantileToCompare : -1;


				if(fanovaOpts.mode.equals("ipc")) {
					FunctionalANOVAVarianceDecompose favd = new FunctionalANOVAVarianceDecompose(famb.getRandomForest(), rh.getAlgorithmRunsExcludingRedundant(), configSpace,pool.getRandom("FANOVA_BUILDER"), compareToDef, quantile, fanovaOpts.rfOptions.logModel);
					
					FanovaRemote remote = new FanovaRemote(favd, new IPCMechanism("localhost", fanovaOpts.port), configSpace);
					remote.run();
				} else {
					//=== Run command line version of fanova
					FunctionalANOVARunner.decomposeVariance(famb.getRandomForest(), rh.getAlgorithmRunsExcludingRedundant(), configSpace,pool.getRandom("FANOVA_BUILDER"), compareToDef, quantile, fanovaOpts.computePairwiseInteration, outputDir,fanovaOpts.rfOptions.logModel, fanovaOpts.plotMarginals);
				}
				

			} finally {
				if(pool != null) {
					pool.logUsage();
				}
			}

		}  catch(ParameterException e) {	
			System.out.println(e);
			log.error(e.getMessage());
			if(log.isDebugEnabled()) {
				log.error("Stack trace:",e);
			}

		} catch(Exception e) {
			e.printStackTrace();
		}
	}
}
