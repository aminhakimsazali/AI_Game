using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using Random = UnityEngine.Random;

[Flags]
public enum WallState
{
    // 0000 -> NO WALLS
    // 1111 -> LEFT,RIGHT,UP,DOWN
    LEFT = 1, // 0001
    RIGHT = 2, // 0010
    UP = 4, // 0100
    DOWN = 8, // 1000

    VISITED = 128, // 1000 0000
}

public struct Position
{
    public int X;
    public int Y;
}

public struct Neighbour
{
    public Position Position;
    public WallState SharedWall;
}

public static class MazeGenerator
{

    private static WallState GetOppositeWall(WallState wall)
    {
        switch (wall)
        {
            case WallState.RIGHT: return WallState.LEFT;
            case WallState.LEFT: return WallState.RIGHT;
            case WallState.UP: return WallState.DOWN;
            case WallState.DOWN: return WallState.UP;
            default: return WallState.LEFT;
        }
    }

    private static WallState[,] BinaryTreeAlgo(WallState[,] maze, int width, int height)
    {
        Debug.Log(maze.Length);
        Debug.Log(maze[9,9]);
        for (int i = 0; i < width; ++i)
        {
            Debug.Log(i);
            for (int j = 0; j < height; ++j)
            {
                Debug.Log(j);
                var test = new Position { X = i, Y = j };
                var jiran = GetUnvisitedNeighbours(test, maze, width, height);
                List<Neighbour> termsList = new List<Neighbour>();
                if (jiran.Count > 0) ;
                {
                    for (int k = 0; k < jiran.Count; k++)
                    {
                        //Debug.Log(jiran[i].Position.X);
                        //Debug.Log(jiran[i].Position.Y);
                        if (jiran[k].SharedWall == WallState.RIGHT | jiran[k].SharedWall == WallState.UP)
                        {
                            termsList.Add(jiran[k]);
                        }

                    }
                    if (termsList.Count > 0)
                    {
                        int index = Random.Range(0, termsList.Count);
                        Debug.Log("index: " + index);

                        Neighbour randomNeighbour = termsList[index];
                        var nPosition = randomNeighbour.Position;

                        maze[test.X, test.Y] &= ~randomNeighbour.SharedWall;
                        maze[nPosition.X, nPosition.Y] &= ~GetOppositeWall(randomNeighbour.SharedWall);
                        Debug.Log(randomNeighbour);
                    }
                    
                }
              
                
            }
        }

          
        // here we make changes
        

        return maze;
    }

    private static List<Neighbour> GetUnvisitedNeighbours(Position p, WallState[,] maze, int width, int height)
    {
        var list = new List<Neighbour>();

        if (p.X > 0) // left
        {
            if (!maze[p.X - 1, p.Y].HasFlag(WallState.VISITED))
            {
                list.Add(new Neighbour
                {
                    Position = new Position
                    {
                        X = p.X - 1,
                        Y = p.Y
                    },
                    SharedWall = WallState.LEFT
                });
            }
        }

        if (p.Y > 0) // DOWN
        {
            if (!maze[p.X, p.Y - 1].HasFlag(WallState.VISITED))
            {
                list.Add(new Neighbour
                {
                    Position = new Position
                    {
                        X = p.X,
                        Y = p.Y - 1
                    },
                    SharedWall = WallState.DOWN
                });
            }
        }

        if (p.Y < height - 1) // UP
        {
            if (!maze[p.X, p.Y + 1].HasFlag(WallState.VISITED))
            {
                list.Add(new Neighbour
                {
                    Position = new Position
                    {
                        X = p.X,
                        Y = p.Y + 1
                    },
                    SharedWall = WallState.UP
                });
            }
        }

        if (p.X < width - 1) // RIGHT
        {
            if (!maze[p.X + 1, p.Y].HasFlag(WallState.VISITED))
            {
                list.Add(new Neighbour
                {
                    Position = new Position
                    {
                        X = p.X + 1,
                        Y = p.Y
                    },
                    SharedWall = WallState.RIGHT
                });
            }
        }

        return list;
    }

    public static WallState[,] Generate(int width, int height)
    {
        WallState[,] maze = new WallState[width, height];
        WallState initial = WallState.RIGHT | WallState.LEFT | WallState.UP | WallState.DOWN;
        for (int i = 0; i < width; ++i)
        {
            for (int j = 0; j < height; ++j)
            {
                maze[i, j] = initial;  // 1111
            }
        }
        
        return BinaryTreeAlgo(maze, width, height);
    }
}
