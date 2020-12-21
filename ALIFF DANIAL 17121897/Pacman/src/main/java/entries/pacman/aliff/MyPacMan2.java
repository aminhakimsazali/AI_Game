package entries.pacman.aliff;

import pacman.Executor;
import pacman.controllers.Controller;
import pacman.controllers.PacmanController;
import pacman.game.Constants;
import pacman.game.Constants.DM;
import pacman.game.Constants.GHOST;
import pacman.game.Constants.MOVE;
import pacman.game.Game;
import pacman.game.GameView;

import java.awt.Color;
import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import java.util.Random;

public class MyPacMan2 extends Controller<MOVE> {
	final static int NUMBER_OF_TRIALS = 100;	
	@Override
	public MOVE getMove(Game game, long timeDue) {
			
			int currentNode = game.getPacmanCurrentNodeIndex();
			
			// Check if it is the first move or pacman is in junction  or pacman is eaten
			if(game.isJunction(currentNode) || lastMove == null ||game.wasPacManEaten()) {
				
				MOVE move = simulate(game, currentNode);
				
				lastMove = move;

				return move;
			} // else move towards the junction which is not last junction
			else {
				
				MOVE[] possibleMoves = game.getPossibleMoves(currentNode, lastMove);
				assert possibleMoves.length == 1: "More than One neigbor";
				
				// possibleMoves returns null when pacman has died
				if(possibleMoves != null) {
					lastMove = possibleMoves[0];
				} else {
					
				}
				
				return lastMove;
				
			}
			
		}

		private MOVE simulate(Game game, int currentNode) {

			int neighboringNodes[] = null;

			// To check whether the pacman is dead or not		
			if(lastMove != null) {
				 neighboringNodes = game.getNeighbouringNodes(currentNode);
			} else {
				neighboringNodes = game.getNeighbouringNodes(currentNode);
			}
			
			// when neighboringNodes is null, means that Pacman is dead.
			if(neighboringNodes == null) {
				return MOVE.NEUTRAL;
			}
			
			// initialize the array for each neighbournode
			double scoresNeighboringNodes[] = new double[neighboringNodes.length];
			

			// It is time to simulate to all neighboring nodes
			for (int i = 0; i < neighboringNodes.length; i++) {
				MOVE moveToReach = game.getMoveToMakeToReachDirectNeighbour(currentNode, neighboringNodes[i]);
				MyTreeSearch simulation = new MyTreeSearch(
						game, moveToReach, NUMBER_OF_TRIALS);
				
				
				double score = simulation.runSimulation();

				
				scoresNeighboringNodes[i] = score;
			}
			
			// Reiterate the scores to find the best one
			double scoreMax = Double.NEGATIVE_INFINITY;
			int bestNode = -1;
			for (int j = 0; j < scoresNeighboringNodes.length; j++) {

				if (scoresNeighboringNodes[j] > scoreMax) {
					scoreMax = scoresNeighboringNodes[j];
					bestNode = neighboringNodes[j];
				}
			}
			
			
			MOVE move = game.getMoveToMakeToReachDirectNeighbour(currentNode, bestNode);
			
			return move;
		}
}
