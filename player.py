import math
import os

import arcade

from settings import *
from helpers import *

class Player(arcade.Sprite):
    """This is the player sprite class.

    Args:
        arcade (): The base class that Player is derived from
    """
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
        self.camera_target = () # I wanted the camera to lead the player a little. This facilitates that.

        # Load spritesheets
        self.idle_textures.right = arcade.load_spritesheet("resources/image/BucketIdleStraightRight.png",32,32,8,8,0,None)
        self.idle_textures.left = arcade.load_spritesheet("resources/image/BucketIdleStraightLeft.png",32,32,8,8,0,None)

        self.jump_reset = True  # Can the player jump again after landing. Needs to release the jump key to enable this

    def jump(self):
        """Call this to make the sprite jump
        """
        if self.jump_reset:
            self.change_y = 10  # TODO: Remove this hard code
            self.jump_reset = (
                False  # Jumping will reset when we let go of the jump button
            )

    def update(self): 
        """ Updates with the main loop
        """
        super().update()
        if self.facing == arcade.FACE_RIGHT: # Make camera lead a little
            self.camera_target = (self.center_x + 100, self.center_y)
        else:
            self.camera_target = (self.center_x - 100, self.center_y)
            
    def update_animation(self, delta_time: float = 1 / 60):
        super().update_animation(delta_time)
        self.texture_id = (self.texture_id + (1/6)) % 8  # This is my lame way to put a delay in the animation. TODO: Better animation system.
  
        if self.facing == arcade.FACE_RIGHT:
            self.texture = self.idle_textures.right[int(math.floor(self.texture_id))]
        else:
            self.texture = self.idle_textures.left[int(math.floor(self.texture_id))]
