import unittest

from LabyrinthSearch import min_dist_lab, InvalidLabyrinthError


class SolutionTests(unittest.TestCase):
    """Set of tests that checks the algorithm with some labyrinth of which the solution
    is known.
    """

    def test_1(self):
        raw_labyrinth = [
            [".", ".", ".", ".", ".", ".", ".", ".", "."],
            ["#", ".", ".", ".", "#", ".", ".", ".", "."],
            [".", ".", ".", ".", "#", ".", ".", ".", "."],
            [".", "#", ".", ".", ".", ".", ".", "#", "."],
            [".", "#", ".", ".", ".", ".", ".", "#", "."],
        ]

        result = min_dist_lab(raw_labyrinth)
        self.assertEqual(result, 11)

    def test_2(self):
        raw_labyrinth = [
            [".", ".", ".", ".", ".", ".", ".", ".", "."],
            ["#", ".", ".", ".", "#", ".", ".", "#", "."],
            [".", ".", ".", ".", "#", ".", ".", ".", "."],
            [".", "#", ".", ".", ".", ".", ".", "#", "."],
            [".", "#", ".", ".", ".", ".", ".", "#", "."],
        ]

        result = min_dist_lab(raw_labyrinth)
        self.assertEqual(result, -1)

    def test_3(self):
        raw_labyrinth = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]

        result = min_dist_lab(raw_labyrinth)
        self.assertEqual(result, 2)

    def test_4(self):
        raw_labyrinth = [
            [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", "#", ".", ".", ".", ".", "#", ".", ".", "."],
            [".", "#", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", "#", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", "#", ".", ".", ".", "#", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", "#", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
        ]

        result = min_dist_lab(raw_labyrinth)
        self.assertEqual(result, 16)


class InputTests(unittest.TestCase):
    """Set of tests checking that an invalid input raises an exception."""

    # Test number of rows.
    def test_too_few_rows(self):
        raw_labyrinth = [
            [".", ".", ".", ".", ".", ".", ".", ".", "."],
            ["#", ".", ".", ".", "#", ".", ".", ".", "."],
        ]

        with self.assertRaises(InvalidLabyrinthError):
            min_dist_lab(raw_labyrinth)

    def test_too_many_rows(self):
        raw_labyrinth = [[".", ".", "."] for _ in range(1001)]

        with self.assertRaises(InvalidLabyrinthError):
            min_dist_lab(raw_labyrinth)

    # Test number of columns.
    def test_too_few_cols(self):
        raw_labyrinth = [[".", "."], ["#", "."], [".", "."]]

        with self.assertRaises(InvalidLabyrinthError):
            min_dist_lab(raw_labyrinth)

    def test_too_many_cols(self):
        raw_labyrinth = [["." for _ in range(1001)] for _ in range(3)]

        with self.assertRaises(InvalidLabyrinthError):
            min_dist_lab(raw_labyrinth)

    # Test rectangle shape.
    def test_rectangle_shape(self):
        raw_labyrinth = [[".", ".", "#", "."], ["#", ".", "."], [".", ".", "#", "."]]

        with self.assertRaises(InvalidLabyrinthError):
            min_dist_lab(raw_labyrinth)

    # Test unallowed characters.
    def test_unallowed_characters(self):
        raw_labyrinth = [
            [".", ".", "#", "."],
            ["#", ".", ".", "+"],
            [".", ".", "#", "."],
        ]

        with self.assertRaises(InvalidLabyrinthError):
            min_dist_lab(raw_labyrinth)

    # Test valid initial state.
    def test_initial_state(self):
        raw_labyrinth = [
            [".", ".", "#"],
            [".", ".", "."],
            [".", ".", "#"],
        ]

        with self.assertRaises(InvalidLabyrinthError):
            min_dist_lab(raw_labyrinth)


if __name__ == "__main__":
    unittest.main()
