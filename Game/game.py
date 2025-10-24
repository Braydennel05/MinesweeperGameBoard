import os
import random

'''The Game class handles the core logic of Minesweeper.
It generates the board, handles tile interactions, determines win/loss conditions, 
and communicates visual updates to the ScreenManager.'''
class Game:
    def __init__(self, screen, mineCount=10, boardSize=8, autoGenerate=True):
        self.screen = screen
        self.mineCount = mineCount
        self.boardSize = boardSize
        self.game_over = False

        self.defaultDictionary = {
            "discovered": False,
            "flagged": False,
            "mine": False,
            "neighbours": 0,
            "empty": False
        }
        self.board = [[self.defaultDictionary.copy() for _ in range(boardSize)] for _ in range(boardSize)]

        if autoGenerate:
            self.generateBoard()

    def start(self):
        print("Game started!")

        for row in range(self.boardSize):
            for col in range(self.boardSize):
             self.change_tile(row * 8 + col + 1, "Blank.png")

    def reset(self):
        """Reset the board for a new game."""
        # Reset flags
        self.game_over = False

        # Reset board data
        for row in range(self.boardSize):
            for col in range(self.boardSize):
                self.board[row][col] = self.defaultDictionary.copy()

        # Reset visuals
        for row in range(self.boardSize):
            for col in range(self.boardSize):
                self.change_tile(row * 8 + col + 1, "Blank.png")

        # Generate new mines
        self.generateBoard()

    def checkWin(self):
        """Check if all non-mine tiles have been revealed."""
        for row in range(self.boardSize):
            for col in range(self.boardSize):
                # If a non-mine tile is still hidden, player hasn't won yet
                if not self.board[row][col]["mine"] and not self.board[row][col]["discovered"]:
                    return False

        # Player has won — reveal all bombs as won.png
        for row in range(self.boardSize):
            for col in range(self.boardSize):
                if self.board[row][col]["mine"]:
                    self.change_tile(row * 8 + col + 1, "won.png")

        print("You Win!")
        self.game_over = True
        return True


    def get_index(self):
        return "Minesweeper"

    def button_press(self, buttonRow, buttonCol,theme, action):
        self.calculateTile(buttonRow, buttonCol,theme,action)
        

    def change_tile(self, tile_number, image):
        self.screen.change_tile(tile_number, image)

    def generateBoard(self):
        randomIntegers = [random.randint(0, (self.boardSize*self.boardSize)-1) for _ in range(self.mineCount)]
        for mineLocation in randomIntegers:
            row, col = divmod(mineLocation, 8)
            self.board[row][col]["mine"] = True
        self.calculateNeighbours()

    def calculateNeighbours(self):
        for row in range(self.boardSize):
            for col in range(self.boardSize):
                if self.board[row][col]["mine"]:
                    continue
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if 0 <= row + i < self.boardSize and 0 <= col + j < self.boardSize:
                            if self.board[row + i][col + j]["mine"]:
                                self.board[row][col]["neighbours"] += 1

    def revealAllMines(self, exclude=None):
        """Show all mines when game over, except the one that was pressed."""
        for row in range(self.boardSize):
            for col in range(self.boardSize):
                if self.board[row][col]["mine"]:
                    if exclude and (row, col) == exclude:
                        continue
                    self.change_tile(row * 8 + col + 1, "bomb.png")



    def calculateTile(self, row, col, theme, action):
        """Called when player clicks a tile."""
        # Ignore already revealed cells
        if self.board[row][col]["discovered"]:
            return
        
        if self.game_over:
            return

        # FLAG TOGGLE MODE
        if action:  # True means flag/unflag
            if not self.board[row][col]["flagged"]:
                self.board[row][col]["flagged"] = True
                self.change_tile(row * 8 + col + 1, "flag.png")
            else:
                self.board[row][col]["flagged"] = False
                self.change_tile(row * 8 + col + 1, "Blank.png")
            return

        # NORMAL CLICK MODE
        self.board[row][col]["discovered"] = True

        # Hit a mine
        if self.board[row][col]["mine"]:
            # Show the clicked mine as red
            self.change_tile(row * 8 + col + 1, "pressedbomb.png")
            print("Game Over")
            self.revealAllMines(exclude=(row, col))
            self.game_over = True
            return

        
        # Count nearby mines
        count = self.countNeighbours(row, col)

        if count == 0:
            self.change_tile(row * 8 + col + 1, "empty.png")
            self.board[row][col]["empty"] = True
            self.revealEmptyNeighbours(row, col, theme)
        else:
            self.change_tile(row * 8 + col + 1, f"{count}.png")

        # After handling tile reveal
        self.checkWin()


    def countNeighbours(self, row, col):
        """Count how many bombs are adjacent to (row, col)."""
        count = 0
        for r_offset in range(-1, 2):
            for c_offset in range(-1, 2):
                if r_offset == 0 and c_offset == 0:
                    continue
                new_r = row + r_offset
                new_c = col + c_offset
                if 0 <= new_r < self.boardSize and 0 <= new_c < self.boardSize:
                    if self.board[new_r][new_c]["mine"]:
                        count += 1
        return count


    def revealEmptyNeighbours(self, row, col, theme):
        """Recursively reveal all connected empty tiles."""
        for r_offset in range(-1, 2):
            for c_offset in range(-1, 2):
                if r_offset == 0 and c_offset == 0:
                    continue
                new_r = row + r_offset
                new_c = col + c_offset
                if 0 <= new_r < self.boardSize and 0 <= new_c < self.boardSize:
                    if not self.board[new_r][new_c]["discovered"]:
                        count = self.countNeighbours(new_r, new_c)
                        self.board[new_r][new_c]["discovered"] = True
                        if count == 0:
                            self.change_tile(new_r * 8 + new_c + 1, f"empty.png")
                            self.board[new_r][new_c]["empty"] = True
                            self.revealEmptyNeighbours(new_r, new_c, theme)
                        else:
                            self.change_tile(new_r * 8 + new_c + 1, f"{count}.png")
