import pytest

from src.minesweeper import Minesweeper


def test_initialization():
    """Test the initialization of the Minesweeper game."""
    # Test valid initialization
    game = Minesweeper(5, 5, 5)
    assert game.rows == 5
    assert game.cols == 5
    assert game.num_mines == 5
    assert len(game.mines) == 5
    assert len(game.revealed) == 0
    assert not game.won
    assert not game.game_over

    # Test that board dimensions match
    assert len(game.board) == 5
    assert len(game.board[0]) == 5

    # Test mine count limitation
    game = Minesweeper(3, 3, 10)  # More mines than cells
    assert game.num_mines == 9  # Should be limited to board size


def test_mine_placement():
    """Test the placement of mines on the board."""
    game = Minesweeper(5, 5, 5)

    # Count mines on board
    mine_count = sum(1 for row in game.board for cell in row if cell == -1)
    assert mine_count == 5

    # Verify mine coordinates match board representation
    for row, col in game.mines:
        assert game.board[row][col] == -1

    # Check that adjacent cells to mines have correct numbers
    for row in range(game.rows):
        for col in range(game.cols):
            if (row, col) not in game.mines:
                # Count adjacent mines manually
                adjacent_mines = 0
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        new_row, new_col = row + dx, col + dy
                        if (new_row, new_col) in game.mines:
                            adjacent_mines += 1
                assert game.board[row][col] == adjacent_mines


def test_restart():
    """Test the restart functionality."""
    game = Minesweeper(5, 5, 5)

    # Store initial state
    initial_mines = game.mines.copy()
    initial_board = [row[:] for row in game.board]

    # Add some revealed cells
    game.revealed.add((0, 0))
    game.won = True
    game.game_over = True

    # Restart game
    game.restart()

    # Verify game state is reset
    assert len(game.revealed) == 0
    assert not game.won
    assert not game.game_over

    # Verify new mines are placed
    assert len(game.mines) == 5
    # Very unlikely but possible that mines are in exactly same positions
    mine_count = sum(1 for row in game.board for cell in row if cell == -1)
    assert mine_count == 5


@pytest.mark.parametrize(
    "rows,cols,mines",
    [
        (1, 1, 1),  # Minimal board
        (10, 10, 20),  # Medium board
        (3, 4, 5),  # Rectangular board
        (5, 5, 24),  # Almost full board
    ],
)
def test_various_board_sizes(rows, cols, mines):
    """Test different board configurations."""
    game = Minesweeper(rows, cols, mines)

    assert game.rows == rows
    assert game.cols == cols
    assert game.num_mines <= rows * cols
    assert len(game.mines) == min(mines, rows * cols)

    # Verify board dimensions
    assert len(game.board) == rows
    assert all(len(row) == cols for row in game.board)


def test_edge_cases():
    """Test edge cases and invalid inputs."""
    # Test with minimum possible values
    game = Minesweeper(1, 1, 1)
    assert game.rows == 1
    assert game.cols == 1
    assert game.num_mines == 1

    # Test with zero mines
    game = Minesweeper(5, 5, 0)
    assert len(game.mines) == 0
    assert all(cell == 0 for row in game.board for cell in row)
