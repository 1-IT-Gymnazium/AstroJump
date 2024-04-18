import pygame
from game import Game


class Main:
    """
    The main entry point for the game, initializing and running the game loop.
    """

    def __init__(self):
        """
        Initializes the Pygame framework, sets up the main display surface in fullscreen mode,
        and creates a game clock and an instance of the Game class to manage game logic.
        """
        pygame.init()
        self.display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.game = Game()

    def run(self):
        """
        Runs the main game loop, updating the game state and rendering each frame.
        This loop continues indefinitely until the game is closed.
        """
        while True:
            dt = self.clock.tick() / 1000  # Time since last frame in seconds.

            self.game.main_menu()  # Call the main_menu method of the Game class.
            pygame.display.update()  # Updates the contents of the entire display.


if __name__ == "__main__":
    main = Main()
    main.run()
