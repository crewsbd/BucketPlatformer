import math
import os

import arcade

from settings import *
from gameview import GameView

def main():
    """This just creates the game view and runs it.
    """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE)
    game_view = GameView()
    window.show_view(game_view)
    arcade.run()


if __name__ == "__main__":
    main()