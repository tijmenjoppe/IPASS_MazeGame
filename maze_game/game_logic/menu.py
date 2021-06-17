from maze_game.animate_helpers import *

class Menu():
    """ Menu class to create mainmenu for game
    Attributes:
            game (Game): Game object for which to be a menu for
            run_menu (bool): True or False whether the menu is running
            state (String): current state of the menu used for simple state machine
            mid_width (int): mid point of width to center menu labels
            mid_height (int): mid point of height to center menu labels
            start_x, start_y | difficulty_x difficulty_y | ... (int): representing the x and y position of each label on the menu
            selection_pointer (pygame Rect): Rect object to represent a cursor/pointer in the menu"""
    def __init__(self, game):
        self.game = game
        self.game.display_height = 250
        self.game.display_width = 400

        self.run_menu = True
        self.state = 'Start'

        self.mid_width = self.game.display_width / 2
        self.mid_height = self.game.display_height / 2

        self.start_x, self.start_y = self.mid_width, self.mid_height - 100
        self.difficulty_x, self.difficulty_y = self.mid_width, self.mid_height - 60
        self.height_x, self.height_y = self.mid_width, self.mid_height - 30
        self.width_x, self.width_y = self.mid_width, self.mid_height
        self.animate_x, self.animate_y = self.mid_width, self.mid_height + 30
        self.exit_x, self.exit_y = self.mid_width, self.mid_height + 100

        self.selection_pointer = pygame.Rect(self.start_x, self.start_y, 20, 20)

    def draw_pointer(self):
        """function to draw_pointer on the screen"""
        # pointer has offset of -180 on x axis
        self.game.draw_text('->', 20, self.selection_pointer.x + -180, self.selection_pointer.y, RED)

    def change_state(self):
        """Function to change menu states gets called every frame"""
        # dictionaries to store what state to change to from which on up and down event.
        down = {'Start': [self.difficulty_x, self.difficulty_y, 'Difficulty'],
                'Difficulty': [self.height_x, self.height_y, 'Height'],
                'Height': [self.width_x, self.width_y, 'Width'], 'Width': [self.animate_x, self.animate_y, 'Animate'],
                'Animate': [self.exit_x, self.exit_y, 'Exit'], 'Exit': [self.start_x, self.start_y, 'Start']}
        up = {'Start': [self.exit_x, self.exit_y, 'Exit'], 'Difficulty': [self.start_x, self.start_y, 'Start'],
              'Height': [self.difficulty_x, self.difficulty_y, 'Difficulty'],
              'Width': [self.height_x, self.height_y, 'Height'], 'Animate': [self.width_x, self.width_y, 'Width'],
              'Exit': [self.animate_x, self.animate_y, 'Animate']}

        # if key is up or down change state according to up down dictionaries
        if self.game.K_DOWN:
            self.selection_pointer.midtop = (down[self.state][0], down[self.state][1])
            self.state = down[self.state][2]
        elif self.game.K_UP:
            self.selection_pointer.midtop = (up[self.state][0], up[self.state][1])
            self.state = up[self.state][2]
        # if key is enter and state is Start: start the game. if state is Exit: exit the game(including menu)
        elif self.game.K_ENTER:
            if self.state == 'Start':
                self.game.in_game = True
                self.run_menu = False
            elif self.state == 'Exit':
                self.run_menu = False
                self.game.running = False
        # if key is right or left
        # depending on the state height/width/difficulty/animation speed gets incremented up(right) or down(left)
        elif self.game.K_RIGHT:
            if self.state == 'Height':
                self.game.maze_h += 1
            elif self.state == 'Width':
                self.game.maze_w += 1
            elif self.state == 'Difficulty' and self.game.maze_difficulty < 3:
                self.game.maze_difficulty += 1
            elif self.state == 'Animate':
                self.game.animate_fps += 10
        elif self.game.K_LEFT:
            if self.state == 'Height' and self.game.maze_h > 3:
                self.game.maze_h -= 1
            elif self.state == 'Width' and self.game.maze_w > 3:
                self.game.maze_w -= 1
            elif self.state == 'Difficulty' and self.game.maze_difficulty > 1:
                self.game.maze_difficulty -= 1
            elif self.state == 'Animate' and self.game.animate_fps > 0:
                self.game.animate_fps -= 10

    def display_menu(self):
        """game loop of the menu itself"""
        # rescale to appropriate menu dimensions
        self.game.display = pygame.display.set_mode((self.game.display_width, self.game.display_height))
        # difficulties stored as int to make more readable for user make labels:
        difficulty_labels = {1: 'Easy', 2: 'Medium', 3: 'Hard'}
        # one line function to return No if fps == 0 else string 'fps: someInt'
        animate_label = lambda fps: 'Nee' if fps == 0 else f'fps: {fps}'

        while self.run_menu:
            # get inputs from event loop
            self.game.event_loop()
            # change state (only changes state if specific inputs are pressed)
            self.change_state()

            self.game.display.fill(WHITE)
            self.game.draw_text('START!', 20, self.start_x, self.start_y, GREEN)
            self.game.draw_text(f'<Moeilijkheid {difficulty_labels[self.game.maze_difficulty]} >', 20,
                                self.difficulty_x, self.difficulty_y, BLACK)
            self.game.draw_text(f'< Hoogte {self.game.maze_h} >', 20, self.height_x, self.height_y, BLACK)
            self.game.draw_text(f'< Breedte {self.game.maze_w} >', 20, self.width_x, self.width_y, BLACK)
            self.game.draw_text(f'< visualiseer Algoritmes {animate_label(self.game.animate_fps)}>', 20, self.animate_x,
                                self.animate_y, BLACK)
            self.game.draw_text('Afsluiten', 20, self.exit_x, self.exit_y, RED)
            self.draw_pointer()
            pygame.display.flip()
            self.game.reset_keys()





