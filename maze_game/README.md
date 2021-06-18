I-PASS Project: Maze Game by Sjoerd Beetsma

How to run:
	1. Make sure all packages from requirements are installed. (pip install I_PASS/requirements.txt)
	2. Open up terminal and locate to main.py in the project directory
	3. enter command: python main.py
Alternatively:
	run main.py or maze_game/play_game.py from a IDE

I_PASS
│   LICENSE.TXT	-> containing license information (MIT)
│   main.py	-> main file to launch from terminal (had to be made seperately from start_game.py to work from terminal)
│   README.md	-> readme
│   requirements.txt -> required packages
│   setup.py	-> setup.py to export as a package
│   spel_instructies.txt -> instructions on how to play after launching
│
├───maze_game
│   │   animate_helpers.py -> animation helper functions/color constants
│   │   start_game.py -> main file from within the package to start the game
│   │
│   ├───documentation_html -> contains all docstrings (in maze_game so excluding test files) in generated HTML format
│   │   └───maze_game
│   │       ├───game_logic
│   │       └───maze_logic 
│   │                   
│   ├───game_logic -> logic to run the game
│   │      game.py -> Game class for gameloop eventhandeling managing game objects etc.
│   │      menu.py -> Menu class to create a simple mainmenu with states/settings
│   │      player.py -> Player class that can move around in the game (the end/finish ingame is also a Player)
│   │      __init__.py  
│   │
│   └───maze_logic -> logic to generate and solve mazes
│         maze.py -> Maze object class (starts out a grid full as 1's)
│         maze_generators.py -> Containing different algorithms to carve out/generate a Maze given a Maze Object
│         maze_solvers.py -> Containing different algorithms to solve mazes
│         __init__.py
│      
└───test
   │   animate_algorithms.py -> visualize ALL solvers and generators algorithms implemented
   │   maze_generators_test.py -> UNIT_TEST for maze generators
   │   maze_generators_time_test.py -> test runtime of generators
   │   maze_maze_test.py -> UNIT_TEST for Maze object
   │   maze_solvers_time_test.py -> test runtime of solvers
   │   maze_solver_test.py -> UNIT_TEST for maze solvers
   │
   └───test_time_results -> runtime results from generators/solvers
       	generators_timed[10x10-1000].png
        generators_timed[30x30-1000].png
        generators_timed[50x50-1000].png
       	solvers_timed[10x10-1000].png
        solvers_timed[30x30-1000].png
        solvers_timed[50x50-1000].png
