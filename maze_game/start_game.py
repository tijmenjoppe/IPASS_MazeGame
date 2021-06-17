from maze_game.game_logic.game import Game


def launch():
    game = Game()
    while game.running:
        game.main_menu.display_menu()
        game.game_loop()


if __name__ == '__main__':
    launch()
