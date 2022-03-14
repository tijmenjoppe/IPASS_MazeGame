"""Main script to start the game"""
import sys
import os

dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
print(f"Adding '{dir}' to the file path.")
sys.path.insert(0, dir)


from maze_game.game_logic.game import Game


def launch():
    """Function to launch the game"""
    game = Game()
    while game.running:
        game.game_loop()
        game.main_menu.display_menu()


if __name__ == '__main__':
    launch()
