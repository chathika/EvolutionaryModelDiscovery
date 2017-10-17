package ec.app.myApp5;

import ec.util.*;
import ec.*;
import ec.gp.*;
import ec.gp.koza.*;
import ec.simple.*;
import org.nlogo.app.App;
import java.util.Random;
import java.io.*;
import java.util.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import org.nlogo.headless.HeadlessWorkspace;
import java.util.concurrent.*;

public class MyProblem extends GPProblem implements SimpleProblemForm {

    public static final String P_DATA = "data";

    public double currentX;
    public double currentY;
    private String modelPath = "C:/Users/ch328575/OneDrive - University of Central Florida - UCF/CASLab/GP4ABM/impl/Anasazi/" + "Artificial Anasazi Ver 5.nlogo";
    private String decisionTreePath = "C:/Users/ch328575/OneDrive - University of Central Florida - UCF/CASLab/GP4ABM/impl/Anasazi/" + "Running Ver 5.nlogo";
    private Random r = new Random();
    private PrintWriter netlogoWriter;
    private File decisionTreeFile;
	
    HeadlessWorkspace workspace;

    public void setup(final EvolutionState state, final Parameter base) {
        // very important, remember this
        super.setup(state, base);
		System.out.println("setup");
        try {
            workspace = HeadlessWorkspace.newInstance();
        } catch (Exception e) {
            e.printStackTrace();
        }
        // verify our input is the right class (or subclasses from it)
        if (!(input instanceof NetlogoData)) {
            state.output.fatal("GPData class must subclass from " + NetlogoData.class, base.push(P_DATA), null);
        }
    }

    public void evaluate(final EvolutionState state, final Individual ind, final int subpopulation,
            final int threadnum) {
        if (!ind.evaluated) // don't bother reevaluating
        {
			
			
			System.out.println("run");
			double result = 0;
			double finalResult = 0;
			int hits = 0;
			int runs = 5;
			for (int run = 0; run < runs ; run++ ){
				NetlogoData input = (NetlogoData) (this.input);
				input.netlogoString.setLength(0);
				((GPIndividual) ind).trees[0].child.eval(state, threadnum, input, stack, ((GPIndividual) ind), this);
				System.out.println("" + input.netlogoString.toString() + "\n");

				try {
					List<String> fileContentOriginal = new ArrayList<>(Files.readAllLines(Paths.get(modelPath), StandardCharsets.UTF_8));
					List<String> fileContentRunning = new ArrayList<>(fileContentOriginal);
					Collections.copy(fileContentRunning, fileContentOriginal);
					for (int i = 0; i < fileContentOriginal.size(); i++) {
						if (fileContentOriginal.get(i).contains(";insert evolutionary code here")) {
							fileContentRunning.set(i, "set best-farm " + input.netlogoString.toString());
							break;
						}
					}
					Files.write(Paths.get(decisionTreePath), fileContentRunning, StandardCharsets.UTF_8);
				} catch (Exception e) {
					e.printStackTrace();
				}

				result = 10000;
				try {
					workspace = HeadlessWorkspace.newInstance();
					workspace.open(decisionTreePath);
					workspace.command("random-seed " + run);
					workspace.command("setup");
					workspace.command("repeat 551 [ go ]");
					result = Double.parseDouble(workspace.report("L2-error").toString());
					workspace.dispose();
				} catch (Exception ex) {
					ex.printStackTrace();
				}
			
				System.out.println("Fitness: "+result);
				if (result <= 733.6)	hits++;
				finalResult += result;
			}
			finalResult = finalResult / runs;
			System.out.println("Final Average Fitness: "+finalResult);
            // the fitness better be KozaFitness!
            KozaFitness f = ((KozaFitness) ind.fitness);
            f.setStandardizedFitness(state, finalResult);
            f.hits = hits;
            ind.evaluated = true;
        }
    }
}
