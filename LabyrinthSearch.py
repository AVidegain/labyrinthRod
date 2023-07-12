from dataclasses import dataclass, replace
from enum import Enum


class Orientation(Enum):
    HORIZONTAL = "h"
    VERTICAL = "v"


@dataclass
class Coordinates:
    """Position in the labyrinth. Both `x` and `y` start at zero. `x` grows as you move
    to the right and `y` grows as you move down.
    """

    x: int
    y: int


@dataclass
class LabyrinthState:
    """Dataclass representing the entire system. `n_rows` and `n_cols` indicate the
    labyrinth size, `walls` indicate where there are obstacles in the labyrinth,
    `rod_pos` and `rod_orientation` indicate the state of the rod and steps contains the
    number of steps that were required to reach a given state.
    """

    n_rows: int
    n_cols: int
    walls: list[Coordinates]
    rod_pos: Coordinates
    rod_orientation: Orientation
    steps: int


def val_lab(raw_labyrinth: list[list[str]]) -> bool:
    """Checks that the input represents a valid labyrinth.

    Args:
        raw_labyrinth (list[list[str]]): Input strings.

    Returns:
        bool: Whether or not the input is valid.
    """

    # Check number of rows.
    try:
        if len(raw_labyrinth) not in range(3, 1001):
            return False

    except TypeError:
        return False

    # Check number of columns.
    try:
        if len(raw_labyrinth[0]) not in range(3, 1001):
            return False

    except TypeError:
        return False

    # Check that it is a rectangle.
    try:
        for row in raw_labyrinth:
            if len(row) != len(raw_labyrinth[0]):
                return False
    except TypeError:
        return False

    # Check for unallowed characters.
    for row in raw_labyrinth:
        for element in row:
            if element not in (".", "#"):
                return False

    # Check that the is enough space for the initial state.
    if any(raw_labyrinth[0][i] == "#" for i in range(3)):
        return False

    return True


def get_valid_moves(state: LabyrinthState) -> list[LabyrinthState]:
    """Get all the states that can be reached from a given state.

    Args:
        state (LabyrinthState): Parent state.

    Returns:
        list[LabyrinthState]: Child states.
    """
    valid_moves = []

    if state.rod_orientation is Orientation.HORIZONTAL:
        # Move to the right.
        right_spot = Coordinates(state.rod_pos.x + 2, state.rod_pos.y)
        if right_spot.x < state.n_cols - 1 and right_spot not in state.walls:
            move = replace(
                state,
                rod_pos=Coordinates(state.rod_pos.x + 1, state.rod_pos.y),
                steps=state.steps + 1,
            )
            valid_moves.append(move)

        # Move to the left.
        left_spot = Coordinates(state.rod_pos.x - 2, state.rod_pos.y)
        if left_spot.x > 0 and left_spot not in state.walls:
            move = replace(
                state,
                rod_pos=Coordinates(state.rod_pos.x - 1, state.rod_pos.y),
                steps=state.steps + 1,
            )
            valid_moves.append(move)

        # Move up.
        above_spots = [
            Coordinates(state.rod_pos.x + i, state.rod_pos.y - 1) for i in range(-1, 2)
        ]
        if all(spot.y > 0 and spot not in state.walls for spot in above_spots):
            move = replace(
                state,
                rod_pos=Coordinates(state.rod_pos.x, state.rod_pos.y - 1),
                steps=state.steps + 1,
            )
            valid_moves.append(move)

        # Move down.
        below_spots = [
            Coordinates(state.rod_pos.x + i, state.rod_pos.y + 1) for i in range(-1, 2)
        ]
        if all(
            spot.y < state.n_rows - 1 and spot not in state.walls
            for spot in below_spots
        ):
            move = replace(
                state,
                rod_pos=Coordinates(state.rod_pos.x, state.rod_pos.y + 1),
                steps=state.steps + 1,
            )
            valid_moves.append(move)

        # Rotate.
        if (
            all(spot.y > 0 for spot in above_spots)
            and all(spot.y < state.n_rows - 1 for spot in below_spots)
            and all(spot not in state.walls for spot in above_spots + below_spots)
        ):
            move = replace(
                state,
                rod_orientation=Orientation.VERTICAL,
                steps=state.steps + 1,
            )
            valid_moves.append(move)

    # Vertical orientation.
    else:
        # Move to the right.
        right_spots = [
            Coordinates(state.rod_pos.x + 1, state.rod_pos.y + i) for i in range(-1, 2)
        ]
        if all(
            spot.x < state.n_cols - 1 and spot not in state.walls
            for spot in right_spots
        ):
            move = replace(
                state,
                rod_pos=Coordinates(state.rod_pos.x + 1, state.rod_pos.y),
                steps=state.steps + 1,
            )
            valid_moves.append(move)

        # Move to the left.
        left_spots = [
            Coordinates(state.rod_pos.x - 1, state.rod_pos.y + i) for i in range(-1, 2)
        ]
        if all(spot.x > 0 and spot not in state.walls for spot in left_spots):
            move = replace(
                state,
                rod_pos=Coordinates(state.rod_pos.x - 1, state.rod_pos.y),
                steps=state.steps + 1,
            )
            valid_moves.append(move)

        # Move up.
        above_spot = Coordinates(state.rod_pos.x, state.rod_pos.y - 2)
        if above_spot.y > 0 and above_spot not in state.walls:
            move = replace(
                state,
                rod_pos=Coordinates(state.rod_pos.x, state.rod_pos.y - 1),
                steps=state.steps + 1,
            )
            valid_moves.append(move)

        # Move down.
        below_spot = Coordinates(state.rod_pos.x, state.rod_pos.y + 2)
        if below_spot.y < state.n_rows - 1 and below_spot not in state.walls:
            move = replace(
                state,
                rod_pos=Coordinates(state.rod_pos.x, state.rod_pos.y + 1),
                steps=state.steps + 1,
            )
            valid_moves.append(move)

        # Rotate.
        if (
            all(spot.y > 0 for spot in right_spots)
            and all(spot.y < state.n_rows - 1 for spot in left_spots)
            and all(spot not in state.walls for spot in right_spots + left_spots)
        ):
            move = replace(
                state,
                rod_orientation=Orientation.HORIZONTAL,
                steps=state.steps + 1,
            )
            valid_moves.append(move)

    return valid_moves


