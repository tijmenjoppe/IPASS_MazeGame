from maze.maze import Maze
from maze.maze_solvers import breadth_first_search, depth_first_search
from menu import Menu
from pygame.locals import *
import time
from maze.animate_helpers import *
import pygame


class Player(pygame.Rect):
    def __init__(self, x, y, height, width):
        super(Player, self).__init__((x, y, height, width))
        self.velx = 1
        self.vely = 1

    def move_player(self, game):
        if game.K_DOWN:
            self.y += self.vely
            for col in game.check_collision(self):
                if self.y > 5:
                    self.bottom = col.top
        if game.K_UP:
            self.y -= self.vely
            for col in game.check_collision(self):
                if self.y > 5:
                    self.top = col.bottom
        if game.K_RIGHT:
            self.x += self.velx
            for col in game.check_collision(self):
                if self.x > 0:
                    self.right = col.left
        if game.K_LEFT:
            self.x -= self.velx
            for col in game.check_collision(self):
                if self.x > 0:
                    self.left = col.right

    def draw(self, win):
        pygame.draw.rect(win, RED, (self.x, self.y, self.width, self.height))


class Game():
    def __init__(self):
        pygame.init()
        # setup screen
        self.display_width = 720
        self.display_height = 480
        self.display = pygame.display.set_mode((self.display_width, self.display_height))
        # the game application is running
        self.running = True
        # player is in game
        self.in_game = False
        # pygame Clock to manage fps
        self.clock = pygame.time.Clock()
        # keyboard inputs used
        self.K_UP, self.K_DOWN, self.K_LEFT, self.K_RIGHT, self.K_ENTER, K_ESC = False, False, False, False, False, False
        # default font
        self.font = pygame.font.get_default_font()
        # standard maze settings/values to generate a new maze
        self.maze_w = 25
        self.maze_h = 25
        self.maze_difficulty = 1
        self.difficulty = 1
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

    def draw_text(self, text, size, x, y, color=WHITE):
        font = pygame.font.Font(self.font, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

    def reset_keys(self):
        # func to reset all keys to False ie: not pressed on every new frame of the game
        self.K_LEFT, self.K_RIGHT, self.K_UP, self.K_DOWN, self.K_ENTER, self.K_ESC = False, False, False, False, False, False

    def solve(self, maze, player, solver):

        path_to_finish = solver(maze,
                                start_pos=(int(player.x / self.tile_size), int(player.y / self.tile_size)),
                                animate=self.animate_fps)
        self.display.fill(WHITE)
        pygame.draw.rect(self.display, YELLOW, (
            maze.end[0] * self.tile_size, maze.end[1] * self.tile_size, self.tile_size, self.tile_size))
        self.draw_walls()
        for step in path_to_finish:

            while step != (player.x / self.tile_size, player.y / self.tile_size):
                self.event_loop()
                x_dif = step[0] - int(player.x / self.tile_size)
                y_dif = step[1] - int(player.y / self.tile_size)
                if 0 < y_dif <= 1:
                    self.K_DOWN = True
                    player.move_player(self)
                    self.reset_keys()
                if -1 <= y_dif <= 0:
                    self.K_UP = True
                    player.move_player(self)
                    self.reset_keys()
                if 0 < x_dif <= 1:
                    self.K_RIGHT = True
                    player.move_player(self)
                    self.reset_keys()
                if -1 <= x_dif <= 0:
                    self.K_LEFT = True
                    player.move_player(self)
                    self.reset_keys()

                # no trail
                player.draw(self.display)
                pygame.display.update()
                self.clock.tick(3000)

    def game_loop(self):
        maze = Maze(self.maze_h, self.maze_w, self.maze_difficulty, self.animate_fps)
        p_1 = Player(1 * self.tile_size, 1 * self.tile_size, self.tile_size, self.tile_size)
        self.walls = []
        ingame_display_width, ingame_display_height = maze.rows * self.tile_size, maze.cols * self.tile_size
        self.display = pygame.display.set_mode((ingame_display_width, ingame_display_height))
        self.add_walls(maze)
        while self.in_game:
            if (int(p_1.x / self.tile_size), int(p_1.y / self.tile_size)) == maze.end:
                self.draw_text('Win!', 30, ingame_display_width / 2, ingame_display_height / 2, GREEN)
                pygame.display.flip()
                time.sleep(1.5)

                self.in_game = False
                self.main_menu.run_menu = True
            self.display.fill(WHITE)
            self.draw_walls()
            self.event_loop()
            # draw finish
            pygame.draw.rect(self.display, YELLOW, (
                maze.end[0] * self.tile_size, maze.end[1] * self.tile_size, self.tile_size, self.tile_size))
            # player movement and redraw
            p_1.move_player(self)
            p_1.draw(self.display)
            # redraw the walls

            if self.K_ENTER:
                self.solve(maze, p_1, breadth_first_search)
            if self.K_ESC:
                self.solve(maze, p_1, depth_first_search)
            self.clock.tick(120)
            pygame.display.flip()

    def add_walls(self, maze):
        for i in range(maze.rows):
            for j in range(maze.cols):
                y = j * self.tile_size
                x = i * self.tile_size
                if maze.grid[i][j] == 1:
                    self.walls.append(pygame.Rect(x, y, self.tile_size, self.tile_size))

    def draw_walls(self):
        for wall in self.walls:
            pygame.draw.rect(self.display, BLACK, wall)

    def check_collision(self, player):
        collisions = []
        for wall in self.walls:
            if player.colliderect(wall):
                collisions.append(wall)
        return collisions
