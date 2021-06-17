import pygame

class Player(pygame.Rect):
    """ Player object used as player in maze game
    Attributes:
        velx (int): movement speed on x axis
        vely (int): movement speed on y axis
        color (tuple): player(/square) color
    """
    def __init__(self, x, y, height, width, color):
        """args:
            x (int): starting position on x axis
            y (int): starting position on y axis
            height (int): height of player
            width (int): width of player
            color (tuple): rgb color code used as player(/square) color"""
        super(Player, self).__init__((x, y, height, width))
        self.velx = 1
        self.vely = 1
        self.color = color

    def move_player(self, game):
        """Function that checks boolean key values for the player's movement keys
        if a key is true the x/y position will change to the new position given there is no collision.
        if there is a collision the player will be moved to the top/bottom/left/right of the colliding object"""

        if game.K_DOWN:
            self.y += self.vely
            for col in game.check_collision(self):
                self.bottom = col.top

        if game.K_UP:
            self.y -= self.vely
            for col in game.check_collision(self):
                self.top = col.bottom

        if game.K_RIGHT:
            self.x += self.velx
            for col in game.check_collision(self):
                self.right = col.left
        if game.K_LEFT:
            self.x -= self.velx
            for col in game.check_collision(self):
                self.left = col.right

    def draw(self, win):
        """draw player on the window
        args:
            win: pygame display object"""
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))