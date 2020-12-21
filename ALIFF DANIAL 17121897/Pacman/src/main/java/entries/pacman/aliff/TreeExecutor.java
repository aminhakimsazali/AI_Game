package entries.pacman.aliff;

import java.util.EnumMap;

import pacman.Executor;
import pacman.controllers.Controller;
import pacman.game.Game;
import pacman.game.Constants.GHOST;
import static pacman.game.Constants.*;
import pacman.game.Constants.MOVE;

public class TreeExecutor{
	Game game;
	final static int NUMBER_OF_MOVES = 50;
	int initialGameScore;
	final static int DEATH_SCORE = -600;
	final static int ALIVE_SCORE = 40;
	final static int GHOST_EATEN_SCORE = 200;
	final static int EATEN_POWERPILLS_SCORE = 100;
	final static int EATEN_PILLS_SCORE = 1;
	final static int LAST_QUARTER_EATEN_PILLS_SCORE = 2;
	final static int LAST_QQ_EATEN_PILLS_SCORE = 4;
	final static int LAST_EATEN_PILLS_SCORE = 100;
	final static int LEVEL_SCORE = 3000;
	private static Controller<MOVE> random_walker  = new random_walk();


	public TreeExecutor(Game game) {
		this.game = game.copy();
		this.initialGameScore = calculateGameScore();

	}

	public int runExperiment(Controller<MOVE> pacManController,
			Controller<EnumMap<GHOST, MOVE>> ghostController, MOVE firstMove) {

		game.advanceGame(
				firstMove,
				ghostController.getMove(game.copy(), System.currentTimeMillis()
						+ DELAY));

		for (int i = 0; i < NUMBER_OF_MOVES; i++) {
			game.advanceGame(
					pacManController.getMove(game, System.currentTimeMillis()
							+ DELAY),
					ghostController.getMove(game, System.currentTimeMillis()
							+ DELAY));
			// System.out.println(game.getPacmanLastMoveMade());
		}

		int gameScore = calculateGameScore();

		return gameScore - initialGameScore;

	}

	// get gameScore for evaluation of each move
	private int calculateGameScore() {
		
		int mcScore = 0;

		if (game.gameOver()) {
			mcScore += DEATH_SCORE;
		} else {
			if (game.getPacmanNumberOfLivesRemaining() > 0) {
				mcScore += game.getPacmanNumberOfLivesRemaining() * ALIVE_SCORE;
			}
		}

		mcScore += game.getNumGhostsEaten() * GHOST_EATEN_SCORE;
		mcScore += evaluateOpp(mcScore);
		mcScore += evaluatePills(mcScore);
		mcScore += evaluatePilleat(mcScore);
		mcScore += game.getCurrentLevel() * LEVEL_SCORE;
		mcScore += game.getScore();
		
		return mcScore;
	}

	private int evaluatePills(int mcScore) {
		
		mcScore += EATEN_POWERPILLS_SCORE
				* (game.getNumberOfPowerPills() - game
						.getNumberOfActivePowerPills());
		int numberOfEatenPills = game.getNumberOfPills()
				- game.getNumberOfActivePills();
		if (game.getNumberOfActivePills() < (game.getNumberOfPills() / 4)) {
			if (game.getNumberOfActivePills() < 3) {
				mcScore += LAST_EATEN_PILLS_SCORE * numberOfEatenPills;
			} else if (game.getNumberOfActivePills() < (game.getNumberOfPills() / 8))
				mcScore += LAST_QQ_EATEN_PILLS_SCORE * numberOfEatenPills;
			else {
				mcScore += LAST_QUARTER_EATEN_PILLS_SCORE * numberOfEatenPills;
			}
		} else {
			mcScore += EATEN_PILLS_SCORE * numberOfEatenPills;

		}
		return mcScore;
	}
	
