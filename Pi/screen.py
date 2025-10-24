import pygame
import os
import sys

'''ScreenManager is responsible for handling all visual aspects of the game. 
It creates a dual-screen display using pygame, loads icons, and updates individual tiles or the entire board.
This class is used by the main script and game logic to show game progress and player interaction visually.'''
class ScreenManager:
    def __init__(self, icon_path, rows=8, cols=8, square_size=64):
        '''Initialize the pygame window and prepare the board layout. 
        It sets up two 4x8 grids stacked vertically to simulate two physical displays.'''
        pygame.init()
        self.ROWS = rows
        self.COLS = cols
        self.SQUARE_SIZE = square_size
        self.SCREEN_ROWS = 4
        self.SCREEN_COUNT = 2
        self.ICON_PATH = icon_path

        # total height = both screens stacked vertically
        total_height = self.SCREEN_COUNT * self.SCREEN_ROWS * square_size
        total_width = self.COLS * square_size

        self.window = pygame.display.set_mode((total_width, total_height))
        pygame.display.set_caption("Dual Game Board")
        self.clock = pygame.time.Clock()

        self.image_cache = {}
        # Initialize all tiles as blank at start
        self.tiles = ["blank.png"] * (self.ROWS * self.COLS)
        self.draw_full_board()

    '''load_icon loads and scales images from the specified icon directory.
    It caches images to prevent reloading them repeatedly, improving performance.'''
    def load_icon(self, filename):
        if filename not in self.image_cache:
            path = os.path.join(self.ICON_PATH, filename)
            if not os.path.exists(path):
                print(f"[WARN] Missing icon: {path}")
                path = os.path.join(self.ICON_PATH, "blank.png")
            img = pygame.image.load(path).convert_alpha()
            self.image_cache[filename] = pygame.transform.scale(img, (self.SQUARE_SIZE, self.SQUARE_SIZE))
        return self.image_cache[filename]

    '''change_tile updates a single tile on the board with a new image.
    It takes the tile number (1 to 64) and the image file name to display.'''
    def change_tile(self, tile_number, new_image):
        if tile_number < 1 or tile_number > self.ROWS * self.COLS:
            print(f"[WARN] Invalid tile: {tile_number}")
            return
        self.tiles[tile_number - 1] = new_image
        self.draw_tile(tile_number)

    '''draw_tile determines where a specific tile should appear on the window 
    (based on row/column) and blits the corresponding image there.'''
    def draw_tile(self, tile_number):
        index = tile_number - 1
        row = index // self.COLS
        col = index % self.COLS

        # figure out which half of window to draw in
        screen_index = 0 if row < self.SCREEN_ROWS else 1
        row_on_screen = row % self.SCREEN_ROWS

        img = self.load_icon(self.tiles[index])

        y_offset = screen_index * (self.SCREEN_ROWS * self.SQUARE_SIZE)
        x = col * self.SQUARE_SIZE
        y = row_on_screen * self.SQUARE_SIZE + y_offset

        self.window.blit(img, (x, y))
        pygame.display.update(pygame.Rect(x, y, self.SQUARE_SIZE, self.SQUARE_SIZE))

    '''draw_full_board refreshes all tiles on the board. 
    This is typically called at startup or after a reset.'''
    def draw_full_board(self):
        for i in range(1, self.ROWS * self.COLS + 1):
            self.draw_tile(i)

    '''run keeps the pygame window active and checks for exit events.
    Used for debugging or standalone testing of the screen display.'''
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.clock.tick(10)
