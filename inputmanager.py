import arcade

class InputManager():
    def __init__(self):
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.jump = False
        self.shoot = False
        self.mouse_current = None
        self.mouse_right_clicked_at = None
        self.mouse_left_clicked_at = None

    def key_down(self, context:arcade.View, key:int, modifiers:int):
        """Handles keyboard key press events

        Args:
            context (arcade.View): The calling object
            key (int): Which key was pressed (arcade.key)
            modifiers (int): Modifiers to key press
        """
        if key == arcade.key.W:
            self.up = True
        if key == arcade.key.A:
            self.left = True
        if key == arcade.key.S:
            self.down = True
        if key == arcade.key.D:
            self.right = True
        if key == arcade.key.SPACE:
            self.jump = True
        if key == arcade.key.ENTER:
            self.shoot = True

    def key_up(self, context:arcade.View, key:int, modifiers:int):
        """Handles keyboard key press release events

        Args:
            context (arcade.View): The calling object
            key (int): Which key press was released (arcade.key)
            modifiers (int): Modifiers to key press release
        """
        if key == arcade.key.W:
            self.up = False
        if key == arcade.key.A:
            self.left = False
        if key == arcade.key.S:
            self.down = False
        if key == arcade.key.D:
            self.right = False
        if key == arcade.key.SPACE:
            self.jump = False
        if key == arcade.key.ENTER:
            self.shoot = False

    def mouse_down(self, context: arcade.View, x:int, y:int, button:int, modifiers:int):
        """Handles mouse button clicks. Also tracks mouse location

        Args:
            context (arcade.View): The calling object
            x (int): Screen x coordinate of the mouse click
            y (int): Screen y coordinate of the mouse click
            button (int): Which button was clicked (arcade.key)
            modifiers (int): Modifiers to the button click
        """
        if button == arcade.MOUSE_BUTTON_LEFT: #Fire
            self.shoot = True
            self.mouse_left_clicked_at = (x,y)
            self.mouse_current = (x,y)
        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.mouse_left_released_at = (x,y)
            self.mouse_current = (x,y)
    
    def mouse_up(self, context: arcade.View, x:int, y:int, button:int, modifiers:int):
        """Handles mouse button click releases. Also tracks mouse location

        Args:
            context (arcade.View): The calling object
            x (int): Screen x coordinate of the mouse click
            y (int): Screen y coordinate of the mouse click
            button (int): Which button was clicked (arcade.key)
            modifiers (int): Modifiers to the button click
        """
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.shoot = False
            self.mouse_right_clicked_at = (x,y)
            self.mouse_current = (x,y)
        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.mouse_right_released_at = (x,y)
            self.mouse_current = (x,y)