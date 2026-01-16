from enum import Enum


class Cell(Enum):
    FLAGGED = -1
    REVEALED_BOMB = -2
    UNREVEALED = -3

class Condition(Enum):
    IN_PROGRESS = 'in_progress'
    WIN = 'win'
    BOMB = 'bomb'

class ActionType(Enum):
    REVEAL = 'reveal'
    FLAG = 'flag'

class Action:
    def __init__(self, action_type, x, y):
        self.action_type = action_type
        self.x = x
        self.y = y

def create_random_board(size, bombs):
        """
        Creates a square game board with randomly placed bombs.

        Args:
            size (int): The size of the board (size x size).
            bombs (int): The number of bombs to place on the board.

        Returns:
            list: A 2D list representing the game board, where ' ' indicates an empty cell and 'B' indicates a bomb.
        """
        import random
        board = [[' ' for _ in range(size)] for _ in range(size)]
        bomb_positions = random.sample(range(size * size), bombs)
        for pos in bomb_positions:
            x, y = divmod(pos, size)
            board[x][y] = 'B'
        return board

def read_bomb_map(file_path):
    """
    Reads a bomb map from a file and returns it as a list of lists.

    Args:
        file_path (str): The path to the file containing the bomb map.

    Returns:
        list of list of str: A 2D list representing the bomb map, where each inner list is a row of the map.
    """
    with open(file_path, 'r') as file:
        bomb_map = [list(line.strip('\n')) for line in file.readlines()]
    return bomb_map
