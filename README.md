# Labyrinth Solver

This is the solution to the Damavis Data Engineer Challenge 2023 by Álvaro Videgain Barranco. It includes a Python code implementation of a labyrinth solver. The code takes a nested list representation of a labyrinth and finds the minimum number of steps required to move a rod from the top left corner to the bottom right corner of the labyrinth, considering certain movement and rotation rules which are specified in the challenge instructions.

## Dependencies

No external dependencies are needed. The code was developed and tested in Python 3.10.7.

## Labyrinth Representation

The labyrinth is internally represented using three main data classes:

### `Coordinates`

- Represents the position of a cell in the labyrinth grid.
- Contains `x` and `y` coordinates, starting from zero.
- `x` increases when moving to the right, and `y` increases when moving down.

### `RodState`

- Represents the position and orientation of the rod in the labyrinth.
- Contains a `pos` field of type `Coordinates` representing the current position of its center.
- Contains an `orientation` field of type `Orientation` representing the current orientation of the rod.
- The `Orientation` enumeration defines two possible values: `HORIZONTAL` and `VERTICAL`.

### `LabyrinthState`

- Represents the entire system state.
- Contains the size of the labyrinth (`n_rows` and `n_cols`).
- Contains a `walls` field, which is a tuple of `Coordinates` representing the positions of walls in the labyrinth.
- Contains a `rod` field of type `RodState`, representing the state of the rod.
- Contains a `steps` field representing the number of steps taken to reach the current state.

A custom exception is raised when the labyrinth is not valid: `InvalidLabyrinthError`.

## Input parsing

The `labyrinth_parser()` function takes the raw labyrinth representation and converts it into a `LabyrinthState` object. It validates the input labyrinth using `validate_lab()` that performs various checks to validate the labyrinth's size, shape, characters, and initial state.

## Solving algorithm

The `solve_labyrinth()` function implements a breadth-first search algorithm to find the minimum number of steps required to reach the bottom right corner of the labyrinth. It starts from the initial state and follows this steps, finding new states to explore:

1. Check if the current state has already been explored, if this is the case, it jumps to the next iteration. In order to track the explored states the list `visited` is used.

2. Find all the potential positions to be reached from the current states and adds them to the states to explore. For this purpose, the function `get_valid_moves()` is used, which takes into account the movement and rotation rules.

3. Check if the bottom right corner has been reached, in this case return the number of steps required to reach it. The number of steps are stored in the field `steps` of `LabyrinthState`.

4. if the bottom right corner has not been reached, explore the next state in a new iteration. As a breadth-first search algorithm is being used, the states to be explored are accessed following a first in, first out (FIFO) method, which is implemented using a Python `collections.deque`.

5. When there are no states left to be explored, return -1 as the labyrinth can not be solved.

## Usage

The file `LabyrinthSearch.py` contains the solution logic. To use the labyrinth solver, call `min_dist_lab()` and pass in the nested list representation of the labyrinth. It will return the minimum number of steps required to solve the labyrinth, -1 if it is not possible to solve it or raise a `InvalidLabyrinthError` if the labyrinth input is invalid.

## Testing

The file `TestLabyrinth.py` contains a set of unit tests to verify the correctness of the labyrinth solver. The test cases cover different scenarios, including solvable labyrinths, unsolvable labyrinths, and invalid inputs. In order to not use external frameworks, the standard library `unittest` module is used, instead of other options, such as `pytest`.

