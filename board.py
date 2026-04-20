from config import *

class Board:

    def __init__(self):

        self.grid = [
            [0 for _ in range(COLS)]
            for _ in range(ROWS)
        ]

    def clear_lines(self):

        new = [row for row in self.grid if any(cell == 0 for cell in row)]

        cleared = ROWS - len(new)

        while len(new) < ROWS:
            new.insert(0,[0]*COLS)

        self.grid = new

        return cleared