	private int evaluateOpp(int mcScore) {
		
		MOVE ghostMove = getMoveTowardsEdibleGhost(game);
		
		
		if (ghostMove != MOVE.NEUTRAL)
		{

			mcScore += GHOST_EATEN_SCORE;
		}
		
		//get the move towards the nearest pill and give it a bonus of 100 score
		getMoveTowardsPill(game);
		mcScore += 100;
		
		return mcScore;
	}
	private MOVE getMoveTowardsEdibleGhost(Game game)
	{
	
		int currentIndex = game.getPacmanCurrentNodeIndex();
		int min = Integer.MAX_VALUE;
		int closestGhostIndex = -1;
		int distance;
		int ghostIndex; 
		
		for (GHOST ghost: GHOST.values())
		{
			if (game.getGhostEdibleTime(ghost) > 0)
			{
				ghostIndex = game.getGhostCurrentNodeIndex(ghost);
				distance = game.getShortestPathDistance(currentIndex, ghostIndex);
				
				if (distance < min)
				{
					min = distance;
					closestGhostIndex = ghostIndex;
				}
			}
		}
		
		if (closestGhostIndex > -1)
		{

			return game.getNextMoveTowardsTarget(currentIndex, closestGhostIndex, DM.PATH);
		}
		else
		{
			return MOVE.NEUTRAL;
		}
	}
	
	
	/**
	 * Gets the move which moves PacMan closer to the nearest pill.
	 * @param game
	 * @return
	 */
	private MOVE getMoveTowardsPill(Game game)
	{

		int currentIndex = game.getPacmanCurrentNodeIndex();
		int[] pills = game.getActivePillsIndices();
		int closestIndex = game.getClosestNodeIndexFromNodeIndex(currentIndex, pills, DM.PATH);
		
		return game.getNextMoveTowardsTarget(currentIndex, closestIndex, DM.PATH);
	}
	
	public int evaluatePilleat(int mcScore)
	{
		int penalty = 300;
		//inspired by StarterPacMan
		int currentIndex = game.getPacmanCurrentNodeIndex();
		int min = 20;		
		int distance;
		int ghostIndex;
		
		if (isPowerPillActive(game))
		{
			//no ghosts nearby, penalise nodes which eat power pills
			for (GHOST ghost: GHOST.values())
			{
				if (game.getGhostEdibleTime(ghost) > 0)
				{
					ghostIndex = game.getGhostCurrentNodeIndex(ghost);
					distance = game.getShortestPathDistance(currentIndex, ghostIndex);
//					System.out.println("Distance: "+distance);
					if (distance > min)
					{
						mcScore += -penalty;
					}
				}
			}
		}
		return mcScore;
	}
	
	
	/**
	 * Returns true if any ghosts are edible; otherwise, returns false.
	 * @param game
	 * @return
	 */
	private boolean isPowerPillActive(Game game)
	{
		int edibleTime = game.getGhostEdibleTime(GHOST.BLINKY)
			+ game.getGhostEdibleTime(GHOST.INKY)
			+ game.getGhostEdibleTime(GHOST.PINKY)
			+ game.getGhostEdibleTime(GHOST.SUE);
		
		return edibleTime > 0;
	}
	
//	/**
//	 * Gets the move which moves PacMan closer to the nearest pill.
//	 * @param game
//	 * @return
//	 */
//	public int evaluatePillDist(int mcScore, int powerPillcount)
//	{
//		int minimumDistance = 10;
//		int penalty = 300;
//		
//		//we're actually using the closest ghost distance from the beginning of the move, not when the
//		//pill is actually eaten, but it saves simulating when it could make the wrong guess
//		//about ghost behaviour anyway, and it's "close enough"
//		if (getNearestGhostDistance(game) < minimumDistance)
//		{
//			//no ghosts nearby, penalise nodes which eat power pills
//			if (game.getNumberOfActivePowerPills() < powerPillcount) {
//				System.out.println("Eat powerPill");
//				mcScore += -penalty;
//			}
//			
//		}
//		return mcScore;
//	}
//	
//	
//	private double getNearestGhostDistance(Game game)
//	{
//		int[] ghostIndices = new int[GHOST.values().length];
//		int i = 0;
//		
//		for (GHOST ghost: GHOST.values())
//		{
//			ghostIndices[i++] = game.getGhostCurrentNodeIndex(ghost);
//		}
//		
//		int currentIndex = game.getPacmanCurrentNodeIndex();
//		int closestIndex = game.getClosestNodeIndexFromNodeIndex(currentIndex, ghostIndices, DM.PATH);
//		return game.getDistance(currentIndex, closestIndex, DM.PATH);
//	}
	
}