def solve_labyrinth(initial_state: LabyrinthState) -> int:
    """Calculate the minimum number of steps required to move the rod from the initial
    state to the right bottom corner.

    Args:
        initial_state (LabyrinthState)

    Returns:
        int: Number of steps or -1 if the labyrinth can not be solved.
    """

    # Visited states and states to explore.
    visited = set()
    states_to_explore = {initial_state}

    while states_to_explore:
        state = states_to_explore.pop()

        if state in visited:
            continue

        visited.add(state)

        # Reached the bottom-right corner. There is no need to check for orientation.
        if (
            state.rod_pos.x == state.n_rows - 1 and state.rod_pos.y == state.n_cols - 2
        ) or (
            state.rod_pos.x == state.n_rows - 2 and state.rod_pos.y == state.n_cols - 1
        ):
            return state.steps

        # Check for valid moves
        valid_moves = get_valid_moves(state)

        # Add valid moves to current states
        states_to_explore.update(valid_moves)

    return -1


def labyrinth_parser(raw_labyrinth: list[list[str]]) -> LabyrinthState:
    """Parses the input into a `labyrinthState`.

    Args:
        raw_labyrinth (list[list[str]]): Lists describing the input using '.' and '#'.

    Raises:
        ValueError: Raises exception if the input is not valid.

    Returns:
        LabyrinthState
    """

    # Check that the input is valid.
    if not val_lab(raw_labyrinth):
        raise ValueError("Invalid input")

    walls = []

    for x, row in enumerate(raw_labyrinth):
        for y, element in enumerate(row):
            if element == "#":
                walls.append(Coordinates(x=x, y=y))

    n_rows = len(raw_labyrinth)
    n_cols = len(raw_labyrinth[0])
    rod_pos = Coordinates(x=1, y=0)

    return LabyrinthState(
        n_rows=n_rows,
        n_cols=n_cols,
        walls=walls,
        rod_pos=rod_pos,
        rod_orientation=Orientation.HORIZONTAL,
        steps=0,
    )


def min_dist_lab(raw_labyrinth: list[list[str]]) -> int:
    """Take two nested lists describing a labyrinth and founds the minimum amount of
    steps required to take a rod from the top left corner to the bottom right corner.

    Args:
        raw_labyrinth (list[list[str]]): Nested list describing the labyrinth.

    Returns:
        int: Minimum number of steps to complete the labyrinth or -1 if it can not be
        solved.
    """

    labyrinth = labyrinth_parser(raw_labyrinth)
    n_steps = solve_labyrinth(labyrinth)
    return n_steps
