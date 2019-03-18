import unittest
import minesweeper
import re


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
        tests = {
            "row-out-of-bound": {
                "board": minesweeper.board(rows=1, columns=1, mines=0),
                "row": 2,
                "col": 0,
                "exptdError": re.compile("incorrect row: [\\d]+"),
            },
            "column-out-of-bound": {
                "board": minesweeper.board(rows=1, columns=1, mines=0),
                "row": 0,
                "col": 2,
                "exptdError": re.compile("incorrect column: [\\d]+"),
            },
            "row-and-column-out-of-bound": {
                "board": minesweeper.board(rows=1, columns=1, mines=0),
                "row": 2,
                "col": 2,
                "exptdError": re.compile("incorrect row: [\\d]+ incorrect column: [\\d]+"),
            },
            "valid-cell": {
                "board": minesweeper.board(rows=1, columns=1, mines=0),
                "row": 0,
                "col": 0,
                "exptdError": None,
            },
        }
        for name, test in tests.items():
            with self.subTest(name=name):
                if test["exptdError"] is not None:
                    self.assertRaisesRegex(
                        minesweeper.InvalidInputError, test["exptdError"], test["board"]._check_cell, row=test["row"], col=test["col"])
                else:
                    self.assertIsNone(test["board"]._check_cell(
                        test["row"], test["col"]))

    def test_check_move(self):
        tests = {
            "valid-move-open-closed": {
                "board": minesweeper.board(rows=1, columns=1, mines=0),
                "display_state": minesweeper.DisplayState.closed,
                "row": 0,
                "col": 0,
                "move": minesweeper.Move.open,
                "exptdError": None,
            },
            "valid-move-flag-closed": {
                "board": minesweeper.board(rows=1, columns=1, mines=0),
                "display_state": minesweeper.DisplayState.closed,
                "row": 0,
                "col": 0,
                "move": minesweeper.Move.flag,
                "exptdError": None,
            },
            "valid-move-clear-flagged": {
                "board": minesweeper.board(rows=1, columns=1, mines=0),
                "display_state": minesweeper.DisplayState.flagged,
                "row": 0,
                "col": 0,
                "move": minesweeper.Move.clear,
                "exptdError": None,
            },
            "invalid-move-clear-closed": {
                "board": minesweeper.board(rows=1, columns=1, mines=0),
                "display_state": minesweeper.DisplayState.closed,
                "row": 0,
                "col": 0,
                "move": minesweeper.Move.clear,
                "exptdError": re.compile("clear is not allowed for a cell that is closed"),
            },
            "invalid-move-clear-opened": {
                "board": minesweeper.board(rows=1, columns=1, mines=0),
                "display_state": minesweeper.DisplayState.opened,
                "row": 0,
                "col": 0,
                "move": minesweeper.Move.clear,
                "exptdError": re.compile("clear is not allowed for a cell that is opened"),
            },
            "invalid-move-flag-flagged": {
                "board": minesweeper.board(rows=1, columns=1, mines=0),
                "display_state": minesweeper.DisplayState.flagged,
                "row": 0,
                "col": 0,
                "move": minesweeper.Move.flag,
                "exptdError": re.compile("flag is not allowed for a cell that is flagged"),
            },
            "invalid-move-flag-opened": {
                "board": minesweeper.board(rows=1, columns=1, mines=0),
                "display_state": minesweeper.DisplayState.opened,
                "row": 0,
                "col": 0,
                "move": minesweeper.Move.flag,
                "exptdError": re.compile("flag is not allowed for a cell that is opened"),
            },
            "invalid-move-open-opened": {
                "board": minesweeper.board(rows=1, columns=1, mines=0),
                "display_state": minesweeper.DisplayState.opened,
                "row": 0,
                "col": 0,
                "move": minesweeper.Move.open,
                "exptdError": re.compile("open is not allowed for a cell that is opened"),
            },
            "invalid-move-open-flagged": {
                "board": minesweeper.board(rows=1, columns=1, mines=0),
                "display_state": minesweeper.DisplayState.flagged,
                "row": 0,
                "col": 0,
                "move": minesweeper.Move.open,
                "exptdError": re.compile("open is not allowed for a cell that is flagged"),
            },
        }
        for name, test in tests.items():
            with self.subTest(name=name):
                test["board"].cells[test["row"]][test["col"]
                                                 ]._display_state = test["display_state"]
                if test["exptdError"] is None:
                    self.assertIsNone(test["board"]._check_move(
                        test["row"], test["col"], test["move"]))
                else:
                    self.assertRaisesRegex(
                        minesweeper.InvalidInputError, test["exptdError"], test["board"]._check_move, row=test["row"], col=test["col"], move=test["move"])

    def test_try_move(self):
        tests = {
            "open-closed-mined": {
                "board": minesweeper.board(rows=1, columns=1, mines=1),
                "display_state": minesweeper.DisplayState.closed,
                "game_state": minesweeper.GameState.mined,
                "row": 0,
                "col": 0,
                "move": minesweeper.Move.open,
                "exptdError": re.compile("Opened a mine, you lost!"),
                "exptdErrorClass": minesweeper.OpenedMine,
                "new_display_state": minesweeper.DisplayState.opened,
                "new_flags": 1,

            },
            "open-closed-clear": {
                "board": minesweeper.board(rows=1, columns=1, mines=1),
                "display_state": minesweeper.DisplayState.closed,
                "game_state": minesweeper.GameState.clear,
                "row": 0,
                "col": 0,
                "move": minesweeper.Move.open,
                "exptdError": None,
                "exptdErrorClass": None,
                "new_display_state": minesweeper.DisplayState.opened,
                "new_flags": 1,
            },
            "flag-closed": {
                "board": minesweeper.board(rows=1, columns=1, mines=1),
                "display_state": minesweeper.DisplayState.closed,
                "game_state": minesweeper.GameState.clear,
                "row": 0,
                "col": 0,
                "move": minesweeper.Move.flag,
                "exptdError": None,
                "exptdErrorClass": None,
                "new_display_state": minesweeper.DisplayState.flagged,
                "new_flags": 0,
            },
            "flag-closed-out-of-flags": {
                "board": minesweeper.board(rows=1, columns=1, mines=0),
                "display_state": minesweeper.DisplayState.closed,
                "game_state": minesweeper.GameState.clear,
                "row": 0,
                "col": 0,
                "move": minesweeper.Move.flag,
                "exptdError": re.compile("you have already consumed all the flags!"),
                "exptdErrorClass": minesweeper.InvalidInputError,
                "new_display_state": minesweeper.DisplayState.closed,
                "new_flags": 0,
            },
            "clear-flagged": {
                "board": minesweeper.board(rows=1, columns=1, mines=0),
                "display_state": minesweeper.DisplayState.flagged,
                "game_state": minesweeper.GameState.clear,
                "row": 0,
                "col": 0,
                "move": minesweeper.Move.clear,
                "exptdError": None,
                "exptdErrorClass": None,
                "new_display_state": minesweeper.DisplayState.closed,
                "new_flags": 1,
            },
        }
        for name, test in tests.items():
            with self.subTest(name=name):
                test["board"].cells[test["row"]][test["col"]
                                                 ]._display_state = test["display_state"]
                test["board"].cells[test["row"]][test["col"]
                                                 ]._game_state = test["game_state"]
                if test["exptdError"] is None:
                    self.assertIsNone(test["board"].try_move(
                        test["row"], test["col"], test["move"]))
                else:
                    self.assertRaisesRegex(
                        test["exptdErrorClass"], test["exptdError"], test["board"].try_move, row=test["row"], col=test["col"], move=test["move"])
                self.assertEqual(
                    test["board"].cells[test["row"]][test["col"]]._display_state, test["new_display_state"])
                self.assertEqual(test["board"]._flags, test["new_flags"])


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
