"""Main script to start the game"""
from maze_game.game_logic.game import Game


def launch():
    """Function to launch the game"""
    game = Game()
    while game.running:
        game.game_loop()
        game.main_menu.display_menu()


if __name__ == '__main__':
    launch()
