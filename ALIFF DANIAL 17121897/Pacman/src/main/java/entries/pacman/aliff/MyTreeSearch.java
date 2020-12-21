package entries.pacman.aliff;



import pacman.Executor;
import pacman.controllers.Controller;
import pacman.controllers.examples.AggressiveGhosts;
import pacman.controllers.examples.Legacy;
import pacman.controllers.examples.RandomGhosts;
import pacman.controllers.examples.StarterGhosts;
import pacman.game.Game;
import pacman.game.Constants.MOVE;
import pacman.controllers.examples.StarterPacMan;

public class MyTreeSearch {
	
	MOVE givenMove;
	Game game;
	int numberOfTrials;
	private static Controller<MOVE> random_walker;
	
	public MyTreeSearch(Game game, MOVE move, int numberOfTrials) {
		this.givenMove = move;
		this.game = game;
		if(random_walker == null){
			random_walker = new random_walk();
		}
		this.numberOfTrials = numberOfTrials;
	}
	
	public double runSimulation() {
		double averageScore = 0;
		for(int i = 0; i< numberOfTrials; i++) {
			TreeExecutor executor = new TreeExecutor(game.copy());
			
			// This is where the score will be received
			int score = executor.runExperiment(random_walker, new StarterGhosts(), givenMove);
			
			averageScore += score;
		}
		
		averageScore = averageScore/ numberOfTrials;
		
		return averageScore;
	}

}


