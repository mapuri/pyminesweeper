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
            with self.subTest(name=name):
                b = minesweeper.board(
                    test["rows"], test["columns"], test["mines"])
                self.assertEqual(len(b._mine_cells), test["mines"])
                self.assertEqual(len(b.cells), test["rows"])
                self.assertEqual(len(b.cells[0]), test["columns"])
                for i in range(test["rows"]):
                    for j in range(test["columns"]):
                        if (i, j) in b._mine_cells:
                            self.assertEqual(
                                b.cells[i][j]._game_state, minesweeper.GameState.mined)

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
            with self.subTest(name=name):
                b = minesweeper.board(0, 0, 0)
                b._mine_cells = test["mines_cells"]
                self.assertEqual(b._get_adjoining_mines(
                    test["row"], test["col"]), test["count"])

    def test_check_cell(self):
        pass

    def test_check_move(self):
        pass

    def test_try_move(self):
        pass

    def test_refesh_display(self):
        pass


class TestCell(unittest.TestCase):
    def test_str(self):
        tests = {
            "closed-cell": {
                "game_state": minesweeper.GameState.mined,
                "display_state": minesweeper.DisplayState.closed,
                "str": "\u25C9",
            },
            "flagged-cell": {
                "game_state": minesweeper.GameState.mined,
                "display_state": minesweeper.DisplayState.flagged,
                "str": "\u26F3",
            },
            "opened-mined-cell": {
                "game_state": minesweeper.GameState.mined,
                "display_state": minesweeper.DisplayState.opened,
                "str": "\u2620",
            },
            "opened-clear-cell": {
                "game_state": minesweeper.GameState.clear,
                "display_state": minesweeper.DisplayState.opened,
                "str": "\u25EF",
            },
            "opened-numbered-cell": {
                "game_state": 11,
                "display_state": minesweeper.DisplayState.opened,
                "str": "11",
            },
        }
        for name, test in tests.items():
            with self.subTest(name=name):
                cell = minesweeper.cell(game_state=test["game_state"])
                cell._display_state = test["display_state"]
                self.assertEqual(str(cell), test["str"])


if __name__ == "__main__":
    unittest.main()
