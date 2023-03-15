"""
Implementation of the depth first algorithm to find a
solution to the maze.

Author: Oscar Klemenz
"""
import sys, time

# Name of file containing the maze
MAZE_FILENAME = 'mazes/maze-Easy.txt'
# Counter for statistics
nodesExplored = 0

def fileToArray() -> list:
    '''
    Converts a file to a 2d array

    Returns: 
        Lines - 2D array representing maze
    '''

    lines = []
    with open(MAZE_FILENAME) as textFile:
        for line in textFile:
            newLine = line.split(' ')
            # Removes line breaks from file
            if '\n' in newLine:
                newLine.remove('\n')
            if '#\n' in newLine:
                newLine[newLine.index('#\n')] = '#'
            # Checks that the array is not empty
            if len(newLine) > 0:
                lines.append(newLine)
    
    return lines


def findStartAndGoal(maze) -> list:
    '''
    Finds start and end nodes inside of the 2d array

    Args: 
        maze - 2D array of maze to solve
    Returns: 
        nodes - start and end locations as coordinates [Y, X]
    '''
    nodes = []

    # Checks along the top of maze
    for i in range(0, len(maze[0])):
        if maze[0][i] == '-':
            # Y and X coord of start/end
            nodes.append([0, i])
            break
    
    # Search all the way along bottom of maze
    bottom_row = len(maze) - 1
    for i in range(0, len(maze[bottom_row])):
        if maze[bottom_row][i] == '-':
            # Y and X coord of start/end
            nodes.append([bottom_row, i])
            break
    
    # Check left and right
    # Checks the left side of maze
    for i in range(0, len(maze)):
        if maze[i][0] == '-':
            # Y and X coord of start/end
            nodes.append([i, 0])
            break
    
    lenOfRows = len(maze[0]) - 1
    for i in range(0, len(maze)):
        if maze[i][lenOfRows] == '-':
            nodes.append([i, lenOfRows])
            break
    
    if len(nodes) != 2:
        print('ERROR: Start and Goal node not found')

    return nodes

def printMaze(maze):
    '''
    Outputs the maze with some formatting

    Args:
        maze - 2D array representing the maze
    '''

    for line in maze:
        print((' ').join(line))
    print('\n')

def findConnecting(maze, coord) -> list:
    '''
    Checks which directions are available to travel along 
    from a given space in the maze

    Args:
        maze - 2D array representing maze
        coord - Node which we are finding neighbours for
    Returns:
        availableNodes - Neighbour nodes of the inputed node
    '''

    availableNodes = []
    
    yCoord, xCoord = coord

    for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        ny, nx = yCoord + dy, xCoord + dx
        if 0 <= ny < len(maze) and 0 <= nx < len(maze[0]) and maze[ny][nx] == '-':
            availableNodes.append([ny, nx])

    return availableNodes

def visualisePath(maze, path):
    '''
    Visualises the path the search has taken

    Args:
        maze - 2D array representing the maze
        path - Coordinates of the path through the maze
    '''

    # Reset the maze to original
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] == 'V':
                maze[y][x] = '-'

    # For each coordinate in path a p is placed
    for coord in path:
        maze[coord[0]][coord[1]] = 'P'

    # Outputs the maze
    printMaze(maze)

def dfs(maze, start, goal) -> list:
    '''
    Depth first searches the maze

    Args:
        maze - 2D array representing the maze
        start - Node which the search is starting at
        end - Node which the search is ending at
    Returns:
        The path through the given maze
    '''

    # Sets node to visited
    maze[start[0]][start[1]] = 'V'
    global nodesExplored
    nodesExplored = nodesExplored + 1
    # Checks if it is the goal
    if (start == goal):
        return [goal]
    # Finds all connecting nodes
    available = findConnecting(maze, start)
    # If dead end then wrong path
    if(available == 0):
        return None
    else:
        # Calls dfs on all other nodes
        for node in available:
            
            path = dfs(maze, node, goal)
            # If path has been found path coords are created
            if (path != None):
                if node not in path:
                    path.insert(0, node)
                return path

def dfsWithStats(maze, start, goal):
    '''
    Performs an depth first search and produces statistics about it

    Args:
        maze - 2D array representing the maze
        start - Node which the search is starting at
        end - Node which the search is ending at
    Returns:
        The path through the given maze with additional statistics
    '''


    # Starts recording time
    startTime = time.time()

    path = dfs(maze, start, goal)

    endTime = time.time()

    global nodesExplored
    # Adds the start node to the path
    path.insert(0, start)
    visualisePath(maze, path)
    print(path)
    print("Note: Each coordinate is layed out (y,x)\n")
    # Outputs stats
    print('===STATISTICS===')
    print('Nodes explored: ' )
    print(nodesExplored)
    print('Time: ' )
    print("{:.6f}".format(endTime-startTime))
    print('Steps in path: ')
    print(len(path))

def main():
    
    # Converts maze file into a 2D array
    maze = fileToArray()

    # Sets recursion depth
    maxNodes = len(maze) * len(maze[0])
    sys.setrecursionlimit(maxNodes)

    # Finds start and goal coords
    nodes = findStartAndGoal(maze)
    start = nodes[0]
    goal = nodes[1]

    dfsWithStats(maze, start, goal)

if __name__ == "__main__":
    main()