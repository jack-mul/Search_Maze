# Search_Maze
A search algorithm that takes in a maze in the form of a text file and finds the solution to the maze using Depth-First Search or Breadth-First Search, depending on which search type the user prefers.

The following is a breakdown of the Python script's functionality:

# Classes:
## Node:
- Represents a single state in the maze exploration process. It holds information about:
- state: The current position (row, column) within the maze.
- parent: The previous Node leading to this state (used for reconstructing the solution path).
- action: The action taken to reach this state from the parent (e.g., "up", "down", etc.).

## StackFrontier/QueueFrontier:
- These classes represent a frontier, which is a data structure used to manage the order in which states are explored during the maze solving algorithm.
- StackFrontier: Implements a Last-In-First-Out (LIFO) behavior, similar to a stack. It prioritizes recently explored states.
- QueueFrontier: Implements a First-In-First-Out (FIFO) behavior, similar to a queue. It explores states in the order they were added.

## Maze:
- Handles loading and representing the maze structure from a text file.
- It also contains functions to solve the maze and visualize the solution.

# Functions
## init(self, filename):
- This constructor (special method) of the Maze class is called when creating a Maze object. It takes a filename as input and performs the following tasks:
  - Reads the maze contents from the file.
  - Validates that there's exactly one starting point ("A") and one goal point ("B").
  - Determines the height and width of the maze based on the file contents.
  - Creates a 2D list (self.walls) to represent the maze, where True indicates a wall and False indicates an empty space.
  - Stores the starting and goal positions within the maze.

## print(self):
- Prints a text representation of the maze, including walls, the starting point ("A"), the goal point ("B"), and the solution path (marked with asterisks "*") if available.

## neighbors(self, state):
- Given a current position (state), this function identifies all valid neighboring positions (up, down, left, right) that are not blocked by walls.
- It returns a list of tuples, where each tuple contains the action ("up", "down", etc.) needed to move to that neighbor and the neighbor's coordinates.

## solve(self):
- This function implements the core maze solving logic.
- It uses a Depth-First Search (DFS) algorithm with a StackFrontier by default (can be swapped to Breadth-First Search with QueueFrontier).
- Here's a simplified explanation of the steps:
  - Initializes a frontier with only the starting position as a Node.
  - Iterates until a solution is found or the frontier becomes empty.
  - In each iteration, it removes a Node from the frontier (prioritizing recently explored states with DFS).
  - Checks if the removed Node's position is the goal. If so, it backtracks through the parent Nodes to reconstruct the solution path and returns.
  - Marks the current Node's position as explored to avoid revisiting it.
  - Explores all valid neighbors of the current Node and adds them as new Nodes to the frontier if they haven't been explored yet.
 
## output_image(self, filename, show_solution=True, show_explored=False):
- This function (optional) generates a visual representation of the maze and solution path as a PNG image file.
- It takes arguments for the filename, whether to show the solution path, and whether to show explored states.

# Use
The script is run from the the command line using the following syntax:
python maze.py maze.txt

In short, when run the script will:
The script will:
- Read the maze file and build a maze object.
- Print the initial maze text representation.
- Solve the maze using the chosen frontier (StackFrontier by default).
- Print the number of states explored during the search.
- Print the maze again with the solution path highlighted.
- Generate a PNG image visualization of the maze solution (optional).
