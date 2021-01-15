using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public enum WallState
{
    LEFT = 1,
    RIGHT = 2,
    UP = 4,
    DOWN = 8,

    VISITED = 128,

}

public struct Position
{
    public int y;
    public int x;
}

public struct Neighbour
{
    public Position position;
    public WallState SharedWall;
}

public static class MazeGenerator
{
    private static WallState GetOppositeWall(WallState wall)
    {
        switch(wall)
        {
            case WallState.RIGHT: return WallState.LEFT;
            case WallState.LEFT: return WallState.RIGHT;
            case WallState.UP: return WallState.DOWN;
            case WallState.DOWN: return WallState.UP;
            default: return WallState.RIGHT;
        }
    }

    private static WallState[,] RecursiveBackTracker(WallState[,] maze, int width, int height)
    {
        // Randomly choose a starting position
        var rng = new System.Random();
        var positionStack = new Stack<Position>();
        var position = new Position { x = rng.Next(0, width), y = rng.Next(0, height) };

        maze[position.x, position.y] |= WallState.VISITED;
        positionStack.Push(position);

        while(positionStack.Count > 0)
        {
            // Current node
            var current = positionStack.Pop();
            // Find neighbour
            var neighbour = GetUnvisitedNeighbours(current, maze, width, height);

            // Go to random neighbour
            if (neighbour.Count > 0)
            {
                positionStack.Push(current);

                // Get random neighbour
                var ranIndex = rng.Next(0, neighbour.Count);
                Debug.Log("ranIndex: " + ranIndex);

                var randNeighbour = neighbour[ranIndex];
                // Position of the neighbour
                var nPosition = randNeighbour.position;
                // Remove shared wall
                maze[current.x, current.y] &= ~randNeighbour.SharedWall;
                Debug.Log(nPosition.x + " " + nPosition.y);
                maze[nPosition.x, nPosition.y] &= ~GetOppositeWall(randNeighbour.SharedWall);

                // Mark as visited
                maze[nPosition.x, nPosition.y] |= WallState.VISITED;
                positionStack.Push(nPosition);

            }
        }
        return maze;
    }

    // Return all visited neighbour is it has flag or not
    private static List<Neighbour> GetUnvisitedNeighbours(Position p, WallState[,] maze, int width, int height)
    {
        var list = new List<Neighbour>();

        // Check for LEFT Wall
        if (p.x > 0)
        {
            if (!maze[p.x - 1, p.y].HasFlag(WallState.VISITED))
            {
                list.Add(new Neighbour
                {
                    position = new Position
                    {
                        x = p.x - 1,
                        y = p.y
                    },
                    SharedWall = WallState.LEFT
                });
            }
        }

        // Check for DOWN wall
        if (p.y > 0)
        {
            if (!maze[p.x, p.y - 1].HasFlag(WallState.VISITED))
            {
                list.Add(new Neighbour
                {
                    position = new Position
                    {
                        x = p.x,
                        y = p.y - 1
                    },
                    SharedWall = WallState.DOWN
                });
            }
        }

        // Check for UP wall
        if (p.y < height - 1)
        {
            if (!maze[p.x, p.y + 1].HasFlag(WallState.VISITED))
            {
                list.Add(new Neighbour
                {
                    position = new Position
                    {
                        x = p.x,
                        y = p.y + 1
                    },
                    SharedWall = WallState.UP
                });
            }
        }

        // Check for RIGHT wall
        if (p.x < width - 1)
        {
            if (!maze[p.x + 1, p.y].HasFlag(WallState.VISITED))
            {
                list.Add(new Neighbour
                {
                    position = new Position
                    {
                        x = p.x + 1,
                        y = p.y
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
        WallState initial = WallState.RIGHT | WallState.LEFT | WallState.DOWN | WallState.UP;
        for (int i = 0; i < width; ++i)
        {
            for (int j = 0; j < height; ++j)
            {
                maze[i, j] = initial;
            }
        }

        return RecursiveBackTracker(maze, width,height);
    }

}
