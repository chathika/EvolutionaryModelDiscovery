package ec.app.myApp2;

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
    private String modelPath = "C:/Users/ch328575/OneDrive - University of Central Florida - UCF/CASLab/GP4ABM/impl/Anasazi/" + "Artificial Anasazi Ver 2.nlogo";
    private String decisionTreePath = "C:/Users/ch328575/OneDrive - University of Central Florida - UCF/CASLab/GP4ABM/impl/Anasazi/" + "Running Ver 2.nlogo";
    private Random r = new Random();
    private PrintWriter netlogoWriter;
    private File decisionTreeFile;
	private static double result;
    HeadlessWorkspace workspace;

    public void setup(final EvolutionState state, final Parameter base) {

        // very important, remember this
        super.setup(state, base);
		System.out.println("setup");
        try {
            //netlogoWriter = new BufferedWriter(new FileWriter(modelPath));

            //App.main(new String[0]);
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
            NetlogoData input = (NetlogoData) (this.input);

            int hits = 0;
            //double sum = 0.0;
            //double expectedResult;
            //double result;
            //for (int y = 0; y < 10; y++) {
            //currentX = state.random[threadnum].nextDouble();
            //currentY = state.random[threadnum].nextDouble();
            //expectedResult = currentX * currentX * currentY + currentX * currentY + currentY;
            input.netlogoString.setLength(0);
            ((GPIndividual) ind).trees[0].child.eval(state, threadnum, input, stack, ((GPIndividual) ind), this);
            System.out.println("" + input.netlogoString.toString() + "\n");
            try {

                List<String> fileContentOriginal = new ArrayList<>(Files.readAllLines(Paths.get(modelPath), StandardCharsets.UTF_8));
                List<String> fileContentRunning = new ArrayList<>(fileContentOriginal);
                Collections.copy(fileContentRunning, fileContentOriginal);

                for (int i = 0; i < fileContentOriginal.size(); i++) {
                    if (fileContentOriginal.get(i).contains(";insert evolutionary code here")) {
                        fileContentRunning.set(i, input.netlogoString.toString());
                        break;
                    }
                }
                Files.write(Paths.get(decisionTreePath), fileContentRunning, StandardCharsets.UTF_8);

            } catch (Exception e) {
                e.printStackTrace();
            }
            //netlogo bit start
             result = 10000;

            try {
                /*java.awt.EventQueue.invokeAndWait(													
		new Runnable() {
			public void run() {
				try {
				  App.app().open(decisionTreePath);
				}
				catch(java.io.IOException ex) {
					ex.printStackTrace();
				}
			}
		}
	);*/
                workspace = HeadlessWorkspace.newInstance();
                workspace.open(decisionTreePath);
                //workspace.command("random-seed 0");
                workspace.command("setup");
				
						
							workspace.command("repeat 551 [ go ]");
							result = Double.parseDouble(workspace.report("L2-error").toString());
							
				workspace.dispose();
				

				
                //App.app().command("setup");
                //App.app().command("repeat 551 [ go ]");
                //result = Double.parseDouble(App.app().report("L2-error").toString());
                //System.out.println(
                //App.app().report("L2-error")
                //);
            } catch (Exception ex) {
                ex.printStackTrace();
            }
            //netlogo bit end
			
			System.out.println("Fitness: "+result);
            if (result <= 900) {
                hits++;
                
            }
            //sum += result;
            //} 

            // the fitness better be KozaFitness!
            KozaFitness f = ((KozaFitness) ind.fitness);
            f.setStandardizedFitness(state, result);
            f.hits = hits;
            ind.evaluated = true;
        }
    }
}
