import arcade

X_CORD = 0
Y_CORD = 1

class LRTextureList:
    """This holds a left and right facing list of textures for sprites to use.  The texture is from a sprite sheet.
    """
    def __init__(self):
        self.right = [[arcade.Texture]]
        self.left = [[arcade.Texture]]

