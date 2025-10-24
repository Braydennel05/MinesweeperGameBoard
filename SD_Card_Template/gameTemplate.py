import os

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.running = False

    def start(self):
        """Called once the game begins."""
        self.running = True
        print("Game started!")
        # Example: draw all blank tiles at start
        for tile in range(1, 65):
            self.change_tile(tile, "image.png")

    def reset(self):
        """Resets the game state for a new round."""
        print("Game reset!")
        self.running = False
        self.start()

    def button_press(self, buttonRow, buttonCol, theme, action):
        """Handles button input from hardware."""
        print(f"Button pressed at ({buttonRow}, {buttonCol}), action={action}")
        # Example of visual feedback
        tile_number = buttonRow * 8 + buttonCol + 1
        self.change_tile(tile_number, "image.png" if action else "image.png")

    def get_index(self):
        """Optional: return game name or ID."""
        return "BaseTemplate"

    # --- Helper for drawing ---
    def change_tile(self, tile_number, image):
        """Change tile image using ScreenManager."""
        self.screen.change_tile(tile_number, image)