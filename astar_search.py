import sys
import matplotlib.pyplot as plt

from queue import PriorityQueue


# Manhattan distance heuristic function
# Defining a heuristic function that calculates the Manhattan distance between two points
def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])



# Defining a helper function to print the maze
def print_maze(maze):
    for row in maze:
        print("".join(row))

# matplot function
def plot_maze1(maze):
    fig, ax = plt.subplots()
    
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == '%':
                ax.add_patch(plt.Rectangle((j, i), 1, 1, facecolor='yellow'))
            elif maze[i][j] == '.':
                ax.add_patch(plt.Rectangle((j, i), 1, 1, facecolor='red',linestyle='dotted'))
            elif maze[i][j] == 'P':
                ax.add_patch(plt.Rectangle((j, i), 1, 1, facecolor='green'))

    
    ax.set_xlim(0, len(maze[0]))
    ax.set_ylim(len(maze), 0)
    ax.set_aspect('equal')
    
    ax.plot([0, 0, len(maze[0]), len(maze[0]), 0], 
            [0, len(maze), len(maze), 0, 0], 
            color='blue', linestyle='dotted')
    plt.show()

# A* search algorithm implementation
def astar(maze, goal_states):
    # Define the start and goal state
    rows, cols = len(maze), len(maze[0])
    start_state = None

    # Find the start and goal state in the maze
    for i in range(rows):
        for j in range(cols):
            if maze[i][j] == "P":
                start_state = (i, j)
                break
            if start_state:
                break
    # Return None if either the starting or goal state were not found
    if start_state is None:
        return None, None, None, None, None

    # Initializing the data structures for A* search
    visited = set()
    border = PriorityQueue()
    g_scores = {start_state: 0}
    f_scores = {start_state: manhattan_distance(start_state, goal_states[0])}
    border.put((f_scores[start_state], start_state, []))
    num_nodes_expanded = 0
    max_tree_depth = 0
    max_border_size = 1
    remaining_goals = set(goal_states)
    all_paths = []

    # Performing A* search
    while not border.empty() and remaining_goals:
        # Get the current node with the lowest f_score from the priority queue
        _, curr_place, path = border.get()
        num_nodes_expanded += 1
        # Return the path if the current node is the goal position
        if curr_place in goal_states:
            remaining_goals.discard(curr_place)
            all_paths.append(path)
            if not remaining_goals:
                return all_paths, len(path), num_nodes_expanded, max_tree_depth, max_border_size


        # Add the current node to the visited set if it has not been visited before
        if curr_place not in visited:
            visited.add(curr_place)
            i, j = curr_place
            # Generate the neighboring nodes of the current node
            for x, y in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
                # Check if the neighboring node is valid and has not been visited before
                if 0 <= x < rows and 0 <= y < cols and maze[x][y] != "%" and (x, y) not in visited:
                    # Calculate the tentative g_score and update it if it is lower than the previous one
                    tentative_g_score = g_scores[curr_place] + 1
                    if (x, y) not in g_scores or tentative_g_score < g_scores[(x, y)]:
                        g_scores[(x, y)] = tentative_g_score
                        # Calculate the f_score and add the neighboring node to the priority queue
                        f_scores[(x, y)] = tentative_g_score + manhattan_distance((x, y), goal_states[0])
                        border.put((f_scores[(x, y)], (x, y), path + [(x, y)]))
                        # Update the maximum fringe size and maximum tree depth
                        max_border_size = max(max_border_size, border.qsize())
                        max_tree_depth = max(max_tree_depth, len(path) + 1)

    # If A* search fails to find a solution, it returns None
    return None, None, num_nodes_expanded, max_tree_depth, max_border_size


# A* search algorithm implementation
def run_astar(file_list):
    for file_name in file_list:
        print('\n')
        with open(file_name, "r") as file:
            maze = [list(line.strip()) for line in file]
        # Find the dimensions of the maze
        rows, cols = len(maze), len(maze[0])

        goal_states = []
        for i in range(rows):
            for j in range(cols):
                if maze[i][j] == ".":
                    goal_states.append((i, j))
        all_paths, path_len, num_nodes_expanded, max_tree_depth, max_border_size = astar(maze, goal_states)

        all_paths, path_len, num_nodes_expanded, max_tree_depth, max_border_size = astar(maze, goal_states)

        if all_paths is None:
            print(f"No path found for {file_name}.")
        else:
            print(f"Path found for {file_name}:")
            print("Path length:", path_len)
            print("Number of nodes expanded:", num_nodes_expanded)
            
            # Mark the visited squares on the path in the maze
            for steps in all_paths:
                for step in steps:
                    if len(step) == 2:
                        i, j = step
                        maze[i][j] = "."
                    else:
                        i = step[0]
                        maze[i][j] = "."

            # Print the updated maze
            print_maze(maze)
            plot_maze1(maze)
            


def main():
    file_list = ['bigMaze.lay', 'openMaze.lay', 'mediumMaze.lay', 'tinySearch.lay', 'trickySearch.lay',
                 'smallSearch.lay']
    run_astar(file_list)


if __name__ == "__main__":
    main()
