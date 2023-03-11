# RoboHanoi
Hello and Welcome to RoboHanoi - an Interactive game based on the classic Tower of Hanoi problem.

Here you can find all code used to create a real-world Human vs. 6 DOF Robot game.

Video example: https://technionmail-my.sharepoint.com/:v:/g/personal/nir_levy_campus_technion_ac_il/EUtX08YsOXpPqrFyOgnVl4UBaD94o-FSorV6FxvRmxLRhg?e=iUpKQX

## Main Components
### Game
Running `game.py` will start the game, including all features and components. The game includes a home screen based on the Tkinter library, which inlcudes a button for switching turns between the human and the Robot.

The whole time, 3 components run in the same time using multithreading:

1. The game itself - the tkinter button and all commands relevant for switching turns and connecting between different modules.

2. Camera - a real-time vision based system that captures the scene and understands the current state of the game in every frame (runs in 30 fps).

3. Planner (called 'perform_planning') - the module responsible for planning (using unified planning) and the execution of the plan by the robot.

### Hanoi
The class responsible for the planning. It is defined in a way that given a `state_map` dictionary, it generates an appropriate plan to solve the game (using unified planning).

### Hanoi Interpreter
The class responsible for understanding the game state. Given an image, it produces a `state_map`.

### Execution (BEN.py)
The class responsible for the execution of a plan by the robot. To play in turns with a human, we defined the method `execute_next` which only executes the first action of a given plan.

### Control, Move
Implementation of robot-specific actions needed to execute action in the real world.
