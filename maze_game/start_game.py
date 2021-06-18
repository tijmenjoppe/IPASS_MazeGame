"""Script to launch the game"""
from game_logic.game import Game


def launch():
    """Function to launch the game"""
    game = Game()
    while game.running:
        game.main_menu.display_menu()
        game.game_loop()


if __name__ == '__main__':
    launch()
