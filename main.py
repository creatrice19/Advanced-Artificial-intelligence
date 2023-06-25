# working for tinysearch
import sys
import matplotlib.pyplot as plt
from collections import deque

from astar_search import *

# Function to read a maze from the given file
def read_maze(filename):
    with open(filename) as file:
        maze = [[char for char in line.strip()] for line in file]
    return maze

class State:
    def __init__(self, coordinates, path):
        self.coordinates = coordinates
        self.path = path


# Function to visualize the solution path in the maze
def visualize_solution(maze, path):
    for i, j in path:
        maze[i][j] = '.'
    for row in maze:
        print(' '.join(row))
    print()


# Breadth-first search algorithm implementation
def bfs(maze):
    # Defining the start state
    rows, cols = len(maze), len(maze[0])
    start_state = None
    goal_states = []

    for i, row in enumerate(maze):
        for j, char in enumerate(row):
            if char == "P":
                start_state = State((i, j),[])
            elif char == ".":
                goal_state = State((i, j),[])
                goal_states.append(goal_state)

    if start_state is None or not goal_states:
        return None, None, None, None, None

    # Initializing the data structures for Breadth-first search
    visited = set()
    border = deque()
    border.append(start_state)
    num_nodes_expanded = 0
    max_tree_depth = 0
    max_border_size = 1
    all_paths = []

    # Performing Breadth-first search
    while border:
        curr_state = border.popleft()
        num_nodes_expanded += 1

        for goal_state in goal_states[:]:
            if curr_state.coordinates == goal_state.coordinates:
                goal_states.remove(goal_state)  # Remove the goal state from the list once reached
                all_paths.append(curr_state.path) # Append the path to all_paths
                if not goal_states:  # Check if all goal states have been reached
                    return all_paths, len(curr_state.path), num_nodes_expanded, max_tree_depth, max_border_size
                
        if curr_state.coordinates not in visited:
            visited.add(curr_state.coordinates)
            i, j = curr_state.coordinates
            for x, y in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
                if 0 <= x < rows and 0 <= y < cols and maze[x][y] != "%" and (x, y) not in visited:
                    new_state = State((x, y), curr_state.path + [(x, y)])
                    border.append(new_state)
                    max_border_size = max(max_border_size, len(border))
            max_tree_depth = max(max_tree_depth, len(curr_state.path))

    # If BFS fails to find a solution, it returns None
    return None, None, num_nodes_expanded, max_tree_depth, max_border_size

# matplot function
def plot_maze1(maze):
    fig, ax = plt.subplots()
    
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == '%':
                ax.add_patch(plt.Rectangle((j, i), 1, 1, facecolor='yellow'))
            elif maze[i][j] == 'P':
                ax.add_patch(plt.Rectangle((j, i), 1, 1, facecolor='green'))
            elif maze[i][j] == '.':
                ax.add_patch(plt.Rectangle((j, i), 1, 1, facecolor='red',linestyle='dotted'))
            
     
    
    ax.set_xlim(0, len(maze[0]))
    ax.set_ylim(len(maze), 0)
    ax.set_aspect('equal')
    
    ax.plot([0, 0, len(maze[0]), len(maze[0]), 0], 
            [0, len(maze), len(maze), 0, 0], 
            color='blue', linestyle='dotted')
    plt.show()

# Main function to run BFS on a given maze and writing output to a file
def run_bfs():
    file_names = ['smallMaze.lay', 'mediumMaze.lay', 'bigMaze.lay', 'openMaze.lay','tinySearch.lay', 'trickySearch.lay','smallSearch.lay']
    for file in file_names:
        print('\n')
        maze = read_maze(file)
        all_paths, path_cost, num_nodes_expanded, max_tree_depth, max_border_size = bfs(maze)
        if all_paths is not None:
            print("BFS solution:", file, "with path cost of", path_cost)
            print("Number of nodes expanded:", num_nodes_expanded)
            print("Maximum tree depth searched:", max_tree_depth)
            print("Maximum size of the fringe:", max_border_size)
            print("Visualizing solution:")
            for path in all_paths:
                visualize_solution(maze, path)
            plot_maze1(maze)
        else:
            print("BFS failed to find a solution", file=sys.stderr)


if __name__ == "__main__":
    print('=' * 130)
    print("starting Breadth-first search (BFS)...")
    print('=' * 130)
    run_bfs()
    print('=' * 130)
    print("starting A* search...")
    print('=' * 130)
    main()