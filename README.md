# Maze Generation using DFS in Python

This project demonstrates how to generate a maze using the Depth-First Search (DFS) algorithm in Python. The maze is represented as a grid, where walls and paths are created based on the DFS traversal.

## Table of Contents

-   [Introduction](#introduction)
-   [Installation](#installation)
-   [Usage](#usage)
-   [Code Explanation](#code-explanation)
-   [License](#license)

## Introduction

The Depth-First Search (DFS) algorithm is a fundamental graph traversal technique that can be used to generate mazes. By treating the maze as a grid and performing a DFS traversal, we can carve out a path from the starting point to the ending point, creating a solvable maze.

## Installation

1.  Make sure you have Python installed. You can download it from [python.org](https://www.python.org/).
    
2.  Clone this repository or download the source code.
    
3.  Install any required libraries (if any) using pip:
    
    bash
    
    Sao chép mã
    
    `pip install -r requirements.txt` 
    

## Usage

To generate a maze, simply run the script `generate_maze.py`. You can specify the dimensions of the maze as command-line arguments:

bash

Sao chép mã

`python generate_maze.py <width> <height>` 

For example, to generate a 20x20 maze:

bash

Sao chép mã

`python generate_maze.py 20 20` 

## Code Explanation

Here's a brief explanation of the code:

1.  **Importing Libraries**: We import the necessary libraries such as `random` and `sys`.
    
2.  **Maze Initialization**: We initialize the maze with walls and create a grid where each cell can be visited.
    
3.  **DFS Algorithm**: We implement the DFS algorithm to carve paths in the maze. The algorithm starts from a random cell, marks it as visited, and recursively visits its unvisited neighbors, removing walls between adjacent cells.
    
4.  **Displaying the Maze**: After generating the maze, we print it to the console in a readable format.
    

Here is the complete code for `generate_maze.py`:

python

Sao chép mã

`import random
import sys

# Directions for moving in the grid (up, down, left, right)
DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]

def initialize_maze(width, height):
    """ Initialize the maze with walls """
    maze = [['#'] * (width * 2 + 1) for _ in range(height * 2 + 1)]
    for y in range(1, height * 2, 2):
        for x in range(1, width * 2, 2):
            maze[y][x] = ' '
    return maze

def print_maze(maze):
    """ Print the maze to the console """
    for row in maze:
        print(''.join(row))

def dfs(maze, x, y):
    """ Perform DFS to generate the maze """
    directions = DIRECTIONS[:]
    random.shuffle(directions)
    for dx, dy in directions:
        nx, ny = x + dx * 2, y + dy * 2
        if 1 <= nx < len(maze[0]) - 1 and 1 <= ny < len(maze) - 1 and maze[ny][nx] == '#':
            maze[ny - dy][nx - dx] = ' '
            maze[ny][nx] = ' '
            dfs(maze, nx, ny)

def generate_maze(width, height):
    maze = initialize_maze(width, height)
    start_x, start_y = 1, 1
    maze[start_y][start_x] = ' '
    dfs(maze, start_x, start_y)
    return maze

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python generate_maze.py <width> <height>")
        sys.exit(1)
    width = int(sys.argv[1])
    height = int(sys.argv[2])
    maze = generate_maze(width, height)
    print_maze(maze)` 

## License

This project is licensed under the MIT License.

* * *

Bạn có thể lưu nội dung này vào file `README.md` trong thư mục dự án của bạn. Nếu có bất kỳ câu hỏi hoặc cần thêm hỗ trợ, hãy cho mình biết!
