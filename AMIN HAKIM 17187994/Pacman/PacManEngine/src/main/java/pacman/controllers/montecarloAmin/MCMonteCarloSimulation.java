package pacman.controllers.montecarloAmin;

import pacman.controllers.Controller;
import pacman.controllers.examples.StarterGhosts;
import pacman.game.Game;
import pacman.game.Constants.MOVE;

public class MCMonteCarloSimulation {
	
	MOVE givenMove;
	Game game;
	int numberOfTrials;
	private static Controller<MOVE> MCMonteCarloPacman;
	
	public MCMonteCarloSimulation(Game game, MOVE move, int numberOfTrials) {
		this.givenMove = move;
		this.game = game;
		if(MCMonteCarloPacman == null){
			MCMonteCarloPacman = new MCMonteCarloPacMan();
		}
		this.numberOfTrials = numberOfTrials;
	}
	
	public double runSimulation() {
		double averageScore = 0;

		for(int i = 0; i< numberOfTrials; i++) {
			MCExecutor executor = new MCExecutor(game.copy());
			int score = executor.runMonteCarloExperiment(MCMonteCarloPacman, new StarterGhosts(), givenMove);

			averageScore += score;
		}

		averageScore = averageScore/ numberOfTrials;
		
		return averageScore;
	}

}
