## Artifical Intelligence and Applications Coursework
#### By Oscar Klemenz

This is the README for my courserwork. This outlines how to run the search algorithms and important files

### How to run

1. Start by opening your terminal inside of the coursework directory
2. To change which maze to execute within either .py files change the `MAZE_FILENAME` variable within the .py files to the path of your chosen maze (`MAZE_FILENAME` is located on line 10 for both algorithms)
3. Type the command `python3 [FILENAME]`
4. The filename can either be:
    - `dfs.py` for the depth first search
    - `a_star.py` for the A* search 
5. Once the code start running the algorithms will find a path, and output a visual representation of the path, the coordinates of the path itself and some statistics about the execution on the algorithm

Note: 
- Heuristic for A* can be changed within the `heuristic()` function. Default is set to Manhattan.
- On maze large and Vlarge, visual representation of maze may not fit into terminal, making it look a bit messy, however the path is correct

### Files

- `a_star.py` - Implementation of the A* algorithm
- `dfs.py` - Implementation of the depth first algorithm
- `/mazes` - Directory containing mazes used for each of the algorithms
