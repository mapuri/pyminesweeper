import random
from enum import Enum


class InvalidInputError(Exception):
    ''' signal invalid user input '''
    pass


class OpenedMine(Exception):
    ''' signal game end when user opens a mine '''
    pass


class Move(Enum):
    ''' allowed player moves '''
    open = 0
    flag = 1
    clear = 2


class GameState(Enum):
    ''' possible cell game states. Game state > 0 indicates a cell with adjoining mines '''
    mined = -1
    clear = 0


class DisplayState(Enum):
    ''' possible cell display states '''
    closed = 0
    flagged = 1
    opened = 2


class cell(object):
    ''' cell represents a position on the board.
    It has following game states:
    - mined
    - clear
    - or a number indicating adjoining mined cells
    It has following display states:
    - closed
    - flagged
    - opened
    '''

    def __init__(self, game_state: GameState):
        self._game_state = game_state
        self._display_state = DisplayState.closed

    def __str__(self):
        if self._display_state == DisplayState.closed:
            return "\u25C9"  # fish eye
        if self._display_state == DisplayState.flagged:
            return "\u26F3"  # flag
        if self._display_state == DisplayState.opened:
            if self._game_state == GameState.mined:
                return "\u2620"  # skull
            if self._game_state == GameState.clear:
                return "\u25EF"  # large circle
            return str(self._game_state)


class board(object):
    ''' board contains cells and represents current state of the game. '''

    def __init__(self, rows: int, columns: int, mines: int):
        ''' initialize the board with specified rows, columns and mines'''
        self._mines = mines
        self._rows = rows
        self._columns = columns
        self._flags = mines

        # pick randoms mine cells
        self._mine_cells = []
        while len(self._mine_cells) < mines:
            i, j = random.randint(0, rows-1), random.randint(0, columns-1)
            if (i, j) not in self._mine_cells:
                self._mine_cells.append((i, j))

        # initialize the board
        self.cells = [[cell(game_state=GameState.clear)
                       for j in range(columns)] for i in range(rows)]

        # place the mines
        for (row, col) in self._mine_cells:
            self.cells[row][col]._game_state = GameState.mined

        # setup rest of the cells
        for row in range(self._rows):
            for col in range(self._columns):
                if self.cells[row][col]._game_state == GameState.clear:
                    # check if the cell has adjoining mines and set a number, if any
                    mine_count = self._get_adjoining_mines(row, col)
                    if mine_count > 0:
                        self.cells[row][col]._game_state = mine_count

    def _get_adjoining_mines(self, row: int, col: int):
        ''' return the number of mines adjoining the cell '''
        adjoining_cells = [
            (row-1, col-1), (row-1, col), (row-1, col+1),
            (row, col-1), (row, col+1),
            (row+1, col-1), (row+1, col), (row+1, col+1),
        ]
        adjoining_mines = list(
            filter(lambda x: x in self._mine_cells, adjoining_cells))
        return len(adjoining_mines)

    def rows(self):
        return self._rows

    def columns(self):
        return self._columns

    def mines(self):
        return self._mines

    def _check_cell(self, row: int, col: int):
        ''' checks if the specified cell position is valid. Throws an InvalidInputError exception otherwise.
        Invalid cell comprises of:
          - invalid row or column or both
        '''
        err = ""
        if row < 0 or row > (self._rows-1):
            err = "incorrect row: {}".format(row)
        if col < 0 or col > (self._columns-1):
            err += " incorrect column: {}".format(col)
        if err != "":
            raise InvalidInputError(err)

    def _check_move(self, row: int, col: int, move: Move):
        ''' checks if the move is allowed at the specified cell. Throws an InvalidInputError exception otherwise.
        Invalid move comprises of:
          - opening a cell that is already open
          - flagging a cell that is already open
          - opening a cell that is flagged
          - clearing a cell that is not flagged
          - flagging a closed cell after all flags have been exhausted
        '''
        display_state = self.cells[row][col]._display_state
        invalid_moves = {
            DisplayState.closed: [Move.clear],
            DisplayState.flagged: [Move.open, Move.flag],
            DisplayState.opened: [Move.clear, Move.open, Move.flag],
        }
        if move in invalid_moves[display_state]:
            raise InvalidInputError(
                move.name + " is not allowed for a cell that is " + display_state.name)

    def try_move(self, row: int, col: int, move: Move):
        ''' tries the specified move on a cpecified cell. One of possible outcome:
        - an invalid cell results in InvalidInputError exception, and user is allowed to enter again.
        - an invalid move results in InvalidInputError exception, and user is allowed to enter again.
        - flagging a closed cell
        - clearing a flagged cell
        - opening a closed cell
        - opening a mined cell (this results in OpenedMine exception and game ends)
        '''
        self._check_cell(row, col)
        self._check_move(row, col, move)
        cell = self.cells[row][col]
        if move == Move.open:
            # _check_move ensure that only display state possible here is DisplayState.closed
            if cell._game_state != GameState.mined:
                cell._display_state = DisplayState.opened
                if cell._game_state == GameState.clear:
                    self._open_adjoining_clear(row, col)
            if cell._game_state == GameState.mined:
                # set the state of cells to open and raise the exception to end the game
                for i in range(self._rows):
                    for j in range(self._columns):
                        self.cells[i][j]._display_state = DisplayState.opened
                raise OpenedMine("Opened a mine, you lost!")

        if move == Move.flag:
            # _check_move ensures that only display state possible here is DisplayState.closed
            if self._flags <= 0:
                raise InvalidInputError(
                    "you have already consumed all the flags!")
            self._flags -= 1
            cell._display_state = DisplayState.flagged

        if move == Move.clear:
            # _check_move ensures that only display state possible here is DisplayState.flagged
            self._flags += 1
            cell._display_state = DisplayState.closed

    def _open_adjoining_clear(self, row: int, col: int):
        ''' tries to open all adjoining cells that are clear '''
        adjoining_cells = [
            (row-1, col-1), (row-1, col), (row-1, col+1),
            (row, col-1), (row, col+1),
            (row+1, col-1), (row+1, col), (row+1, col+1),
        ]

        valid_cells = list(filter(lambda t: t[0] >= 0 and t[0] <
                                  self._rows and t[1] >= 0 and t[1] < self._columns, adjoining_cells))
        for adj_row, adj_col in valid_cells:
            adj_cell = self.cells[adj_row][adj_col]
            if adj_cell._display_state == DisplayState.closed and adj_cell._game_state != GameState.mined:
                adj_cell._display_state = DisplayState.opened
                if adj_cell._game_state == GameState.clear:
                    self._open_adjoining_clear(adj_row, adj_col)

    def refresh_display(self):
        ''' prints the current state of the board '''
        print("*".join([" " for i in range(20)]))
        print("{} flags remaining".format(self._flags))
        print("{} {}".format(" ", [str(i) for i in range(self._columns)]))
        for i in range(self._rows):
            print("{} {}".format(i, [str(cell) for cell in self.cells[i]]))
        print("*".join([" " for i in range(20)]))

    def more_moves_remaining(self):
        ''' checks if there are more moves remaining '''
        # if a cell is still in closed state, then there are more moves possible
        for i in range(self._rows):
            if any([cell._display_state == DisplayState.closed for cell in self.cells[i]]):
                return True
        # otherwise if any flags are remainging then there are more moves possible
        return self._flags > 0


