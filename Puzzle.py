import heapq

# Class representing the state of the puzzle
class PuzzleState:
    def __init__(self, board, parent=None, move=None, depth=0, cost=0):
        self.board = board  # Current board configuration
        self.parent = parent  # Parent state
        self.move = move  # Move taken to reach this state
        self.depth = depth  # Depth of the state in the search tree
        self.cost = cost  # Cost to reach this state

    # Comparison function for the priority queue
    def __lt__(self, other):
        return self.cost < other.cost

    # Function to get neighboring states
    def get_neighbors(self):
        neighbors = []
        zero_index = self.board.index(0)  # Find the empty space
        x, y = zero_index // 3, zero_index % 3  # Get the coordinates of the empty space

        directions = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}  # Possible moves

        for move, (dx, dy) in directions.items():
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3:  # Check if the move is valid
                new_board = self.board[:]
                new_index = nx * 3 + ny
                # Swap the empty space with the new position
                new_board[zero_index], new_board[new_index] = new_board[new_index], new_board[zero_index]
                neighbors.append(PuzzleState(new_board, self, move, self.depth + 1, 0))

        return neighbors


# Function to calculate the Manhattan distance between the current and goal states
def distance(board, goal):
    cost = 0
    for i in range(1, 9):
        xi, yi = divmod(board.index(i), 3)  # Get the current position of the tile
        xg, yg = divmod(goal.index(i), 3)  # Get the goal position of the tile
        cost += abs(xi - xg) + abs(yi - yg)  # Calculate the Manhattan distance
    return cost


# A* search algorithm
def a_star(start, goal):
    opened_list = []  # Priority queue of states to explore
    done = set()  # Set of states already explored
    start_state = PuzzleState(start, cost=distance(start, goal))

    heapq.heappush(opened_list, start_state)  # Add the start state to the priority queue

    while opened_list:
        current = heapq.heappop(opened_list)  # Get the state with the lowest cost

        if current.board == goal:  # Check if the goal state is reached
            return current

        done.add(tuple(current.board))  # Mark the current state as explored

        for neighbor in current.get_neighbors():
            if tuple(neighbor.board) in done:
                continue

            neighbor.cost = neighbor.depth + distance(neighbor.board, goal)  # Calculate the cost of the neighbor
            heapq.heappush(opened_list, neighbor)  # Add the neighbor to the priority queue
    return None


# Function to get the solution path from the start state to the goal state
def get_solution_path(state):
    path = []
    while state:
        path.append((state.move, state.board))
        state = state.parent
    path.reverse()
    return path

