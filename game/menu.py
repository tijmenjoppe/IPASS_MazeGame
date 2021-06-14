import pygame
import game
from maze.animate_helpers import *


class Menu():
    def __init__(self, game):
        self.game = game
        self.game.display_height = 300
        self.game.display_width = 400
        self.mid_width = self.game.display_width / 2
        self.mid_height = self.game.display_height / 2

        self.run_menu = True

        self.state = 'Start'
        self.start_x, self.start_y = self.mid_width, self.mid_height - 100
        self.difficulty_x, self.difficulty_y = self.mid_width, self.mid_height - 50
        self.height_x, self.height_y = self.mid_width, self.mid_height - 20
        self.width_x, self.width_y = self.mid_width, self.mid_height + 10
        self.animate_x, self.animate_y = self.mid_width, self.mid_height + 40

        self.exit_x, self.exit_y = self.mid_width, self.mid_height + 100

        self.offset = -180
        self.pointer_rect = pygame.Rect(self.start_x + self.offset, self.start_y, 20, 20)

    def draw_pointer(self):
        self.game.draw_text('->', 20, self.pointer_rect.x, self.pointer_rect.y, RED)

    def move_pointer(self):
        down = {'Start': [self.difficulty_x, self.difficulty_y, 'Difficulty'],
                'Difficulty': [self.height_x, self.height_y, 'Height'],
                'Height': [self.width_x, self.width_y, 'Width'], 'Width': [self.animate_x, self.animate_y, 'Animate'],
                'Animate': [self.exit_x, self.exit_y, 'Exit'], 'Exit': [self.start_x, self.start_y, 'Start']}

        up = {'Start': [self.exit_x, self.exit_y, 'Exit'], 'Difficulty': [self.start_x, self.start_y, 'Start'],
              'Height': [self.difficulty_x, self.difficulty_y, 'Difficulty'],
              'Width': [self.height_x, self.height_y, 'Height'], 'Animate': [self.width_x, self.width_y, 'Width'],
              'Exit': [self.animate_x, self.animate_y, 'Animate']}
        if self.game.K_DOWN:
            self.pointer_rect.midtop = (down[self.state][0] + self.offset, down[self.state][1])
            self.state = down[self.state][2]
        if self.game.K_UP:
            self.pointer_rect.midtop = (up[self.state][0] + self.offset, up[self.state][1])
            self.state = up[self.state][2]

    def display_menu(self):
        self.run_menu = True
        self.game.display = pygame.display.set_mode((self.game.display_width, self.game.display_height))
        difficulty_labels = {1: 'Easy', 2: 'Medium', 3: 'Hard', 4: 'Hardv2', 5: 'Hardv3'}
        # one line function to return No if fps == 0 (algorithm animation won't be turned on)
        animate_label = lambda fps: 'No' if fps == 0 else f'fps: {fps}'

        while self.run_menu:
            self.game.event_loop()
            self.check_input()
            self.game.display.fill(BLACK)
            self.game.draw_text('START!', 20, self.start_x, self.start_y, GREEN)
            self.game.draw_text(f'<Moeilijkheid {difficulty_labels[self.game.maze_difficulty]} >', 20,
                                self.difficulty_x, self.difficulty_y)
            self.game.draw_text(f'< hoogte {self.game.maze_h} >', 20, self.height_x, self.height_y)
            self.game.draw_text(f'< breedte {self.game.maze_w} >', 20, self.width_x, self.width_y)
            self.game.draw_text(f'< Algoritmes animeren {animate_label(self.game.animate_fps)}>', 20, self.animate_x,
                                self.animate_y)
            self.game.draw_text('Afsluiten', 20, self.exit_x, self.exit_y, RED)
            self.draw_pointer()
            pygame.display.flip()
            self.game.reset_keys()

    def check_input(self):
        self.move_pointer()
        if self.game.K_ENTER:
            if self.state == 'Start':
                self.game.in_game = True
                self.run_menu = False
        if self.game.K_RIGHT:
            if self.state == 'Height':
                self.game.maze_h += 1
            if self.state == 'Width':
                self.game.maze_w += 1
            if self.state == 'Difficulty' and self.game.maze_difficulty < 5:
                self.game.maze_difficulty += 1
            if self.state == 'Animate':
                self.game.animate_fps += 10
        if self.game.K_LEFT:
            if self.state == 'Height' and self.game.maze_h > 3:
                self.game.maze_h -= 1
            if self.state == 'Width' and self.game.maze_w > 3:
                self.game.maze_w -= 1
            if self.state == 'Difficulty' and self.game.maze_difficulty > 1:
                self.game.maze_difficulty -= 1
            if self.state == 'Animate' and self.game.animate_fps > 0:
                self.game.animate_fps -= 10
