package ec.app.myApp;
import ec.util.*;
import ec.*;
import ec.gp.*;
import ec.gp.koza.*;
import ec.simple.*;
import org.nlogo.app.App;

public class MyProblem extends GPProblem implements SimpleProblemForm {

	public static final String P_DATA = "data";

	public double currentX;
	public double currentY;
	private String netlogoRoot = "C:/Program Files/NetLogo 5.3.1/app/";
    

    
	public void setup(final EvolutionState state, final Parameter base) {
		
		// very important, remember this
		super.setup(state, base);

		// verify our input is the right class (or subclasses from it)
		if (!(input instanceof NetlogoData))
			state.output.fatal("GPData class must subclass from " + NetlogoData.class, base.push(P_DATA), null);
		
	}

	public void evaluate(final EvolutionState state, final Individual ind, final int subpopulation,
			final int threadnum) {
		if (!ind.evaluated) // don't bother reevaluating
		{
			
			NetlogoData input = (NetlogoData) (this.input);

			int hits = 0;
			double sum = 0.0;
			double expectedResult;
			double result;
			//for (int y = 0; y < 10; y++) {
				currentX = state.random[threadnum].nextDouble();
				currentY = state.random[threadnum].nextDouble();
				expectedResult = currentX * currentX * currentY + currentX * currentY + currentY;
				((GPIndividual) ind).trees[0].child.eval(state, threadnum, input, stack, ((GPIndividual) ind), this);
System.out.println("loop" );
				//netlogo bit start
				result = 0;
				//Netlogo bit start
				App.main(new String[0]);
				System.out.println("Netlogo bit");
				try {
					java.awt.EventQueue.invokeAndWait(													
					new Runnable() {
						public void run() {
							try {
							  App.app().open("C:/Users/chath/OneDrive - University of Central Florida - UCF/CASLab/GP4ABM/impl/Anasazi/"+ "Artificial Anasazi.nlogo");
							}
							catch(java.io.IOException ex) {
								ex.printStackTrace();
							}
						}
					});
			//App.app().command("set density 62");
			
					App.app().command("random-seed 0");
					App.app().command("setup");
					App.app().command("repeat 50 [ go ]");
					result = Double.parseDouble(App.app().report("L2-error").toString());
					System.out.println(
						App.app().report("L2-error")
					);
				} catch(Exception ex) {
					ex.printStackTrace();
				}	
				//netlogo bit end
				//result = //Math.abs(expectedResult - 2);
				if (result <= 0.01)
					hits++;
				sum += result;
			//} 

			// the fitness better be KozaFitness!
			KozaFitness f = ((KozaFitness) ind.fitness);
			f.setStandardizedFitness(state, sum);
			f.hits = hits;
			ind.evaluated = true;
		}
	}
}