class game(object):
    ''' game interfaces with the board through moves to progress the game. '''

    def __init__(self, difficulty="easy"):
        ''' initializes the game with specified difficulty. Possible difficulty values are:
        - easy: 8 x 10 board, 10 mines
        - medium: 14 x 18 board, 40 mines
        - hard: 20 x 24 board, 100 mines
        '''
        if difficulty not in ["Easy", "easy", "E", "e", "Medium", "medium", "M", "m", "Difficult", "difficult", "D", "d"]:
            raise InvalidInputError("Invalid input: " + difficulty)

        rows, cols, mines = 8, 10, 10
        if difficulty in ["Medium", "medium", "M", "m"]:
            rows, cols, mines = 14, 18, 40
        if difficulty in ["Difficult", "difficult", "D", "d"]:
            rows, cols, mines = 20, 24, 100

        self.board = board(rows, cols, mines)

    def play(self):
        ''' represents the game. It:
        - accepts the moves(a tuple representing action on a specific cell)
        - updates the state
        - and repeats until game is won or lost
        '''
        def validate_int(text):
            try:
                row = int(text)
            except ValueError:
                return (0, False)
            else:
                return (row, True)

        def validate_move(text):
            if text not in ["Open", "open", "O", "o", "Flag", "flag", "F", "f", "Clear", "clear", "C", "c"]:
                return ("", False)
            if text in ["Open", "open", "O", "o"]:
                return (Move.open, True)
            if text in ["Flag", "flag", "F", "f"]:
                return (Move.flag, True)
            if text in ["Clear", "clear", "C", "c"]:
                return (Move.clear, True)

        def validate_yes_no(text):
            if text not in ["Yes", "yes", "Y", "y", "No", "no", "N", "n"]:
                return ("", False)
            if text in ["Yes", "yes", "Y", "y"]:
                return ("yes", True)
            if text in ["No", "no", "N", "n"]:
                return ("no", True)

        self.board.refresh_display()
        while self.board.more_moves_remaining():
            try:
                row = self._input(msg="Enter the row: ",
                                  validator=validate_int)
                col = self._input(msg="Enter the column: ",
                                  validator=validate_int)
                move = self._input(
                    msg="Enter your move. [O/o]pen, [F/f]lag, [C/c]lear: ", validator=validate_move)
                self.board.try_move(row, col, move)
            except InvalidInputError as e:
                print(e)
            except OpenedMine as e:
                print(e)
                return
            except KeyboardInterrupt as e:
                print()
                yes_no = self._input(
                    msg="Leave the game. [Y/y]es, [N/n]o: ", validator=validate_yes_no)
                if yes_no == "yes":
                    print("Bye!")
                    return
            finally:
                self.board.refresh_display()
        print("Hooray!! You won!!")

    def _input(self, msg=None, validator=None):
        ''' accepts a user input and validates it using specified validator '''
        while True:
            text = input(msg)
            out, ok = validator(text)
            if ok:
                return out
            print("invalid input: ", text)


def main():
    try:
        difficulty = input(
            "Enter the difficulty level. [E/e]asy, [M/m]edium OR [D/d]ifficult: ")
        g = game(difficulty)
        g.play()
    except EOFError:
        print("Bye!")
        exit(0)
    except InvalidInputError as e:
        print(e)
        exit(-1)


if __name__ == '__main__':
    main()
