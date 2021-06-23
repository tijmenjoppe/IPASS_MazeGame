I-PASS Project: Maze Game by Sjoerd Beetsma<br/>
How to launch:<br/>
	1. Make sure all packages from requirements are installed. (pip install I_PASS/requirements.txt)<br/>
	2. Run maze_game/start_game.py<br/>
<br/>
References:<br/>
Algorithm generated maze difficulies:<br/>
-Gabrovšek, P (2019). Analysis of Maze Generating Algorithms, IPSI Transactions on Internet Research, Vol. 15, No. 1<br/>
Maze generators:<br/>
-Kim, P. (2019). Intelligent Maze Generation. (Electronic Thesis or Dissertation).<br/>
Maze solvers:
-Babula, M. (2009). Simulated maze solving algorithms through unknown mazes. Organizing and Program Committee, 13.<br/>
<br/>
I_PASS<br/>
├───maze_game
│   │   animate_helpers.py   -> animation helper functions/color constants<br/>
│   │   start_game.py        -> main file from within the package to start the game<br/>
│   │   LICENSE.TXT	     -> containing license information (MIT)<br/>
│   │   main.py	             -> main file to launch from terminal (had to be made seperately from start_game.py to work from terminal)<br/>
│   │   README.md<br/>
│   │   requirements.txt     -> required packages<br/>
│   │   spel_instructies.txt -> instructions on how to play the game itself.<br/>
│   │<br/>
│   ├───documentation_html   -> contains all docstrings (in maze_game so excluding test files) in generated HTML format<br/>
│   │   └───maze_game<br/>
│   │       ├───game_logic<br/>
│   │       └───maze_logic<br/>
│   │<br/>                   
│   ├───game_logic           -> logic to run the game<br/>
│   │      game.py           -> Game class for gameloop eventhandeling managing game objects etc.<br/>
│   │      menu.py 	     -> Menu class to create a simple mainmenu with states/settings<br/>
│   │      player.py 	     -> Player class that can move around in the game (the end/finish ingame is also a Player)<br/>
│   │      __init__.py<br/>  
│   │
│   └───maze_logic 	     -> logic to generate and solve mazes<br/>
│         maze.py            -> Maze object class (starts out a grid full as 1's)<br/>
│         maze_generators.py -> Containing different algorithms to carve out/generate a Maze given a Maze Object<br/>
│         maze_solvers.py    -> Containing different algorithms to solve mazes<br/>
│         __init__.py<br/>
│<br/>      
└───test -> testing directory
   │   animate_algorithms.py   -> visualize all solvers and generators algorithms implemented<br/>
   │   maze_generators_test.py -> UNIT_TEST for maze generators<br/>
   │   maze_maze_test.py       -> UNIT_TEST for Maze object<br/>
   │   maze_solver_test.py     -> UNIT_TEST for maze solvers<br/>
   │<br/>
   └───test_time_results             -> runtime results from generators/solvers<br/>
	maze_generators_time_test.py -> test runtime of generators<br/>
	maze_solvers_time_test.py    -> test runtime of solvers<br/>
       	generators_timed[10x10-1000].png<br/>
        generators_timed[30x30-1000].png<br/>
        generators_timed[50x50-1000].png<br/>
       	solvers_timed[10x10-1000].png<br/>
        solvers_timed[30x30-1000].png<br/>
        solvers_timed[50x50-1000].png<br/>
