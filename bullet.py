import math
import os

import arcade

from settings import *
from helpers import *

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

        self.texture_id = 0.0 # TEMP TESTING
        self.facing = arcade.FACE_RIGHT
        self.idle_textures = LRTextureList()
        self.walk_textures = LRTextureList()
        self.jump_textures = LRTextureList()
        self.shoot_textures = LRTextureList()

        # Load spritesheets
        self.idle_textures.right = arcade.load_spritesheet("resources/image/Bullet_Right.png",8,8,4,4,0,None)
        self.idle_textures.left = arcade.load_spritesheet("resources/image/Bullet_Left.png",8,8,4,4,0,None)

    def update(self): # Updates with the main loop
        super().update()
        self.change_y -= GRAVITY # Fall!
        
            
    def update_animation(self, delta_time: float = 1 / 60):
        super().update_animation(delta_time)
        self.texture_id = (self.texture_id + (1/2)) % 4  # That middle number is just the speed factor...It's bad.
  
