# seekers_maze
# SEEKERS MAZE

## Overview
SEEKERS MAZE is a Python-based maze-solving game built using the Tkinter GUI framework. The game generates a random maze using Prim's algorithm and allows an animated agent to navigate the maze, exploring different paths and finding the optimal route.

## Features
- **Random Maze Generation**: Uses Prim's algorithm to generate a new maze layout each time.
- **Animated Agent**: A graphical agent moves through the maze.
- **Pathfinding Algorithm**: Uses depth-first search (DFS) to find all possible paths.
- **Optimal Path Highlighting**: Identifies and displays the shortest path from start to end.
- **User Controls**:
  - Adjust animation speed.
  - Generate a new maze.
  - Start/stop pathfinding animation.
  - Show the optimal path.

## Installation
### Prerequisites
- Python 3.x
- Tkinter (included in standard Python installation)
- NumPy (for matrix operations)

### Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/seekers-maze.git
   cd seekers-maze
   ```
2. Install dependencies:
   ```sh
   pip install numpy
   ```
3. Run the game:
   ```sh
   python maze_game.py
   ```

## How to Play
- **New Maze**: Generates a new maze layout.
- **Find All Paths**: Starts an animation showing all valid paths from start to end.
- **Stop Animation**: Stops the current animation.
- **Show Optimal Path**: Highlights the shortest path to the exit.
- **Speed Control**: Adjust the animation speed using the slider.

## Code Structure
```
seekers-maze/
│-- maze_game.py    # Main game script
│-- README.md       # Documentation
```

## Contributing
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Create a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Maze generation inspired by Prim's algorithm.
- Tkinter for GUI development.
- NumPy for matrix-based operations.

Enjoy playing SEEKERS MAZE!

