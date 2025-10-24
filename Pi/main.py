import importlib.util
import os
import time
import pygame
import sys
import select
from screen import ScreenManager

# CHANGE THESE PATHS FOR YOUR SYSTEM
''' These 5 lines are used to idicate the SD card / Main and its location as well as the Icons
(Note that the Icons are a variable so we can do multiple themes)'''
SD_PATH = r"C:\Users\nhhas\Documents\School\IEEE\Minesweeper\Code\Game\game.py"
SD_THEME = "Classic"
SD_ICONS = rf"C:\Users\nhhas\Documents\School\IEEE\Minesweeper\Code\Game\Icons\{SD_THEME}"
THEME = "Default"
ICONS = rf"C:\Users\nhhas\Documents\School\IEEE\Minesweeper\Code\Pi\Icons\{THEME}"


'''Load_game basically makes sure that it can find the game and as well as establishes the screen'''
def load_game(path, screen):
    if not os.path.exists(path):
        print("No game cartridge detected.")
        return None
    spec = importlib.util.spec_from_file_location("game", path)
    game_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(game_module)
    return game_module.Game(screen)


'''Button_to_Index will take the inputs from the arduinos and break it down to tell the game file a button was pressed and its location'''
def button_to_index(bits: str, game, action):
    if len(bits) != 6:
        raise ValueError("Bits string must be exactly 6 characters long.")
    row = int(bits[:3], 2)
    col = int(bits[3:], 2)
    game.button_press(row, col, THEME, action)


'''NonBlocking_input makes sure that the PYGames doesnt crash when putting in inputs'''
def nonblocking_input(prompt="", timeout=0.1):
    """Waits for input for up to timeout seconds, returns line or None."""
    print(prompt, end="", flush=True)
    i, _, _ = select.select([sys.stdin], [], [], timeout)
    if i:
        return sys.stdin.readline().strip()
    return None


'''Main does what main does and runs everything it for now controls in inputs that will help later determine the buttons inputs'''
def main():
    screen = ScreenManager(icon_path=ICONS)
    pygame.display.flip()
    screen.clock.tick(30)
    print("Window initialized — now waiting for input...")

    start = input("Enter 'y'=start, 'n'=quit: ").strip().lower()

    if start == "y":
        screen = ScreenManager(icon_path=SD_ICONS)
        pygame.display.flip()
        screen.clock.tick(30)
        print("Game initialized — now waiting for input...")

    game = None
    action = False
    running = True

    while running:
        bits = input("Enter 6-bit (or 's'=start, 'a'=flag, 'q'=quit): ").strip().lower()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
                return

        if bits == "q":
            running = False
            break

        elif bits == "s":
            if game is None:
                game = load_game(SD_PATH, screen)
                if not game:
                    return
                game.start()
            else:
                # Reset the game if it already exists
                game.reset()
                game.start()
                print("New game started!")

        elif bits == "a":
            action = not action
            print(f"Flag mode: {action}")
        else:
            if game is None:
                print("Game not started yet. Press 's' first.")
                continue
            try:
                button_to_index(bits, game, action)
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    main()
