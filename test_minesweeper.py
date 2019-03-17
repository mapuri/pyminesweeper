import unittest
import minesweeper


class TestBoard(unittest.TestCase):

    def test_board_init(self):
        tests = {
            "regular-case": {
                "rows": 10,
                "columns": 5,
                "mines": 12,
            },
            "no-mines": {
                "rows": 1,
                "columns": 5,
                "mines": 0,
            },
        }
        for name, test in tests.items():
            b = minesweeper.board(test["rows"], test["columns"], test["mines"])
            self.assertEqual(len(b._mine_cells), test["mines"], msg=name)
            self.assertEqual(len(b.cells), test["rows"], msg=name)
            self.assertEqual(len(b.cells[0]), test["columns"], msg=name)
            for i in range(test["rows"]):
                for j in range(test["columns"]):
                    if (i, j) in b._mine_cells:
                        self.assertEqual(
                            b.cells[i][j]._game_state, "mined", msg=name)

    def test_get_adjoining_mines(self):
        tests = {
            "no-adjoining-mines-case": {
                "mines_cells": [(1, 2), (3, 4), (5, 6)],
                "row": 1,
                "col": 2,
                "count": 0,
            },
            "one-adjoining-mines-case": {
                "mines_cells": [(1, 1), (3, 4), (5, 6)],
                "row": 1,
                "col": 2,
                "count": 1,
            },
            "eight-adjoining-mines-case": {
                "mines_cells": [(0, 1), (0, 2), (0, 3), (1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 4), (5, 6)],
                "row": 1,
                "col": 2,
                "count": 8,
            },
        }
        for name, test in tests.items():
            b = minesweeper.board(0, 0, 0)
            b._mine_cells = test["mines_cells"]
            self.assertEqual(b._get_adjoining_mines(
                test["row"], test["col"]), test["count"], msg=name)


if __name__ == "__main__":
    unittest.main()
