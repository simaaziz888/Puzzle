from flask import Flask, request, jsonify
from Puzzle import PuzzleState, a_star, get_solution_path

# Initialize Flask application
name = '__name__'
app = Flask(name, static_folder='static', static_url_path='')

# Route for the main page
@app.route('/')
def index():
    return app.send_static_file('index.html')  # Serve the static HTML file

# Route to solve the puzzle
@app.route('/solve', methods=['POST'])
def solve():
    data = request.get_json()  # Get the JSON data from the request
    initial_state = list(map(int, data['initialState'].split()))  # Convert initial state to list of integers
    goal_state = list(map(int, data['goalState'].split()))  # Convert goal state to list of integers
    solution = a_star(initial_state, goal_state)  # Find the solution using A* algorithm

    if solution:
        solution_path = get_solution_path(solution)  # Get the solution path
        # Create a list of steps to describe the solution
        steps = [f'Move: {move}, State: {state}' for move, state in solution_path]
        return jsonify(result=steps)  # Return the solution steps as JSON
    else:
        return jsonify(result=["No Solution Found"])  # Return if no solution is found

# Run the Flask application
if name == '__main__':
    app.run(debug=True)  # Enable debug mode for better error messages
