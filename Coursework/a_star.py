import sys, time, math
from queue import PriorityQueue

# Name of file containing the maze
MAZE_FILENAME = 'mazes/maze-VLarge.txt'

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

def findConnecting(maze, coord):
    '''
    Checks in which directions are available to travel along 
    from a given space in the maze
    '''


    availableNodes = []
    
    yCoord = coord[0]
    xCoord = coord[1]

    # For all of these conditionals an additonal check is made, for the case when
    # we are checking a start or goal node
    if (yCoord < (len(maze)-1)):
        if maze[yCoord + 1][xCoord] == '-':
            availableNodes.append([yCoord+1,xCoord])
        
    if(yCoord > 0):  
        if maze[yCoord - 1][xCoord] == '-':
            availableNodes.append([yCoord-1,xCoord])

    if(xCoord < (len(maze[0])-1)):
        if maze[yCoord][xCoord + 1] == '-':
            availableNodes.append([yCoord,xCoord + 1])

    if(xCoord > 0):
        if maze[yCoord][xCoord - 1] == '-':
            availableNodes.append([yCoord,xCoord-1])

    return availableNodes

def heurstic(coord, goal):

    xDist = abs(goal[1] - coord[1])
    yDist = abs(goal[0] - coord[0])
    
    h = math.sqrt((xDist ** 2) + (yDist ** 2))

    return h

def aStar(maze, start, goal):
    '''
    A Star Searches the maze

    CURRENT ISSUE: start node needs to be added to list of nodes
    '''

    # Sets node to visited
    maze[start[0]][start[1]] = 'V'
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
            
            path = aStar(maze, node, goal)
            # If path has been found path coords are created
            if (path != None):
                if node not in path:
                    path.insert(0, node)
                return path

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

    '''
    TO HAVE:

    - Function will need an g that holds the current cost
    - h that holds the heuristic for new nodes
    - f that is the sum  of the two

    - COULD POSSIBLY DO EUCLIDIAN, with/without sqrt, Manhattan
    
    Non-Recursive algorithm,
        - Create priority queue
        - f score dictionary for each coord
        - g score dictionary for each coord

    '''

if __name__ == "__main__":
    main()