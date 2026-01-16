from graphics_display import MinesweeperUI
from utils import ActionType, Cell, Condition, create_random_board


class Minesweeper:
    # NOTE: Constructor
    def __init__(self, size=5, bombs=5, bomb_map=None, gui=False):
        """
        Initializes the Minesweeper game.

        Args:
            size (int, optional): The size of the board (size x size). Defaults to 5.
            bombs (int, optional): The number of bombs to place on the board. Defaults to 5.
            bomb_map (list of list of int, optional): A predefined bomb map. If None, a random bomb map is created. Defaults to None.
            gui (bool, optional): Whether to initialize the game with a GUI. Defaults to False.
        """
        self.size = size
        self.revealed_board = [[Cell.UNREVEALED for _ in range(size)] for _ in range(size)]

        # The actual bomb map, you should not access this variable and read from it
        self.__board = bomb_map if bomb_map else create_random_board(size, bombs)
        # For GUI purposes, you do not need to access and modify these variables.
        self.last_action = None  # Track the last revealed cell (x, y)
        self.gui = gui

        # update GUI if you're using one.
        if self.gui:
            self.gui = MinesweeperUI(self) #update GUI if you're using one.

    def obs(self):
        """
        Returns the current observation of the revealed board.

        The revealed board is a representation of the Minesweeper game board
        where cells that have been revealed are shown, and unrevealed cells
        remain hidden. Each cell can be one of the following values:
            - Cell.UNREVEALED: The cell has not been revealed.
            - Cell.FLAGGED: The cell has been flagged by the agent.
            - Cell.REVEALED_BOMB: The cell contains a bomb and has been revealed.
            - int: The cell has been revealed and contains a number indicating the

        Returns:
            list: A 2D list representing the revealed state of the Minesweeper board.
        """
        return self.revealed_board

    def step(self, action):
        """
        Takes a step in the Minesweeper game based on the given action.

        Args:
            action (Action): The action to be performed, which includes the type of action
                             (REVEAL or FLAG) and the coordinates (x, y) where the action
                             is to be performed.

        Returns:
            tuple: A tuple containing the current observation of the board and the game
                   condition after the action is performed. The game condition can be one
                   of the following:
                   - Condition.IN_PROGRESS: The game is still ongoing.
                   - Condition.BOMB: The game is over because a bomb was revealed.
                   - Condition.WIN: The game is won because all non-bomb cells are revealed.

        Notes:
            - If the action is to reveal a cell and the cell contains a bomb, the game ends.
            - If the action is to flag a cell, the cell is marked as flagged or unflagged.
            - The method updates the GUI if it is enabled, otherwise it prints the board
              and the game status to the console.
        """
        x, y = action.x, action.y
        print(f"Action: {action.action_type} at ({x}, {y})")
        if isinstance(self.revealed_board[x][y], int) and self.revealed_board[x][y] >= 0:
            return self.obs(), Condition.IN_PROGRESS
        # Update the board based on the action
        if action.action_type == ActionType.REVEAL:
            if self.__board[x][y] == 'B':
                self.revealed_board[x][y] = Cell.REVEALED_BOMB
            else:
                self.reveal(x, y)
        elif action.action_type == ActionType.FLAG: #flag/unflag
            self.revealed_board[x][y] = Cell.FLAGGED if self.revealed_board[x][y] != Cell.FLAGGED else Cell.UNREVEALED
        # Track the last action for highlighting
        self.last_action = action
        # Test if the game ends and update the GUI if necessary
        condition = self.goal_test()
        if self.gui:
            self.gui.update_gui(condition)
        else:
            self.print_board()
            if condition == Condition.BOMB:
                print("Game Over! You hit a bomb!")
            elif condition == Condition.WIN:
                print("Congratulations! You win!")
        return self.obs(), condition
    
    def goal_test(self):
        """
        Tests the current state of the game to determine if the goal has been reached.

        Returns:
            Condition: The current condition of the game, which can be one of the following:
                - Condition.BOMB: If the last action revealed a bomb.
                - Condition.IN_PROGRESS: If there are still unrevealed or flagged cells that are not bombs.
                - Condition.WIN: If all non-bomb cells have been revealed.
        """

        last_action = self.last_action

        # 1. If the last action revealed a bomb, you lose (return Condition.bomb)
        if (last_action.action_type == ActionType.REVEAL) and (self.revealed_board[last_action.x][last_action.y] == Cell.REVEALED_BOMB):
            return Condition.BOMB # you lose!

        # 2. Else if there are still unrevealed (or flagged) non-bomb cells remaining
        for row_i in range(self.size):
            for col_i in range(self.size):
                curr_cell = self.revealed_board[row_i][col_i] #self.revealed_board shows user-visible condition
                if (curr_cell == Cell.FLAGGED or curr_cell == Cell.UNREVEALED) and (self.__board[row_i][col_i] != 'B'):
                    return Condition.IN_PROGRESS

        # 3. You didn't click on a bomb, and there are no non-bombs left that are flagged or unrevealed.
        return Condition.WIN



    
    def print_board(self):
        """
        Prints the current state of the Minesweeper board.

        The board is printed row by row, with each cell represented by a specific character:
        - 'B' for revealed bombs.
        - 'F' for flagged cells.
        - A number (as a string) for revealed cells with adjacent bombs.
        - ' ' (space) for revealed cells with no adjacent bombs.
        - '.' for unrevealed cells.

        This method does not return any value; it only prints the board to the console.
        """
        for x in range(self.size):
            row = []
            for y in range(self.size):
                if self.revealed_board[x][y] == Cell.REVEALED_BOMB:
                    row.append('B')
                elif self.revealed_board[x][y] == Cell.FLAGGED:
                    row.append('F')
                elif isinstance(self.revealed_board[x][y], int):
                    if self.revealed_board[x][y] == 0:
                        row.append(' ')
                    elif self.revealed_board[x][y] > 0:
                        row.append(str(self.revealed_board[x][y]))
                else:
                    row.append('.')
            print(' '.join(row))
        print()

    def reveal(self, x, y, revealed=None):
        """
        Reveals the cell at the given coordinates (x, y) and recursively reveals adjacent cells if the cell has no adjacent bombs.

        Args:
            x (int): The x-coordinate of the cell to reveal.
            y (int): The y-coordinate of the cell to reveal.
            revealed (set, optional): A set of coordinates that have already been revealed. Defaults to None.

        Returns:
            None
        """
        if revealed is None:
            revealed = set()
        if (x, y) in revealed:
            return
        revealed.add((x, y))
        count = self.count_adjacent_bombs(x, y)
        self.revealed_board[x][y] = count
        if count == 0:
            directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.size and 0 <= ny < self.size:
                    self.reveal(nx, ny, revealed)

    def count_adjacent_bombs(self, x, y):
        """
        Counts the number of bombs adjacent to a given cell in the Minesweeper board.

        Args:
            x (int): The x-coordinate of the cell.
            y (int): The y-coordinate of the cell.

        Returns:
            int: The number of adjacent bombs.
        """
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        count = 0
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size and self.__board[nx][ny] == 'B':
                count += 1
        return count
