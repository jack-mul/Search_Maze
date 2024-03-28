import sys

# Creating "Node" that keeps track of the state, parent, and action
# In this case we aren't keeping track of a path cost yet
class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier():
    # Function to create a frontier that will be represented as a list (initially empty)
    def __init__(self):
        self.frontier = []
    # Function that adds something to the frontier by appending it to the end of the list
    def add(self, node):
        self.frontier.append(node)
    # Function that checks if the frontier contains a particular state
    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)
    # Function that checks if the frontier is empty
    def empty(self):
        return len(self.frontier) == 0
    # Function that removes something from the frontier
    def remove(self):
        # Can't remove something if the frontier's empty, so check that first
        if self.empty():
            raise Exception("empty frontier")
        # Because we're implementing a Stack (last-in first-out) method, we have to remove the last-in item of the list (hence the -1)
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1] # Update frontier to remove that node
            return node

# Alternative version of StackFrontier that inherits from StackFrontier
# Meaning it will do everything StackFrontier does, unless functions are redefined
class QueueFrontier(StackFrontier):
    # Redefining the way we remove a frontier
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        # Because we're implementing a Queue (first-in first-out) method, we have to remove the first-in item of the list
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

# Class will handle the process of taking a maze as a text file and figuring out how to solve it
class Maze():

    def __init__(self, filename):

        # Read file and set height and width of maze
        with open(filename) as f:
            contents = f.read()

        # Ensure only one start and goal in maze
        if contents.count("A") != 1:
            raise Exception("maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("maze must have exactly one goal")

        # Determine height and width of maze
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # Keep track of walls
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None


    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()


    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result

    # Finds a solution to maze, if one exists
    def solve(self):
        # Keep track of number of states explored
        self.num_explored = 0
        # Initialize frontier to just the starting position
        start = Node(state=self.start, parent=None, action=None)
        # Start with a frontier as a Stack - Using DFS algorithm
        frontier = StackFrontier()
        # Initially the frontier will just contain the start state
        frontier.add(start)
        # Initialize an empty explored set
        self.explored = set()

        # Loop that keeps going until solution is found
        while True:
            # If nothing left in frontier, then no path
            if frontier.empty():
                raise Exception("no solution")

            # Choose a node from the frontier
            node = frontier.remove()
            # Update the number of states explored
            self.num_explored += 1

            # If node is the goal, then we have a solution
            if node.state == self.goal:
                # The goal has been found, we want to keep track of how we got there
                # Making an empty list to store the correct actions we made
                actions = []
                # Making an empty list to store the correct cells we passed
                cells = []
                
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return

            # Mark node as explored
            self.explored.add(node.state)

            # Add neighbors to frontier
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)


    def output_image(self, filename, show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw
        cell_size = 50
        cell_border = 2

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):

                # Walls
                if col:
                    fill = (40, 40, 40)

                # Start
                elif (i, j) == self.start:
                    fill = (255, 0, 0)

                # Goal
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)

                # Solution
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)

                # Explored
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)

                # Empty cell
                else:
                    fill = (237, 240, 252)

                # Draw cell
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )

        img.save(filename)


if len(sys.argv) != 2:
    sys.exit("Usage: python maze.py maze.txt")

m = Maze(sys.argv[1])
print("Maze:")
m.print()
print("Solving...")
m.solve()
print("States Explored:", m.num_explored)
print("Solution:")
m.print()
m.output_image("maze.png", show_explored=True)
