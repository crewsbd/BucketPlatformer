import math
import os

import arcade

from settings import *

class Bullet(arcade.Sprite):
    def __init__(
        self,
        image_file: str,
        scale: float,
        image_x: int,
        image_y: int,
        image_width: int,
        image_height: int,
        center_x: int,
        center_y: int,
    ):
        super().__init__(
            image_file,
            scale,
            image_x,
            image_y,
            image_width,
            image_height,
            center_x,
            center_y,
        )