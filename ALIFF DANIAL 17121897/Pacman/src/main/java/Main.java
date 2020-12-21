

import pacman.Executor;
import pacman.controllers.IndividualGhostController;
import pacman.controllers.MASController;
import pacman.controllers.examples.po.POCommGhosts;
import pacman.entries.ghostMAS.Blinky;
import pacman.entries.ghostMAS.Inky;
import pacman.entries.ghostMAS.Pinky;
import pacman.entries.ghostMAS.Sue;
import pacman.game.Constants.*;
import pacman.game.internal.POType;
import entries.pacman.aliff.MyPacMan2;

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
                .setScaleFactor(2) // Increase game visual size
                .setPOType(POType.RADIUS) // pacman sense objects around it in a radius wide fashion instead of straight line sights
                .setSightLimit(5000) // The sight radius limit, set to maximum 
                .build();

//        EnumMap<GHOST, IndividualGhostController> controllers = new EnumMap<>(GHOST.class);
//
//        controllers.put(GHOST.INKY, new Inky());
//        controllers.put(GHOST.BLINKY, new Blinky());
//        controllers.put(GHOST.PINKY, new Pinky());
//        controllers.put(GHOST.SUE, new Sue());

        MASController ghosts = new POCommGhosts(50);
        executor.runGame(new MyPacMan2(), ghosts, 10);

//        System.out.print("Monte Pac Man");
//        Double final_score = 0.0;
//        for(int i=0;i<10;i++) {
//        	final_score += executor.runExperiment(new MyPacMan2(), ghosts, 10);
//        }
//        System.out.println("Final Average: " + final_score/10);
//        
//        executor.runExperiment(new MyPacMan2(), ghosts, 10);
    }
}