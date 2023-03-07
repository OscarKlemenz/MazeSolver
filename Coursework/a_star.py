import sys, time, math
from queue import PriorityQueue

# Name of file containing the maze
MAZE_FILENAME = 'mazes/maze-Medium.txt'

nodesExplored = 0

def fileToArray():
    '''
    Converts a file to a 2d array

    Return - 2D array representing maze
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


def findStartAndGoal(maze):
    '''
    Finds start and end nodes inside of the 2d array

    maze - 2D array of maze to solve
    Return - start and end locations as coordinates [Y, X]
    '''
    nodes = []

    # Checks along the top of maze
    for i in range(0, len(maze[0])):
        if maze[0][i] == '-':
            # X and Y coord of start/end
            nodes.append((i, 0))
            break
    
    # Search all the way along bottom of maze
    bottom_row = len(maze) - 1
    for i in range(0, len(maze[bottom_row])):
        if maze[bottom_row][i] == '-':
            # X and Y coord of start/end
            nodes.append((i, bottom_row))
            break
    
    # Check left and right
    # Checks the left side of maze
    for i in range(0, len(maze)):
        if maze[i][0] == '-':
            # Y and X coord of start/end
            nodes.append((0, i))
            break
    
    lenOfRows = len(maze[0]) - 1
    for i in range(0, len(maze)):
        if maze[i][lenOfRows] == '-':
            nodes.append((lenOfRows, i))
            break
    
    if len(nodes) != 2:
        print('ERROR: Start and Goal node not found')

    return nodes

def findConnecting(maze, coord):
    '''
    Checks in which directions are available to travel along 
    from a given space in the maze
    '''

    availableNodes = []
    
    xCoord, yCoord = coord

    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        nx, ny = xCoord + dx, yCoord + dy
        if 0 <= ny < len(maze) and 0 <= nx < len(maze[0]) and maze[ny][nx] == '-':
            availableNodes.append((nx, ny))

    return availableNodes

def heurstic(coord, goal):

    xDist = abs(goal[0] - coord[0])
    yDist = abs(goal[1] - coord[1])
    
    # Euclidian without sqrt
    #h = (xDist ** 2) + (yDist ** 2)
    # Euclidian
    #h = math.sqrt((xDist ** 2) + (yDist ** 2))
    # Manhattan
    h = abs(goal[0] - coord[0]) + abs(goal[1] - coord[1])

    return h


def findAllNodes(maze):
    """
    Finds all the coordinates of dashes in the maze
    """

    nodes = []

    for y in range(0, len(maze)):
        for x in range(0, len(maze[y])):
            if maze[y][x] == '-':
                nodes.append((x, y))
    
    return nodes

def reconstructPath(cameFrom, current):
    """
    Reonstructs the path of the algorithm from start to finish
    """

    totalPath = [current]
    while current in cameFrom.keys():
        current = cameFrom[current]
        totalPath.insert(0, current)
    
    return totalPath

def visualisePath(maze, path):
    '''
    Visualises the path the search has taken
    '''

    # Reset the maze to original
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] == 'V':
                maze[y][x] = '-'

    # For each coordinate in path a p is placed
    for coord in path:
        maze[coord[1]][coord[0]] = 'P'

    # Outputs the maze
    printMaze(maze)

def aStar(maze, start, goal):
    '''
    A Star Searches the maze

    '''
    global nodesExplored
    # Priority queue
    openSet = PriorityQueue()
    openSet.put((0, start))
    # Came from contains adjacent node with the cheapest path
    cameFrom = {}

    # For all nodes populate them in dictionary with infinity value for g and f score
    gScore = {}
    fScore = {}
    nodes = findAllNodes(maze)
    
    # Sets all initial scores to infinity
    for node in nodes:
        gScore[node] = math.inf
        fScore[node] = math.inf

    # Initialises the start node
    gScore[start] = 0
    fScore[start] = heurstic(start, goal)

    while openSet.qsize() > 0:
        # Gets the node with smallest f value
        current = openSet.get()[1]
        # Checks if it is the goal
        if current == goal:
            return reconstructPath(cameFrom, current)
        
        # Gets all adjacent nodes
        neighbours = findConnecting(maze, current)
        # Checks all nodes 
        for node in neighbours:
            # g is +1 for each node
            tempGScore = gScore[current] + 1
            # Checks if new g is smaller than old g
            if tempGScore < gScore[node]:
                cameFrom[node] = current
                gScore[node] = tempGScore
                fScore[node] = tempGScore + heurstic(node, goal)
                # Adds node to priority queue
                if node not in (x[1] for x in openSet.queue):
                    nodesExplored += 1
                    openSet.put((fScore[node], node))
    
    return None

def aStarWithStats(maze, start, goal):
    '''
    Performs a dfs and produces statistics about it
    '''

    startTime = time.time()

    path = aStar(maze, start, goal)

    endTime = time.time()

    global nodesExplored

    visualisePath(maze, path)

    # Outputs stats
    print('===STATISTICS===')
    print('Nodes explored: ' )
    print(nodesExplored)
    print('Time: ' )
    print("{:.6f}".format(endTime-startTime))
    print('Steps in path: ')
    print(len(path))


def printMaze(maze):
    '''
    Outputs the maze with some formatting
    '''

    for line in maze:
        print((' ').join(line))
    print('\n')


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


    aStarWithStats(maze, start, goal)

    '''
    - Construct a dictionary, each coord has an array of coordinates its connected to 
    '''

if __name__ == "__main__":
    main()