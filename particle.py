import pygame
import random


class Particle:
    """
    Represents a single particle of an explosion effect.

    Each particle has its own position, velocity, and lifespan. Particles are drawn
    as small circles and move outward from their origin point.

    :param x: Initial x-coordinate of the particle.
    :param y: Initial y-coordinate of the particle.
    :param lifespan: Number of frames the particle will be alive.

    :type x: float
    :type y: float
    :type lifespan: int
    """

    def __init__(self, x, y, lifespan):
        """
        Initialize a particle with velocity and lifespan.

        Velocity is randomly generated to create an explosion effect.
        """
        self.x = x
        self.y = y
        self.x_vel = random.uniform(-5, 5)
        self.y_vel = random.uniform(-5, 5)
        self.lifespan = lifespan
        self.alive = True

    def update(self):
        """
        Update the particle's position based on its velocity and reduce its lifespan.

        This method should be called once per frame.
        """
        if self.alive:
            self.x += self.x_vel
            self.y += self.y_vel
            self.lifespan -= 1
            if self.lifespan <= 0:
                self.alive = False

    def draw(self, screen):
        """
        Draw the particle on the specified screen as a circle.

        :param screen: The Pygame surface to draw the particle on.
        :type screen: pygame.Surface
        """
        if self.alive:
            pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)),
                               3)


class ParticleSystem:
    """
    Manages all particles in the game to create an explosion effect when needed.

    This class handles updating and drawing all active particles, and it can emit
    new particles when an explosion is triggered.
    """

    def __init__(self):
        """
        Create a new particle system.

        Initializes an empty list to hold all particles.
        """
        self.particles = []

    def emit(self, x, y, amount, lifespan=30):
        """
        Emit a number of particles from a specific point.

        :param x: x-coordinate from where particles are emitted.
        :param y: y-coordinate from where particles are emitted.
        :param amount: Number of particles to emit.
        :param lifespan: Number of frames each particle will live.

        :type x: float
        :type y: float
        :type amount: int
        :type lifespan: int
        """
        for _ in range(amount):
            self.particles.append(Particle(x, y, lifespan))

    def update(self):
        """
        Update all particles in the system.

        Particles are updated and removed if their lifespan has expired.
        """
        for particle in self.particles[:]:
            particle.update()
            if not particle.alive:
                self.particles.remove(particle)

    def draw(self, screen):
        """
        Draw all particles on the specified screen.

        :param screen: The Pygame surface where particles will be drawn.
        :type screen: pygame.Surface
        """
        for particle in self.particles:
            particle.draw(screen)

