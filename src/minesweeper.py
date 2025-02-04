import random


class Minesweeper:
    """This class implements the Minesweeper game."""

    def __init__(self, rows: int, cols: int, num_mines: int):
        self.rows = rows
        self.cols = cols
        self.num_mines = min(num_mines, rows * cols)
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.mines = set()
        self.revealed = set()
        self.game_state = {"won": False, "over": False}
        self.place_mines()

    def place_mines(self):
        """This function places mines on the board."""
        mines_placed = 0
        while mines_placed < self.num_mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if (row, col) not in self.mines:
                self.mines.add((row, col))
                self.board[row][col] = -1
                mines_placed += 1
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        new_row, new_col = row + dx, col + dy
                        if (
                            0 <= new_row < self.rows
                            and 0 <= new_col < self.cols
                            and self.board[new_row][new_col] != -1
                        ):
                            self.board[new_row][new_col] += 1

    def restart(self):
        """Restart the game with the same parameters."""
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.mines = set()
        self.revealed = set()
        self.game_state = {"won": False, "over": False}
        self.place_mines()

    def reveal_cell(self, row: int, col: int):
        """Reveal a cell and update the game state."""
        if (row, col) in self.revealed:
            return  # Cell already revealed

        self.revealed.add((row, col))

        # Check if the revealed cell is a mine
        if (row, col) in self.mines:
            self.game_state["over"] = True
            self.game_state["won"] = False
            return

        # Check if all non-mine cells have been revealed
        total_cells = self.rows * self.cols
        if len(self.revealed) == total_cells - self.num_mines:
            self.game_state["won"] = True
            self.game_state["over"] = True
