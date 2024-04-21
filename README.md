# Astro Jump

Welcome to the GitHub repository for my game **Astro Jump**, an action packed, 2D pixel art, platformer. You will need to traverse multiple levels with danger waiting behind every corner. If you want to know more detailed information about the project, please check my [documentation](https://astro-jump-docs.vercel.app)

### Installation

1. Download `AstroJumpEXE.zip` from the releases section.
2. Unzip the contents into a file.
3. Install the necessary dependencies.
4. Click the AstroJump.exe and enjoy!!

### Game Overview

- Start from Level 0 and find your way through to Level 3.
- Be ready for a chalenging experience and dont give up.
- Also checkout all the options in the main menu such as settings or tutorial.

### How to play

- Use the A and D keys for moving left and right.
- Use SPACE to jump.
- Avoid dangers like spikes and bullets.
- Reach the end of each level from 1 to 3.
- Dont forget not to fall into the void!

### File Structure

- `AstroJump.exe`: The executable file to launch the game.
- `main.py`: The main script that initializes and runs the game.
- `game.py`: The central hub in which the main loop and all of the game states are.
- `player.py`: Handles everything for the players such as drawing, respawning etc.
- `enemy.py`: Manages the cannon projectiles.
- `slider.py`: Handles the sliders used in the settings.
- `camera.py`: Manages the camera which moves with the player as he progreses the level.
- `animation.py`: Handles the animation of the player.
- `settings.py`: Contains configuration settings for the game.
- `transition.py`: Creates a transition effect that is used for entering a level from the menu or progresing from one level to another.
- `particle.py`: Manages a particle effect that occurs when the player dies.
- `Graphics/`: Contains all of the games graphic assets.
- `Sounds/`: Contains all of the games sound assets.
- `levels/`: Contains all 3 levels as .csv files.

### Dependencies

Before running the game, ensure the following dependencies are installed:

- Python 3.12
- Pygame
- OS (usually comes with Python)

### Installing Python

Download Python 3.12 from the [official Python website](https://www.python.org/). During installation, ensure to check the option "Add Python to PATH".

### Installing Pygame and other libraries

After Python is installed, you can install the remaining dependencies using pip, Python's package installer. Run the following command in your terminal (Command Prompt or PowerShell on Windows):

```bash
pip install pygame 
