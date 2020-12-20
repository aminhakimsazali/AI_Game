
import examples.StarterGhostComm.Blinky;
import examples.StarterGhostComm.Inky;
import examples.StarterGhostComm.Pinky;
import examples.StarterGhostComm.Sue;
import pacman.Executor;
import pacman.controllers.IndividualGhostController;
import pacman.controllers.MASController;
import pacman.controllers.examples.po.POCommGhosts;
import pacman.controllers.montecarloAmin.MCPacMan;
import pacman.game.Constants.*;
import pacman.game.internal.POType;

import java.util.EnumMap;

/**
 * Created by pwillic on 06/05/2016.
 */
public class Main {

    public static void main(String[] args) {

        Executor executor = new Executor.Builder()
                .setVisual(true)
                .setPacmanPO(false)
                .setTickLimit(10000)
                .setScaleFactor(3) // Increase game visual size
                .setPOType(POType.RADIUS) // pacman sense objects around it in a radius wide fashion instead of straight line sights
                .setSightLimit(5000) // The sight radius limit, set to maximum 
                .build();

        EnumMap<GHOST, IndividualGhostController> controllers = new EnumMap<>(GHOST.class);

        controllers.put(GHOST.INKY, new Inky());
        controllers.put(GHOST.BLINKY, new Blinky());
        controllers.put(GHOST.PINKY, new Pinky());
        controllers.put(GHOST.SUE, new Sue());

        MASController ghosts = new POCommGhosts(100);
        executor.runGame(new MCPacMan(), ghosts, 10);
        executor.runExperiment(new MCPacMan(), ghosts, 10, "");


    }
}


















//        executor.runGame(new MonteCarloPacMan(), ghosts, 10);
//        executor.runExperiment(new MonteCarloPacMan(), ghosts, 10, "Monte Carlo Medium");

//        executor.runExperiment(new TreeSearchPacMan(), ghosts, 10, "Tree Search");
//        executor.runExperiment(new MyPacMan(), ghosts, 10, "Stater Pacman");
