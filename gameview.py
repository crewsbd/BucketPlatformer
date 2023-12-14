import math
import os

import arcade
import pytiled_parser

from settings import *
from helpers import *
from inputmanager import InputManager

from player import Player
from quid import Quid
from bullet import Bullet


class GameView(arcade.View):
    def __init__(self):
        """GameView constructor. Declares all the properties of GameView"""
        super().__init__()
        self.scene = None
        self.map = None
        self.player = None
        self.physics_engine = None
        self.input_manager = None
        self.player_camera = None
        self.ui_camera = None

        self.score = 0

        self.sounds = {}
        self.sounds["player_shoot"] = arcade.load_sound(
            "./resources/sound/player_shoot.wav"
        )
        self.sounds["player_jump"] = arcade.load_sound(
            "./resources/sound/player_jump.wav"
        )
        self.background_images = arcade.SpriteList()
        self.background_images.append(
            arcade.Sprite("./resources/image/Background.png", scale=GAME_SCALE * 1.1)
        )

    def setup(self):
        """Set up all the resources, values and states the game needs to start. This should only be called once. Loading new levels will be handled in a different way"""
        self.player = Player(
            "resources/image/BucketIdleStraightRight.png",
            scale=GAME_SCALE,
            image_x=0,
            image_y=0,
            image_width=32,
            image_height=32,
            center_x=450,
            center_y=650,
        )
        self.player.set_hit_box([(0,-16), (10,-14), (16,0), (-16,0), (-10, -14)])
        

        self.player_camera = arcade.Camera(self.window.width, self.window.height)
        self.ui_camera = arcade.Camera(self.window.width, self.window.height)
        self.input_manager = InputManager()

        # Set some options for each of the scene layers. Mostly for performance considerations.
        layer_options = {
            "Platforms": {
                "use_spatial_hash": True,
            },
            "Near Background": {
                "use_spatial_hash": True,
                
            },
            "Moving Platforms": {
                "use_spatial_hash": False,
            },
        }
        # Load the map and set the scene up
        self.map = arcade.load_tilemap(MAP_FILE, TILE_SCALING, layer_options)
        self.scene = arcade.Scene.from_tilemap(self.map)
    
        
        self.scene.add_sprite_list("Bullets")
        self.scene.add_sprite("Player", self.player)


        if self.map.background_color:
            arcade.set_background_color(self.map.background_color)

        self.physics_engine = arcade.PymunkPhysicsEngine(gravity=(0, -1500))
        self.physics_engine.add_sprite(  # Add the player
            self.player,
            mass=10,
            friction=0.1,
            moment=arcade.PymunkPhysicsEngine.MOMENT_INF,
            collision_type="player",
            max_horizontal_velocity=500,
            max_vertical_velocity=500,
            damping=.99, elasticity=.5
        )
        # Spawn things from the map file
        for spawn in self.map.object_lists["Spawn Points"]:
            if spawn.properties["type"] == "player_spawn":
                self.player.center_x = spawn.shape[X_CORD]
                self.player.center_y = spawn.shape[Y_CORD]
            if spawn.properties["type"] == "enemy_spawn":
                new_enemy = Quid(
                "./resources/image/Quid_Right.png",
                scale=GAME_SCALE,
                image_x=0,
                image_y=0,
                image_width=32,
                image_height=32,
                center_x=spawn.shape[X_CORD],
                center_y=spawn.shape[Y_CORD],   
                )
                new_enemy.set_hit_box([(0,-16), (10,-14), (16,0), (-16,0), (-10, -14)])
                self.scene.add_sprite("Enemies", new_enemy)
                self.physics_engine.add_sprite(new_enemy, mass=10, moment=arcade.PymunkPhysicsEngine.MOMENT_INF, collision_type="item", body_type=arcade.PymunkPhysicsEngine.KINEMATIC)
        

   
        self.physics_engine.add_sprite_list(
            self.scene["Platforms"],
            friction=0.7,
            collision_type="wall",
            body_type=arcade.PymunkPhysicsEngine.STATIC,
        )

    def on_show_view(self):
        """Runs when the View is first visible"""
        self.setup()

    def on_draw(self):
        """Draws the entire view each frame"""
        self.clear()
        self.ui_camera.use()
        # self.background_images.draw(pixelated=True)
        self.player_camera.use()

        self.scene.draw(pixelated=True)
        
        if DEBUG:
            self.player.draw_hit_box()
            self.scene["Platforms"].draw_hit_boxes() # For debugging

        self.ui_camera.use()
        arcade.draw_text("SCORE", 10, 10, arcade.csscolor.BLACK, 18)

    def on_update(self, delta_time: float):
        """Updates the logic of the game periodically.  Do not draw to the View here.

        Args:
            delta_time (float): The amount of time that has elapsed since the last update
        """

        # Player logic---------------------
        # Directional movement
        if self.input_manager.right and not self.input_manager.left: # No two button action
            self.physics_engine.apply_force(self.player, (16800, 0))
            self.player.facing = arcade.FACE_RIGHT
        elif self.input_manager.left and not self.input_manager.right:
            self.physics_engine.apply_force(self.player, (-16800, 0))
            self.player.facing = arcade.FACE_LEFT
        else: # Apply stopping force
            velocity = self.physics_engine.get_physics_object(self.player).body.velocity
            if self.physics_engine.is_on_ground(self.player): # Player actively stops if on the ground and not moving forward.
                if velocity[0] == 0:
                    direction = 0
                else:
                    direction = (velocity[0]/abs(velocity[0]))
                
                self.physics_engine.apply_force(self.player, (-direction * 9800, 0))

        # Jumping
        if self.input_manager.jump:  # If the player can jump then jump
            if self.physics_engine.is_on_ground(self.player) and self.player.jump_reset:
                self.player.jump(self.physics_engine)
        else:
            if self.physics_engine.is_on_ground(self.player):  # NEW PYMUNK ENGINE MORE GOOD
                self.player.jump_reset = True  # The jump option is available again because the key was released

        # Shooting
        if self.input_manager.shoot:
            self.player.shoot(self.scene.get_sprite_list("Bullets"), self.physics_engine)

        # Update stuff
  
        self.physics_engine.step()
        self.scene.update(["Player", "Enemies", "Bullets"])
        self.scene.update_animation(delta_time, ["Player", "Enemies", "Bullets"])
        self.player_camera.move_to(
            (
                self.player.camera_target[X_CORD] - SCREEN_WIDTH / 2,
                self.player.camera_target[Y_CORD] - SCREEN_HEIGHT / 2,
            ),
            0.09,
        )
        self._update_backgrounds()

        #Cleanup dead things
        sprite_list = self.scene.get_sprite_list("Bullets")

        for entity in reversed(sprite_list):
            if not entity.alive: # Remove dead entities
                sprite_list.remove(entity)
                self.physics_engine.remove_sprite(entity)




    # All input events simply pass their events to the input manager
    def on_key_press(self, key: int, modifiers: int):
        self.input_manager.key_down(self, key, modifiers)

    def on_key_release(self, key: int, modifiers: int):
        self.input_manager.key_up(self, key, modifiers)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        self.input_manager.mouse_down(self, x, y, button, modifiers)

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        self.input_manager.mouse_up(self, x, y, button, modifiers)


    def _update_backgrounds(self):
        """This method changes the background image locations in the scene according to the parallax information in the map file.
        """
        camera = self.player_camera.position # The backgrounds need to track to the camera

        for layer in self.map.tiled_map.layers: # Search through all the map layers for "BackgroundXX" where XX is a number
            if layer.name[0:-2] == "Background": # Is it a background?
                parallax_x = 1 - layer.parallax_factor.x # Get parallax factors from map layer
                parallax_y = 1 - layer.parallax_factor.y
                offset_x = layer.offset.x #Get offsets from map layer
                offset_y = layer.offset.y
                sprites = self.scene[layer.name].sprite_list #If it's in the map, it's in the scene I assume.
                for sprite in sprites: # Update each background sprite location to the new caluculated position.
                    sprite.center_x = camera.x * parallax_x + offset_x * GAME_SCALE + SCREEN_WIDTH
                    sprite.center_y = camera.y * parallax_y - offset_y * GAME_SCALE + 100
            
    
                