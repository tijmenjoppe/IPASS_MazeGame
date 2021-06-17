from maze_game.maze_logic.maze import Maze
from maze_game.maze_logic.maze_solvers import depth_first_search
from .menu import Menu
from .player import Player
from pygame.locals import *
import time
from maze_game.animate_helpers import *

class Game:
    """Game object for playing a maze game
        Attributes:
            running (bool): true or false whether a pygame process is running (menu or game)
            in_game (bool): true or false whether in game
            fps (int): in game FPS
            K_UP, ... K_ESC (bool): true representing active key false representing non active key
            font (font): font for displaying text
            maze_w (int): standard maze_w
            maze_h (int): standard maze_h
            maze_difficulty (int): standard maze_difficulty
            tile_size (int): size of tiles in game, tiles will be squares ex: tile_size = 15 makes 15x15 tiles
            animate_fps (int): animation speed of solving and/or generating algorithms if 0 they won't be animated
            main_menu (Menu): Menu object serving as main menu
        """
    def __init__(self):
        pygame.init()
        # the game application is running
        self.running = True
        # player is in game
        self.in_game = False
        # pygame Clock to manage fps
        self.clock = pygame.time.Clock()
        self.fps = 120
        # keyboard inputs used
        self.K_UP, self.K_DOWN, self.K_LEFT, self.K_RIGHT, self.K_ENTER, self.K_ESC = False, False, False, False, False, False
        # default font
        self.font = pygame.font.get_default_font()
        # standard maze settings/values to display
        self.maze_w = 10
        self.maze_h = 10
        self.maze_difficulty = 1
        self.tile_size = 15
        self.animate_fps = 0
        self.main_menu = Menu(self)

    def event_loop(self):
        """gets called once every frame to update all current events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # quit event
                self.in_game = False
                self.running = False
            if event.type == pygame.KEYDOWN:  # key press event
                if event.key == K_UP:
                    self.K_UP = True
                if event.key == K_DOWN:
                    self.K_DOWN = True
                if event.key == K_LEFT:
                    self.K_LEFT = True
                if event.key == K_RIGHT:
                    self.K_RIGHT = True
                if event.key == K_RETURN:
                    self.K_ENTER = True
                if event.key == K_ESCAPE:
                    self.K_ESC = True
            if event.type == pygame.KEYUP:  # key release event
                if event.key == K_UP:
                    self.K_UP = False
                if event.key == K_DOWN:
                    self.K_DOWN = False
                if event.key == K_LEFT:
                    self.K_LEFT = False
                if event.key == K_RIGHT:
                    self.K_RIGHT = False
                if event.key == K_RETURN:
                    self.K_ENTER = False
                if event.key == K_ESCAPE:
                    self.K_ESC = False

    def game_loop(self):
        # new maze, player, finish, wall objects in game loop to create a new instance every game
        maze = Maze(x=self.maze_w, y=self.maze_h, gen_func=self.maze_difficulty, animate=self.animate_fps)
        self.player = Player(maze.start[1] * self.tile_size, maze.start[0] * self.tile_size, self.tile_size,
                             self.tile_size, RED)
        self.finish = Player(maze.end[1] * self.tile_size, maze.end[0] * self.tile_size, self.tile_size, self.tile_size,
                             YELLOW)
        self.walls = []
        # setup screen resolution according to the maze size
        ingame_display_width, ingame_display_height = maze.cols * self.tile_size, maze.rows * self.tile_size
        self.display = pygame.display.set_mode((ingame_display_width, ingame_display_height))
        # add walls to the game object from the maze
        self.add_walls(maze)

        while self.in_game:
            # win condition if player has collision with finish
            if self.player.colliderect(self.finish):
                # display text indicating the game is over and update screen
                self.draw_text('WIN!', 30, ingame_display_width / 2, ingame_display_height / 2, GREEN)
                pygame.display.flip()
                # wait 2 seconds and return to main menu
                time.sleep(2)
                self.in_game = False
                self.main_menu.run_menu = True

            # paths are white, walls will be drawn over white canvas making the paths white by default
            self.display.fill(WHITE)
            # check events
            self.event_loop()
            # move player based on events in game object (self)
            self.player.move_player(self)
            # re-draw everything
            self.draw_all()
            # if key is enter solve the maze if key is ESC return to main menu
            if self.K_ENTER:
                self.solve(maze, self.player, depth_first_search)
            if self.K_ESC:
                self.in_game = False
            # tick the clock to run game at defined fps
            self.clock.tick(self.fps)
            pygame.display.flip()

    def solve(self, maze, player, solver):
        """function to show the solution and also solve
            the function will run a pathfinding algorithm and take over the player's controls to finish the game
            args:
                maze: Maze object containing a perfect maze
                player: player object
                solver: solver function"""
        # get path from current position to finish from a solver function
        path_to_finish = solver(maze,
                                start_pos=(int(player.y / self.tile_size), int(player.x / self.tile_size)),
                                animate=self.animate_fps)

        # change velocity of player so the computer solving the maze doesn't look super slow
        player.velx = 3
        player.vely = 3

        # for steps in path to finish: simulate key presses to move to the next step based on the difference in x and y axis.
        # do this for every step until finish is reached.
        for step in path_to_finish:
            while step != (round(player.y / self.tile_size), round(player.x / self.tile_size)):
                x_dif = step[1] - (player.x / self.tile_size)
                y_dif = step[0] - (player.y / self.tile_size)

                if y_dif > 0:
                    self.K_DOWN = True
                    player.move_player(self)
                    self.reset_keys()

                if y_dif < 0:
                    self.K_UP = True
                    player.move_player(self)
                    self.reset_keys()

                if x_dif > 0:
                    self.K_RIGHT = True
                    player.move_player(self)
                    self.reset_keys()

                if x_dif < 0:
                    self.K_LEFT = True
                    player.move_player(self)
                    self.reset_keys()

                self.event_loop()
                self.draw_all()
                self.clock.tick(self.fps)
                pygame.display.flip()


    def draw_text(self, text, size, x, y, color=WHITE):
        """method to draw text over the screen
            args:
                text: string of which text to display
                size: font size (int)
                x: x position on pygame display
                y: y position on pygame display
                color: text color"""

        font = pygame.font.Font(self.font, size)
        text_surface = font.render(text, True, color)

        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

    def add_walls(self, maze):
        """function to add walls from a maze object to the game as a Rectangle object (to handle collisions easily)
        args:
            maze: Maze object containing a perfect maze"""
        for i in range(maze.rows):
            for j in range(maze.cols):
                y = i * self.tile_size
                x = j * self.tile_size
                if maze.grid[i][j] == 1:
                    self.walls.append(pygame.Rect(x, y, self.tile_size, self.tile_size))

    def draw_walls(self):
        """function to draw walls on the screen"""
        for wall in self.walls:
            pygame.draw.rect(self.display, BLACK, wall)

    def check_collision(self, player):
        """function to check for collisions between a given player and all the walls in the game
        args:
            player: player object to check for collisions
        returns:
            list with all walls that are in collision with player
        """
        collisions = []
        for wall in self.walls:
            if player.colliderect(wall):
                collisions.append(wall)
        return collisions

    def reset_keys(self):
        """function to reset all key presses each frame"""
        self.K_LEFT, self.K_RIGHT, self.K_UP, self.K_DOWN, self.K_ENTER, self.K_ESC = False, False, False, False, False, False

    def draw_all(self):
        """function that calls all drawing functions to re-draw the entire scene with 1 function call"""
        self.draw_walls()
        self.player.draw(self.display)
        self.finish.draw(self.display)
