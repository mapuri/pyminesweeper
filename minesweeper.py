class InvalidInputError(Exception):
    ''' signal invalid user input '''
    pass

class cell(object):
    ''' cell represents a position on the board.
    It has following game states:
    - mined
    - clear
    - or a number indicating mined cells
    It has following display states:
    - closed
    - flagged
    - opened
    '''
    def __init__(self, game_state):
        self._game_state = game_state
        self._display_state = "closed"

    def open(self):
        ''' opens the cell. Throws exception if cell is mined '''
        pass
    
    def flag(self):
        ''' flags the cell. Throws exception if all flags (equals to number of mines)
        have been used '''
        pass
    
    def close(self):
        ''' closes the cell if it is flagged. Throws exception if cell is opened '''
        pass

class board(object):
    ''' board contains cells and represents current state of the game. ''' 
    def __init__(self, rows, columns, mines):
        ''' initialize the board with specified rows, columns and mines'''
        self._mines = mines
        self.cells = [[self._init_cell(i,j) for j in range(columns)] for i in range(rows)]

    def _init_cell(self, row, col):
        ''' returns a cell in it's initial state at the beginingof the game '''
        pass
    
    def open_one(self, row, col):
        ''' opens the specified cell '''
        pass

    def flag_one(self, row, col):
        ''' flags specified cell '''
        pass

    def close_one(self, row, col):
        ''' closes specified cell '''
        pass

    def _check_cell(self, row, col):
        ''' checks if the specified cell position is valid. Throws an InvalidInputError exception otherwise.'''
        pass

    def _refresh_display(self, row, col):
        ''' refreshes the display based on last move '''
        pass

class game(object):
    ''' game interfaces with the board through moves to progress the game. '''
    
    def __init__(self, difficulty = "easy"):
        ''' initializes the game with specified difficulty. Possible difficulty values are:
        - easy : 8 x 10 board, 10 mines
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
        - accepts the moves (a tuple representing action on a specific cell)
        - updates the state
        - and repeats until game is won or lost
        '''
        pass

def main():
    try:
        difficulty = input("Enter the difficulty level. [E/e]asy, [M/m]edium OR [D/d]ifficult")
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