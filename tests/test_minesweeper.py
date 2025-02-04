import pytest

from src.minesweeper import Minesweeper


def test_initialization():
    """Test the initialization of the Minesweeper game."""
    rows, cols, num_mines = 10, 10, 10
    game = Minesweeper(rows, cols, num_mines)

    assert game.rows == rows
    assert game.cols == cols
    assert game.num_mines == num_mines
    assert len(game.mines) == num_mines
    assert len(game.revealed) == 0
    assert game.game_state["won"] is False
    assert game.game_state["over"] is False


def test_mine_placement():
    """Test that mines are placed correctly on the board."""
    rows, cols, num_mines = 5, 5, 5
    game = Minesweeper(rows, cols, num_mines)

    # Ensure the number of mines placed is correct
    assert len(game.mines) == num_mines

    # Ensure mines are within the board boundaries
    for mine in game.mines:
        assert 0 <= mine[0] < rows
        assert 0 <= mine[1] < cols

    # Ensure the board reflects the mine placement
    mine_count = 0
    for row in range(rows):
        for col in range(cols):
            if game.board[row][col] == -1:
                mine_count += 1
    assert mine_count == num_mines


def test_adjacent_mine_count():
    """Test that the adjacent mine counts are calculated correctly."""
    rows, cols, num_mines = 3, 3, 1
    game = Minesweeper(rows, cols, num_mines)

    # Find the mine position
    mine_pos = next(iter(game.mines))

    # Check adjacent cells for correct counts
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            new_row, new_col = mine_pos[0] + dx, mine_pos[1] + dy
            if (new_row, new_col) == mine_pos:
                continue  # Skip the mine itself
            if 0 <= new_row < rows and 0 <= new_col < cols:
                assert game.board[new_row][new_col] == 1


def test_restart():
    """Test that the game restarts correctly."""
    rows, cols, num_mines = 5, 5, 5
    game = Minesweeper(rows, cols, num_mines)

    # Store initial mine positions
    initial_mines = game.mines.copy()

    # Restart the game
    game.restart()

    # Ensure the game state is reset
    assert len(game.mines) == num_mines
    assert len(game.revealed) == 0
    assert game.game_state["won"] is False
    assert game.game_state["over"] is False

    # Ensure the mine positions are different after restart
    assert game.mines != initial_mines


def test_game_over_on_mine_reveal():
    """Test that the game ends when a mine is revealed."""
    rows, cols, num_mines = 5, 5, 1
    game = Minesweeper(rows, cols, num_mines)

    # Reveal a mine
    mine_pos = next(iter(game.mines))
    game.reveal_cell(mine_pos[0], mine_pos[1])

    # Check game state
    assert game.game_state["over"] is True
    assert game.game_state["won"] is False


def test_game_won_when_all_non_mines_revealed():
    """Test that the game is won when all non-mine cells are revealed."""
    rows, cols, num_mines = 2, 2, 1
    game = Minesweeper(rows, cols, num_mines)

    # Reveal all non-mine cells
    for row in range(rows):
        for col in range(cols):
            if (row, col) not in game.mines:
                game.reveal_cell(row, col)

    # Check game state
    assert game.game_state["won"] is True
    assert game.game_state["over"] is True


if __name__ == "__main__":
    pytest.main()
