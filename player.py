import math
import os

import arcade

from settings import *
from helpers import *

from bullet import Bullet

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

        self.SHOOT_DELAY = .2
        self.shot_timer = 0
        self.texture_id = 0.0 # TEMP TESTING
        self.facing = arcade.FACE_RIGHT
        self.idle_textures = LRTextureList()
        self.walk_textures = LRTextureList()
        self.jump_textures = LRTextureList()
        self.shoot_textures = LRTextureList()
        self.shoot_sound = arcade.load_sound("./resources/sound/player_shoot.wav")
        self.jump_sound = arcade.load_sound("./resources/sound/player_jump.wav")
        self.camera_target = () # I wanted the camera to lead the player a little. This facilitates that.

        # Load spritesheets
        self.idle_textures.right = arcade.load_spritesheet("resources/image/BucketIdleStraightRight.png",32,32,8,8,0,None)
        self.idle_textures.left = arcade.load_spritesheet("resources/image/BucketIdleStraightLeft.png",32,32,8,8,0,None)

        self.jump_reset = True  # Can the player jump again after landing. Needs to release the jump key to enable this

    def jump(self, physics: arcade.PymunkPhysicsEngine):
        """Call this to make the sprite jump
        """
        if self.jump_reset:
            self.change_y = 10  # TODO: Remove this hard code
            physics.apply_impulse(self, (0, 23000))
            arcade.play_sound(self.jump_sound)
            self.jump_reset = False  # Jumping will reset when we let go of the jump button

    def shoot(self, bullet_list: list[arcade.Sprite], physics: arcade.PymunkPhysicsEngine):
        if self.shot_timer <= 0:
            self.shot_timer = self.SHOOT_DELAY # Reset the timer
            unit_speed = 1 
            if self.facing == arcade.FACE_LEFT: # Set out unit direction. 1 or -1
                unit_speed = -unit_speed

            # Make a new bullet and add it to the right lists
            new_bullet = Bullet("resources/image/Bullet_Right.png",GAME_SCALE, 0,0,8,8,self.center_x + unit_speed*20, self.center_y-10)
            new_bullet.facing = self.facing # Bullet points in same direction as player.
            bullet_list.append(new_bullet)
            physics.add_sprite(new_bullet)
            physics.apply_impulse(new_bullet, (unit_speed*2900, 100))
            arcade.play_sound(self.shoot_sound)


    def update(self): 
        """ Updates with the main loop
        """
        super().update()
        delta_time = 1/60  # I'd like to have a true delta time, but pymunk doesn't like it.
        if self.shot_timer > 0:  # Handle the shot timer, to regulate fire rate
            self.shot_timer -= delta_time

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
